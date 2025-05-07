load("distribution.sage")
load("ciphertext.sage")
load("gadget.sage")

class tinyCKKS:
    def __init__(self, N, p, B, L, debug):
        self.N = N
        self.p = p
        self.B = B
        self.L = L
        self.q = p^(L+1)
        P.<X> = PolynomialRing(Zmod(self.q))
        Q.<X> = P.quotient(X^N+1)
        self.Q = Q
        self.delta = p
        self.debug = debug
        self.t = ceil(log(self.q, self.B))
        self.gadget = build_gadget(self.q, self.B)
        self.gen_sk()
        self.gen_relin_key()

    def gen_sk(self):
        self.sk = sample_ternery_poly(self.Q)

    def gen_ksk(self, new_sk):
        ksk = []

        for i in range(self.t):
            if self.debug:
                e = polynomial(self.q, self.N, "0")
            else:
                e = sample_gaussian_poly(self.Q)
            a = sample_uniform_poly(self.Q)
            b = self.sk * self.gadget[i] - (a * new_sk + e)
            ksk.append(Ciphertext(a, b))

        return ksk

    def gen_galois_key(self, t):
        mapping_sk = self.sk.mapping(t)
        new_sk = self.sk
        self.sk = mapping_sk
        galois_key = self.gen_ksk(new_sk)
        self.sk = new_sk

        return galois_key

    def gen_relin_key(self):
        relin_key = []

        for i in range(self.t):
            if self.debug:
                e = polynomial(self.q, self.N, "0")
            else:
                e = sample_gaussian_poly(self.Q)
            a = sample_uniform_poly(self.Q)
            b = self.sk * self.sk * self.gadget[i] - (a * self.sk + e)
            relin_key.append(Ciphertext(a, b))

        self.relin_key = relin_key

    # For simplicity, we don't use Vanilla Encoding
    def encode(self, coeffs):
        poly = [round(coeffs[i] * self.delta) for i in range(len(coeffs))]
        poly = polynomial(self.q, self.N, poly)
        return poly

    def decode(self, pt):
        coeffs = [float(std_form(ZZ(c), self.q) / self.delta) for c in pt.poly.list()]
        return coeffs

    def encrypt(self, pt):
        if self.debug:
            e = polynomial(self.q, self.N, "0")
        else:
            e = sample_gaussian_poly(self.Q)
        ct0 = sample_uniform_poly(self.Q)
        ct1 = pt + e - ct0 * self.sk
        return Ciphertext(ct0, ct1)

    def decrypt(self, ct, sk = None):
        ct0, ct1 = ct.a, ct.b
        if sk:
            return ct1 + ct0 * sk
        else:
            return ct1 + ct0 * self.sk

    def add(self, ct1, ct2):
        return ct1 + ct2

    def sub(self, ct1, ct2):
        return ct1 - ct2

    def multiply(self, ct1, ct2):
        if isinstance(ct1, Ciphertext) and isinstance(ct2, polynomial):
            return ct1 * ct2
        elif isinstance(ct1, Ciphertext) and isinstance(ct2, Ciphertext):
            expand_ct = ct1 * ct2
            return self.relin(expand_ct, self.relin_key)
        else:
            raise TypeError("Type not support")

    def key_switch(self, ct, ksk):
        a, b = ct.a, ct.b
        decomp_a = gadget_decomposition(a, self.B)

        a1 = polynomial(self.q, self.N, "0")
        b1 = b

        assert len(ksk) == self.t

        for i in range(self.t):
            a1 += ksk[i].a * decomp_a[i]
            b1 += ksk[i].b * decomp_a[i]

        return Ciphertext(a1, b1)

    def apply_galois(self, ct, t, galois_key):
        mapping_ct = Ciphertext(ct.a.mapping(t), ct.b.mapping(t))
        return self.key_switch(mapping_ct, galois_key)

    def relin(self, expand_ct, relin_key):
        d0, d1, d2 = expand_ct
        decomp_d0 = gadget_decomposition(d0, self.B)
        a = d1
        b = d2

        for i in range(self.t):
            a += self.relin_key[i].a * decomp_d0[i]
            b += self.relin_key[i].b * decomp_d0[i]

        return Ciphertext(a, b)

    def rescale(self, ct):
        ct = ct // self.delta
        self.L -= 1
        self.q = self.q // self.delta

        return ct

    def reset(self):
        self.L += 1
        self.q = self.q * self.delta

