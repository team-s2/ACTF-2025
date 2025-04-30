## **解题思路**
+ 题目主要实现了迭代幂次的计算，根据欧拉定理可以不断套欧拉函数快速计算结果（我们认为这是一个考察点，因此不提供`tetration`函数，但提供了选项四便于测试）,基于此可以自行实现`tetration`函数。
    $$ g^{g^{g^{...^{g^x}}}} \equiv g^{g^{g^{...^{g^{x \mod \phi^{t+1}(P)} \mod \phi^{t}(P)} ... } \mod \phi^2(P)} \mod \phi(P)} \pmod {P} $$
    ```python
    def getPhiLis(P):
        philis = []
        phi = P
        while phi!=1:
            philis.append(phi)
            phi = totient(phi)
            # print(factorint(phi))
        return philis

    def tetration(g, times, x, philis):
        if times>len(philis):
            return tetration(g, len(philis), 0, philis)
        res = x
        for i in range(times-1,-1,-1):
            res = pow(g, res, philis[i])
        return res
    ```
+ 容易发现在迭代 t 次后若有 $\phi^{t-1}(P)=2$ ，则 $\phi^{t}(P)=1$，因此迭代幂次次数为 t 次或更高次后，结果恒为某个固定的值。
+ 假设对于每一层而言 g 都是 $Zmod(\phi^{k}(P))$ 的原根，则在迭代 t-1 次时便可遍历 $\phi^{t-1}(P)$ 种情况得到 $x\%\phi^{t-1}(P)$ 的值。逐步递减迭代次数，在迭代 k 次可遍历 $\phi^{k}(P) // \phi^{k+1}(P)$ 种情况在已知 $x\%\phi^{k+1}(P)$ 的情况下得到 $x\%\phi^{k}(P)$ 的值来恢复 x （要求 $\phi^{k}(P) \% \phi^{k+1}(P) =0$）
+ 实际上，我们难以做到使得对于每一层而言 g 都是原根，但只要满足大部分层数满足原根条件，可以在较高层保持这种性质，并且得到的 x 的长度与 P 大致相当。因此题目本意是在提供的众多 P 中找到恰当的 P 使得其满足上述条件（事实上只有一个），然后通过上述方法恢复 x 即可。

## **参考代码**
```python
from pwn import *
import re
from sympy import totient, factorint
from tqdm import trange
from Crypto.Util.number import long_to_bytes, bytes_to_long

context.log_level = "critical"

g = 5
def interative(targetP, times):
    p = 0
    while 1:
        io = process(["python","main.py"])
        # io = remote("1.95.137.123",9999)
        io.recvuntil(b"What do you do? ")
        io.sendline(b"1")
        p = int(re.findall("\d+",io.recvline().decode("utf-8"))[0])
        if p==targetP:
            break
        io.close()

    io.recvuntil(b"What do you do? ")
    io.sendline(b"2")
    io.sendlineafter(b"You decide to pick your own lucky number: ",str(g).encode())
    assert io.recvline() == b"You successfully pick your lucky number.\n"

    io.recvuntil(b"What do you do? ")
    io.sendline(b"3")
    io.sendlineafter(b"You decide to pick your bet size: ",str(times).encode())
    res = int(re.findall("\d+",io.recvline().decode("utf-8"))[0])
    io.close()

    return res

def getPhiLis(P):
    philis = []
    phi = P
    while phi!=1:
        philis.append(phi)
        phi = totient(phi)
        # print(factorint(phi))
    return philis

def tetration(g, times, x, philis):
    if times>len(philis):
        return tetration(g, len(philis), 0, philis)
    res = x
    for i in range(times-1,-1,-1):
        res = pow(g, res, philis[i])
    return res

p = 670144747631070976739015819027954827310379693667090873445520193836663869580245599076670148076473491050020123654751096623483807617465722698994356143777563707
philis = getPhiLis(p)
# print(getPhiLis(5))
# print(tetration(3, len(getPhiLis(5))-1, 0, getPhiLis(5))==tetration(3, len(getPhiLis(5))-1, 1, getPhiLis(5)))
idx = len(philis)-7
print(idx)
assert tetration(g, idx, 0, philis)!=tetration(g, idx, 1, philis)
assert tetration(g, idx, 0, philis)==tetration(g, idx, 2, philis)

res = 0
base = 2
t = interative(p, idx)
for i in range(base):
    if tetration(g, idx, i, philis) == t:
        res = i
        print(f"x mod {base}: ", res)
        break

step = 5
for i in trange(idx-step,1,-step):
    assert philis[i]%philis[i+step]==0
    t = interative(p, i)
    for j in range(philis[i]//philis[i+step]):
        if tetration(g, i, res+j*base, philis) == t:
            res = res+j*base
            base *= philis[i]//philis[i+step]
            # print(f"x mod {base}: ", res)
            # print(x%base)
            break
    else:
        exit()

# not enough
t = interative(p, 1)
for k in range(p//base):
    if tetration(g, 1, res+k*base, philis) == t:
        res = res+k*base
        break

print(long_to_bytes(res))
```

## **彩蛋**
+ 详见 http://www.wuy4n.com/2025/04/30/ACTF2025/