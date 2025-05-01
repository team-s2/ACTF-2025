# Writeup - AFL sandbox

This challenge uses [AFL](https://github.com/google/AFL/tree/master) fuzzer to fuzz player-provided shellcode, with extra imposed seccomp jail, hoping that the being fuzzed code can escape the fuzzing and leak the flag.

In a nutshell, the shellcode need to steal the flag under below conditions (see source code in harness.c):

- stdin is redirect, stdout and stderr is "closed".
    - https://github.com/google/AFL/blob/master/afl-fuzz.c#L2067
- use only "open", "read", "write", "exit", "exit_group", "brk", "shmat" syscalls.

## Intended Solution

As you can already see the *shmat* syscall, it is seldom used in any CTF pwning challenge.

That is, the player should implement the AFL forkserver logic and transmit *fake coverage* to let the parent fuzzer output what the flag is. See `example.c` as a demo.

> By the way, rather than the coverage, side-channel via CRASH is also doable. Just get clear what the AFL and the forkserver speak using 198 and 199 file descriptors.

## Unintended Solution

Using a timeout side channel can be much easier without implementing any forkserver code.

In addition, thanks to the @N0WayBack team, you can just use `write` syscall to fake a `random.py` and achieve a straightforward RCE to get the flag >_<, what a stupid environment and privilege management.

## Besides

After checking the writeups, I found that most of players are directly using assembly to finish the shellcode. Please checkout the [example.c](./example.c) and the [linker script](./custom_linker.ld) that help you develop quick C based shellcode.