// gcc harness.c -Wall -o harness -lseccomp -pie -Wl,-z,relro -Wl,-z,now
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#include <unistd.h>
#include <seccomp.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>

#define SHELLCODE_TEXT_ADDR_CONST (0x10000)
#define SHELLCODE_DATA_ADDR_CONST (0x20000)
#define SHELLCODE_PATH "/tmp/shellcode.bin"

char shm_id[] = "__AFL_SHM_ID";
char todo[] = "support libasan.so in the future";
void *shellcode_addr;

int setup()
{
    int err;

    // turn off bufferring
    err = setvbuf(stdin, NULL, _IONBF, 0);
    err = setvbuf(stdout, NULL, _IONBF, 0);
    err = setvbuf(stderr, NULL, _IONBF, 0);
    if (err < 0)
        return err;

    // prepare dest shellcode
    int fd = open(SHELLCODE_PATH, O_RDONLY);
    if (fd < 0)
        return fd;

    shellcode_addr = mmap((void *)SHELLCODE_TEXT_ADDR_CONST, 0x1000, PROT_EXEC | PROT_READ, MAP_PRIVATE | MAP_FIXED, fd, 0x0);
    if (shellcode_addr == MAP_FAILED)
    {
#ifdef DEBUG
        perror("mmap");
#endif
        return -1;
    }

#ifdef DEBUG
    printf("[DEBUG] shellcode mapped at %p\n", shellcode_addr);
#endif

    void *shellcode_data = mmap((void *)SHELLCODE_DATA_ADDR_CONST, 0x1000, PROT_WRITE | PROT_READ, MAP_PRIVATE | MAP_FIXED | MAP_ANON, -1, 0x0);
    if (shellcode_data == MAP_FAILED)
    {
#ifdef DEBUG
        perror("mmap");
#endif
        return -1;
    }

    // setup seccomp
    static const int allowed[] = {
        SCMP_SYS(open),
        SCMP_SYS(read),
        SCMP_SYS(write),
        SCMP_SYS(exit),
        SCMP_SYS(exit_group),
        SCMP_SYS(brk),
        SCMP_SYS(shmat),
    };

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL)
    {
        return -1;
    }
    for (int i = 0; i < sizeof(allowed) / sizeof(allowed[0]); i++)
    {
        err = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, allowed[i], 0);
        if (err < 0)
            return err;
    }
    err = seccomp_load(ctx);
    if (err < 0)
    {
        return err;
    }
    seccomp_release(ctx);
    return 0;
}

int main(int argc, char *argv[], char *env[])
{
    int err;
    err = setup();

    if (err)
    {
#ifdef DEBUG
        printf("[DEBUG] setup failed with err = %d\n", err);
#endif
        exit(-1);
    }

    void (*fptr)(int, char **, char **) = shellcode_addr;
    fptr(argc, argv, env);

    exit(0);
}
