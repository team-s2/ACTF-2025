# unstoppable

## Underground

The idea of this challenge is the [busy beaver](https://en.wikipedia.org/wiki/Busy_beaver) challenge, and the number of BB(5) was proved in July 2024. You can see [this](https://github.com/ccz181078/Coq-BB5) for detail. In a netshell, for an 5-state, 2-color turing machine, the max number of steps before halting is 47176870.

This challenge asks us to find all stoppable VMs in the VMs given to us, and what you should do is to check whether they are stoppable.

## Solution 1

Just reverse the challenge, you will find two functions ollvmed, one with fla & bcf, the other with fla & bcf & sub.

However, you can simply use tools like [Hrtng](https://github.com/KasperskyLab/hrtng) to quickly deobfuscate the first function. As for the second function, you can also use tools to deobfuscate it, however, you can just skip this function, inputting the correct answer and get the flag.

To write a solve script, you can just dump all VMs, then use C++ & openmp to bruteforce it quickly.

```C++
#include <cstdio>
#include <vector>
#include <cstdint>
#include <omp.h>
#include "op.hpp" // VMs dumped -> uint8_t opcode[5005][30]

using namespace std;

int main()
{
    setvbuf(stdout, nullptr, _IONBF, 0);
    #pragma omp parallel for
    for (int i = 0; i < ALLN; i++)
    {
        vector<uint8_t> bit_vec(1024, 0);
        uint64_t now_op = 511;
        uint64_t now_count = 0;
        uint8_t now_state = 0;

        while (now_count < 47176870)
        {
            now_count++;
            uint8_t* operation = opcode[i] + 3 * ((now_state << 1) | (bit_vec[now_op] != 0));
            bit_vec[now_op] = operation[0];
            if (operation[1])
            {
                now_op++;
                if (now_op == bit_vec.size())
                {
                    bit_vec.insert(bit_vec.end(), bit_vec.size(), 0);
                }
            }
            else
            {
                if (now_op == 0)
                {
                    now_op += bit_vec.size();
                    bit_vec.insert(bit_vec.begin(), bit_vec.size(), 0);
                }
                now_op--;
            }
            now_state = operation[2];
            if (now_state == 25)
            {
                printf("%d ", i);
                break;
            }
        }
    }
    return 0;
}
```

## Solution 2

Of course, you don't need to actually reverse the whole challenge, you only need to notice that this challenge is "2703 stoppable numbers / 5005 all numbers".

Because of this, you can patch the original challenge and make sure that you can input one number each time and you can quickly exit this program if you input a stoppable number (if you skip the hash function, it will be faster).

I test this solution, writing a python script multiprocessing the patched challenge, setting a timeout threshold (you can also gradually increase it, and you should set threshold based on the compute capability of your computer).

```python
import subprocess
from multiprocessing import Pool

def test_number(n):
    proc = subprocess.Popen(
        ['./unstoppable_patched'],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    try:
        proc.communicate(input=f"{n}\n".encode(), timeout=40)

        return n
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return None
    except Exception as e:
        proc.kill()
        proc.communicate()
        raise e


if __name__ == '__main__':
    inputs = list(range(5005))

    with Pool() as pool:
        results = pool.map(test_number, inputs)

    successful_numbers = [n for n in results if n is not None]

    print("Successful inputs:", successful_numbers)
    print("number:", len(successful_numbers))
```