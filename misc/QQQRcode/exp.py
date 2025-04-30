from pwn import *
import hashlib
import itertools
import string

io = remote("1.95.71.197",9999)

def pow(target_hash, suffix):
    charset = string.ascii_letters + string.digits
    for combo in itertools.product(charset, repeat=4):
        xxxx = "".join(combo)
        candidate = xxxx + suffix
        hash_result = hashlib.sha256(candidate.encode()).hexdigest()
        if hash_result == target_hash:
            return xxxx
    return None

suffix = io.recvuntil(b")").decode().split("+")[-1][:-1]
target = io.recvline().decode().split("=")[-1].strip()
print(suffix, target)
result = pow(target, suffix)
print(result)
io.sendline(result.encode())

with open("dump.txt", "r") as f:
    io.sendline(f.read().encode())

io.interactive()