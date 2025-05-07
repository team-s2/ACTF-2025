import random
import re
import os
load("ckks.sage")

flag = os.getenv('FLAG')

def recv_poly():
    pattern = r"^(.*?) over Z\[X\]/\(X\^(\d+)\+1\) modulo (\d+)$"

    poly = input("")
    match = re.match(pattern, poly)
    if match:
        poly_str, N_str, q_str = match.groups()
        N = int(N_str)
        q = int(q_str)
        return polynomial(q, N, poly_str)
    else:
        raise TypeError("Input is not a valid polynomial")

def send_ct(ct):
    print(ct)

def recv_ct():
    a = recv_poly()
    b = recv_poly()

    return Ciphertext(a, b)

def send_key(key):
    for i in range(len(key)):
        send_ct(key[i])

def main():
    print("Welcome to ACTF 2025!")
    print("Here is a tiny implementation of CKKS scheme.")
    print("You can test by running module_test.sage.")
    print("Now let's start the challenge.")

    N = 1024
    p = 947819
    B = 2
    L = 4

    r = 10
    precision = 4

    debug = False

    ckks = tinyCKKS(N, p, B, L, debug)

    for _ in range(7):
        plain = [round(np.random.uniform(0, r), precision) for _ in range(N)]
        pt = ckks.encode(plain)
        ct = ckks.encrypt(pt)
        target_pt = pt

        send_ct(ct)

        c = int(input("Please give me c: "))

        if c == 1:
            ccc = int(input("Please choose operations you want to perform: "))
            assert 0 <= ccc <= 4

            if ccc == 1:
                print("Addition")
                plain1 = [round(np.random.uniform(0, r), precision) for _ in range(N)]
                pt1 = ckks.encode(plain1)
                ct1 = ckks.encrypt(pt1)
                send_ct(ct1)
                target_pt += pt1
            if ccc == 2:
                print("Multiplication")
                plain1 = [round(np.random.uniform(0, r), precision) for _ in range(N)]
                pt1 = ckks.encode(plain1)
                ct1 = ckks.encrypt(pt1)
                send_ct(ct1)
                print("relin_key: ")
                send_key(ckks.relin_key)
                target_pt *= pt1
                target_pt //= ckks.delta
            if ccc == 3:
                print("Key Switching")
                new_sk = sample_ternery_poly(ckks.Q)
                ksk = ckks.gen_ksk(new_sk)
                send_key(ksk)
                target_pt = pt
            if ccc == 4:
                print("Galois")
                t = int(input("Please choose galois parameter:")) % (2 * ckks.N)
                assert t % 2 == 1
                galois_key = ckks.gen_galois_key(t)
                send_key(galois_key)
                target_pt = target_pt.mapping(t)

            print("Please give me ct: ")
            ct = recv_ct()

            if ccc == 3:
                pt_decrypt = ckks.decrypt(ct, new_sk)
            else:
                pt_decrypt = ckks.decrypt(ct)

            new_plain = ckks.decode(pt_decrypt)
            target_plain = ckks.decode(target_pt)
            assert all([abs(target_plain[i] - new_plain[i]) <= 0.5 for i in range(ckks.N)])

            print("new_plain: ", new_plain)

            if ccc == 2:
                ckks.reset()
        elif c == 2:
            print("Here you are: ")
            origin_plain = ckks.decode(target_pt)
            print(origin_plain)
        elif c == 3:
            print("Do you know?")
            your_plain = recv_poly()
            if your_plain == target_pt:
                print(flag)
        else:
            print("Bye...")
            break
    

if __name__ == "__main__":
    main()

    

