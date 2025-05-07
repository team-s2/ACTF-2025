import random

load("ckks.sage")
load("gadget.sage")
load("poly.sage")
load("distribution.sage")

def gadget_test():
    N = 4
    q = 23
    B = 3

    poly = "19 + 13*X + 14*X^2 + 17*X^3"
    poly = polynomial(q, N, poly)

    gadget_poly = gadget_decomposition(poly, B)
    assert poly == gadget_recomposition(gadget_poly, B)

def poly_test():
    N = 4
    q = 23

    p1 = "1 + 2*X + 3*X^2 + 4*X^3"
    p1 = polynomial(q, N, p1)

    p2 = "4 + 3*X + 2*X^2 + 1*X^3"
    p2 = polynomial(q, N, p2)

    assert str(p1) == "4*X^3 + 3*X^2 + 2*X + 1 over Z[X]/(X^4+1) modulo 23"
    assert str(p2) == "X^3 + 2*X^2 + 3*X + 4 over Z[X]/(X^4+1) modulo 23"
    assert str(p1 + 10) == "4*X^3 + 3*X^2 + 2*X + 11 over Z[X]/(X^4+1) modulo 23"
    assert str(p1 + p2) == "5*X^3 + 5*X^2 + 5*X + 5 over Z[X]/(X^4+1) modulo 23"
    assert str(p1 - 10) == "4*X^3 + 3*X^2 + 2*X + 14 over Z[X]/(X^4+1) modulo 23"
    assert str(p1 - p2) == "3*X^3 + X^2 + 22*X + 20 over Z[X]/(X^4+1) modulo 23"
    assert str(p1 * 7) == "5*X^3 + 21*X^2 + 14*X + 7 over Z[X]/(X^4+1) modulo 23"
    assert str(p1 * p2) == "7*X^3 + 16*X^2 + 7 over Z[X]/(X^4+1) modulo 23"
    assert str(p1.mapping(3)) == "2*X^3 + 20*X^2 + 4*X + 1 over Z[X]/(X^4+1) modulo 23"

def ckks_test():
    N = 32
    p = 947819
    B = 2^8
    L = 3

    debug = True

    ckks = tinyCKKS(N, p, B, L, debug)

    # plain1 = [1.2345, 2.3456, 3.4567, 4.5678]
    # plain2 = plain1[::-1]
    plain1 = [round(random.uniform(0, 100), 4) for _ in range(N)]
    plain2 = [round(random.uniform(0, 100), 4) for _ in range(N)]

    print("Plaintext:")
    print(f"pt1(origin): {plain1}")
    print(f"pt2(origin): {plain2}")

    # Test Encoding / Decoding

    pt1 = ckks.encode(plain1)
    pt2 = ckks.encode(plain2)

    print("Test Encoding and Decoding:")
    print(f"pt1(decoded): {ckks.decode(pt1)}")
    print(f"pt2(decoded): {ckks.decode(pt2)}")

    # Test Encrypt / Decrypt

    ct1 = ckks.encrypt(pt1)
    ct2 = ckks.encrypt(pt2)

    print("Test Encrypt and Decrypt:")
    print(f"pt1(decrypted and decoded): {ckks.decode(ckks.decrypt(ct1))}")
    print(f"pt2(decrypted and decoded): {ckks.decode(ckks.decrypt(ct2))}")

    # Test Operations
    print("Test Operations:")
    
    ct_add = ckks.add(ct1, ct2)

    print("Test Addition:")
    print(f"pt(added): {[plain1[i]+plain2[i] for i in range(N)]}")
    print(f"pt(encrypted and added): {ckks.decode(ckks.decrypt(ct_add))}")

    ct_mul = ckks.multiply(ct1, ct2)
    ct_mul_rescaled = ckks.rescale(ct_mul)

    print("Test Multiplication:")
    print(f"pt1 * pt2(decoded and rescaled): {ckks.decode((pt1 * pt2) // ckks.delta)}")
    print(f"pt1 * pt2(decrypted and decoded): {ckks.decode(ckks.decrypt(ct_mul_rescaled))}")

    # Reset
    ckks.reset()

    new_sk = sample_ternery_poly(ckks.Q)
    ksk = ckks.gen_ksk(new_sk)
    ct1_switched = ckks.key_switch(ct1, ksk)
    ct2_switched = ckks.key_switch(ct2, ksk)

    print("Test Key Switching:")
    test = ckks.decrypt(ct1_switched, new_sk)
    print(f"pt1(key switched and decrypted): {ckks.decode(ckks.decrypt(ct1_switched, new_sk))}")
    print(f"pt2(key switched and decrypted): {ckks.decode(ckks.decrypt(ct2_switched, new_sk))}")

    t = 3
    pt1_galois = pt1.mapping(t)
    galois_key = ckks.gen_galois_key(t)
    ct1_galois = ckks.apply_galois(ct1, t, galois_key)

    print("Test Galois:")
    print(f"pt1(mapping): {pt1_galois}")
    print(f"pt1(encrypted and mapping): {ckks.decrypt(ct1_galois)}")

if __name__ == "__main__":
    gadget_test()
    poly_test()
    ckks_test()