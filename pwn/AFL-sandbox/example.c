//
// example shellcode simply setup AFL forksrv to avoid dying ...
// wrap everything into one function
// gcc -Wall -nostdlib -Wl,-T,custom_linker.ld -o example example.c
// objcopy -O binary --only-section=.text example shellcode.bin
//
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <syscall.h>

#define MAP_SIZE (1 << 16)

/* inline helpers */
static inline void my_memset(void *s, uint8_t c, size_t n)
{
    for (size_t i = 0; i < n; i++)
    {
        ((uint8_t *)s)[i] = c;
    }
}

static inline int my_strcmp(const char *s1, const char *s2)
{
    while (*s1 && (*s1 == *s2))
    {
        s1++;
        s2++;
    }
    return *(unsigned char *)s1 - *(unsigned char *)s2;
}

static inline int my_strncmp(const char *str1, const char *str2, size_t n)
{
    // Compare up to n characters
    while (n > 0 && *str1 && (*str1 == *str2))
    {
        str1++;
        str2++;
        n--;
    }

    // If n is 0, the strings are equal up to the first n characters
    if (n == 0)
    {
        return 0;
    }

    // Return the difference between the characters at the current position
    return *(unsigned char *)str1 - *(unsigned char *)str2;
}

static inline size_t my_strlen(const char *s)
{
    size_t i;
    for (i = 0; s[i]; i++)
    {
    }
    return i;
}

static inline char *my_getenv(const char *name, char **environ)
{
    size_t len = my_strlen(name);
    for (char **env = environ; *env != NULL; env++)
    {
        if (my_strncmp(*env, name, len) == 0 && (*env)[len] == '=')
        {
            return &(*env)[len + 1];
        }
    }
    return NULL;
}

static inline int my_atoi(const char *str)
{
    int result = 0;

    while (*str >= '0' && *str <= '9')
    {
        result = result * 10 + (*str - '0');
        str++;
    }

    return result;
}

static inline long my_syscall3(long sysno, long arg1, long arg2, long arg3)
{
    long result;
    __asm__ volatile(
        "mov %1, %%rax\n"
        "mov %2, %%rdi\n"
        "mov %3, %%rsi\n"
        "mov %4, %%rdx\n"
        "syscall\n"
        "mov %%rax, %0"
        : "=r"(result)
        : "r"(sysno), "r"(arg1), "r"(arg2), "r"(arg3)
        : "%rax", "%rdi", "%rsi", "%rdx");

    return result;
}

static inline void *my_shmat(int shmid, const void *shmaddr, int shmflg)
{
    return (void *)my_syscall3(SYS_shmat, (long)shmid, (long)shmaddr, (long)shmflg);
}

/* any BSS datas */
char shmid[16];

static inline void setup_bss()
{
    // __AFL_SHM_ID
    shmid[0] = '_';
    shmid[1] = '_';
    shmid[2] = 'A';
    shmid[3] = 'F';
    shmid[4] = 'L';
    shmid[5] = '_';
    shmid[6] = 'S';
    shmid[7] = 'H';
    shmid[8] = 'M';
    shmid[9] = '_';
    shmid[10] = 'I';
    shmid[11] = 'D';

    // ...
}

__attribute__((section(".text.main"))) void entry(int argc, char **argv, char **env)
{
    // 0. setup bss
    setup_bss();

    // 1. Get getenv("__AFL_SHM_ID");
    // XXX: what if this value is constant via each call ...
    const char *afl_shm_id_str = my_getenv(shmid, env);
    if (afl_shm_id_str == NULL)
        return;

    // 2. Wrap the shared memory (coverage)
    int afl_shm_id = my_atoi(afl_shm_id_str);
    uint8_t *afl_area_ptr = my_shmat(afl_shm_id, NULL, 0);

    // 3. simulate the fuzzing loop
    // 3.1 welcome
    uint32_t tmp = 0;
    if (my_syscall3(SYS_write, 198 + 1, (long)(&tmp), 4) != 4)
        return;

    // 3.2 loop
    while (1)
    {
        // cycle
        uint32_t child_pid = 99;
        uint32_t was_killed = -1;
        int r = my_syscall3(SYS_read, 198, (long)(&was_killed), 4);
        if (r != 4)
        {
            return;
        }
        // XXX: should fork here
        r = my_syscall3(SYS_write, 198 + 1, (long)(&child_pid), 4);
        if (r != 4)
        {
            return;
        }

        char stack_buffer[512 * 1024];
        my_memset(stack_buffer, 0, 32);
        /* int buf_len = */ my_syscall3(SYS_read, 0, (long)stack_buffer, sizeof(stack_buffer));

        // coverage logic
        for (int i = 0; i < 0x10000; i++)
        {
            afl_area_ptr[i % MAP_SIZE] += 1;
        }

        // update status
        uint32_t no_crash = 0;
        r = my_syscall3(SYS_write, 198 + 1, (long)(&no_crash), 4);
        if (r != 4)
        {
            return;
        }
    }

    return;
}