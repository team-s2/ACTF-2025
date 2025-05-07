# tinyCKKS

## Category
Crypto
## Difficulty
Hard(intend solution)
## Solves
2
## Description
EE and ZZ. Isn’t it easy?
## writeups
题目背景是CKKS的已知明文攻击，由于CKKS方案把噪声当成明文的低位看待，从而能够支持浮点数近似运算，但这样会带来安全问题：假设密文是$(a,b=-as+\Delta*m+e)$，解密就是$(b+a*s)=\Delta*m+e$再$(b+a*s)/\Delta$，BFV方案这里是整除并取最近的整数，因此会round掉噪声，但是CKKS在这里是浮点数除法，噪声会带在明文里面，因此拿到解密的结果我们乘$\Delta$并取最近的整数得到$\Delta*m+e$，然后用密文的b减去就直接得到了$a*s$，$a$是知道的，直接求逆就得到了$s$。在题目里面提供了四种同态操作，随便执行一种就可以拿到一对明密文求出$sk$，再根据$sk$和$c=2$去求出每次使用的$e$，然后$e$是通过$getrandbits(4)$得到的，凑够数之后可以用MT19937预测后面使用的$e$，然后就直接打flag就行。N1STAR战队采用的方法和预期大概一致，不过参数没控制好导致明文和噪声差太多可以直接恢复，N0wayBack战队用了一种出乎意料的解法去攻击np.random伪随机数，根据每次选的$a$去判断np.choice的结果，然后恢复numpy里面的MT19937去推测np.uniform，从而绕过了$sk$的求解。预期的exp如下（其实如果看懂了整个过程预期解法还是不难的，而且还写了module_test帮助理解测试代码，标hard难度单纯是因为代码阅读量比较大）：
```python
load("poly.sage")
load("ckks.sage")

from pwn import context, process, remote
from MT19937 import *
import re

# context.log_level = "debug"

io = process(["sage", "main.sage"])
# io = remote("1.95.157.234", 9999)

def negacyclic_mat(x):
    q = x.q
    N = x.N
    M = matrix(Zmod(q), N, N)
    coeffs = x.poly.list()
    
    for i in range(N):
        for j in range(N):
            M[i, (i+j)%N] = coeffs[j] if i+j < N else -coeffs[j]

    return M

def get_sk(a, b):
    q = a.q
    N = a.N
    l = negacyclic_mat(a)
    r = vector(Zmod(q), b.poly.list())
    res = list(l.solve_left(r))

    return polynomial(q, N, res)

def parse_poly(poly):
    pattern = r"^(.*?) over Z\[X\]/\(X\^(\d+)\+1\) modulo (\d+)$"

    match = re.match(pattern, poly)
    if match:
        poly_str, N_str, q_str = match.groups()
        N = int(N_str)
        q = int(q_str)
        return polynomial(q, N, poly_str)
    else:
        raise TypeError("Parse failed!")

def parse_ct(ct):
    ct = ct[1:-1]
    a, b = ct.split(", ")
    a = parse_poly(a)
    b = parse_poly(b)

    return Ciphertext(a, b)

def construct_poly(q, N, poly):
    return f"{poly} over Z[X]/(X^{N}+1) modulo {q}"

def exp():
    N = 1024
    p = 947819
    B = 2
    L = 4
    q = p^(L+1)
    debug = False
    ckks = tinyCKKS(N, p, B, L, debug)

    io.recvuntil(b"ct: ")
    ct = parse_ct(io.recvline()[:-1].decode())
    io.recvuntil(b"Please give me c: ")
    io.sendline(b"1")
    io.recvuntil(b"Please choose operations you want to perform: ")
    io.sendline(b"1")
    io.recvuntil(b"ct: ")
    ct1 = parse_ct(io.recvline()[:-1].decode())
    ct = ckks.add(ct, ct1)
    ct_a, ct_b = ct.a, ct.b
    io.recvuntil(b"Please give me ct: \n")
    io.sendline(str(ct.a).encode())
    io.sendline(str(ct.b).encode())
    io.recvuntil(b"new_plain: ")
    plain = eval(io.recvline()[:-1].decode())
    pt = polynomial(q, N, [round(p*i) for i in plain])
    
    print("begin.....")
    sk = get_sk(ct_a, pt - ct_b)
    print("sk: ", sk)
    
    mt_use = []
    for i in range(5):
        io.recvuntil(b"ct: ")
        ct = parse_ct(io.recvline()[:-1].decode())
        ct_a, ct_b = ct.a, ct.b
        io.recvuntil(b"Please give me c: ")
        io.sendline(b"2")
        io.recvuntil(b"Here you are: \n")
        plain = eval(io.recvline()[:-1].decode())
        real_pt = polynomial(q, N, [round(p*i) for i in plain])
        error = ct_b + ct_a * sk - real_pt
        error = [i if i < 16 else q-i for i in error.poly.list()]
        mt_use += error
    
    assert len(mt_use) * N * 4 >= 624 * 32

    nbits = 4
    rng_clone = MT19937(state_from_data = (mt_use, nbits))

    for n in mt_use:
        assert n == rng_clone() >> (32-nbits), "Clone failed!"
        
    e = [rng_clone() >> (32-nbits) for _ in range(N//2)] + [-(rng_clone() >> (32-nbits)) for _ in range(N//2)]
    e = polynomial(q, N, e)

    io.recvuntil(b"ct: ")
    ct = parse_ct(io.recvline()[:-1].decode())
    ct_a, ct_b = ct.a, ct.b
    io.recvuntil(b"Please give me c: ")
    io.sendline(b"3")
    io.recvuntil(b"Do you know?\n")
    pt = ct_b + ct_a * sk - e
    io.sendline(str(pt).encode())
    print(io.recvall())
    
exp()
```