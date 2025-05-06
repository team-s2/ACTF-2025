exec timeout 300 qemu-system-x86_64  \
-m 512M  \
-smp 1 \
-kernel ./bzImage    \
-append "console=ttyS0 quiet kaslr sysctl.kernel.io_uring_disabled=1"     \
-initrd rootfs.cpio \
-nographic  \
-net nic,model=e1000 \
-no-reboot \
-monitor /dev/null 


