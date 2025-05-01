#!/usr/bin/python3
import os
import random
import string
import signal
import pathlib

BANNER = """
    
     _______  _______  ___     
    |   _   ||       ||   |    
    |  |_|  ||    ___||   |    
    |       ||   |___ |   |    
    |       ||    ___||   |___ 
    |   _   ||   |    |       |
    |__| |__||___|    |_______|
    
"""

SC_PATH = "/tmp/shellcode.bin"
DO_POW = True
DIFFICULTY_POW = 12
SCRIPT_DIR = pathlib.PosixPath(os.path.abspath(__file__)).parent


def is_valid(digest):
    zeros = "0" * DIFFICULTY_POW
    bits = "".join(bin(i)[2:].zfill(8) for i in digest)
    return bits[:DIFFICULTY_POW] == zeros


def proof_of_work():
    import hashlib

    random_prefix = "".join(random.choice(string.hexdigits) for _ in range(8))
    print(
        f"solve this: sha256({random_prefix} + ?) starts with prefix {DIFFICULTY_POW} zero bits",
        flush=True,
    )
    answer = input().strip()
    concat = random_prefix + answer
    if is_valid(hashlib.sha256(concat.encode()).digest()):
        return
    else:
        print("proof-of-work fails", flush=True)
        exit(0)


def recv_shellcode() -> bytes:
    result = b""
    try:
        while True:
            print("> ", flush=True)
            line_content = input().strip()
            if not line_content:
                break
            result += bytes.fromhex(line_content)
    except Exception as err:
        print("Bad input format", flush=True)
        exit(-1)

    print(f"receive in total {len(result)} bytes, move on ...")
    return result


def main() -> None:
    if DO_POW:
        proof_of_work()

    print(BANNER, flush=True)
    print("welcome to this challenge !!!", flush=True)
    print("we will run awesome AFL to fuzz your input program ~~~\n", flush=True)
    print("so, upload your program (in hex encoding)", flush=True)
    sc = recv_shellcode()
    open(SC_PATH, "wb").write(sc)
    print(f"save your program at {SC_PATH}", flush=True)
    os.system(
        f"timeout 5m {SCRIPT_DIR}/afl-fuzz -i {SCRIPT_DIR}/input -o {SCRIPT_DIR}/output -- {SCRIPT_DIR}/harness"
    )
    print("awesome, see you next time :)))", flush=True)
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, lambda _: exit(-1))
    signal.alarm(10 * 60)
    main()
