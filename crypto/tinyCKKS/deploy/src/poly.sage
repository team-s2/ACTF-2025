def std_form(c, q):
    half_q = q // 2
    return c if c < half_q else c - q

class polynomial:
    def __init__(self, q, N, poly):
        self.q = q
        self.N = N
        P.<X> = PolynomialRing(Zmod(q))
        Q.<X> = P.quotient(X^N+1)
        self.Q = Q
        self.poly = self.Q(poly)

    def check_parameter(self, other):
        assert self.N == other.N
        assert self.q % other.q == 0

    def __add__(self, other):
        if isinstance(other, (int, Integer)):
            return polynomial(self.q, self.N, self.Q(self.poly + other))
        elif isinstance(other, polynomial):
            if self.q < other.q:
                other.check_parameter(self)
                poly = self.Q([ZZ(c) % self.q for c in other.poly.list()])
                return polynomial(self.q, self.N, self.Q(self.poly + poly))
            else:
                self.check_parameter(other)
                poly = other.Q([ZZ(c) % other.q for c in self.poly.list()])
                return polynomial(other.q, other.N, other.Q(poly + other.poly))
        else:
            raise TypeError("Type not support")

    def __sub__(self, other):
        if isinstance(other, (int, Integer)):
            return polynomial(self.q, self.N, self.Q(self.poly - other))
        elif isinstance(other, polynomial):
            if self.q < other.q:
                other.check_parameter(self)
                poly = self.Q([ZZ(c) % self.q for c in other.poly.list()])
                return polynomial(self.q, self.N, self.Q(self.poly - poly))
            else:
                self.check_parameter(other)
                poly = other.Q([ZZ(c) % other.q for c in self.poly.list()])
                return polynomial(other.q, other.N, other.Q(poly - other.poly))
        else:
            raise TypeError("Type not support")

    def __mul__(self, other):
        if isinstance(other, (int, Integer)):
            return polynomial(self.q, self.N, self.Q(self.poly * other))
        elif isinstance(other, polynomial):
            if self.q < other.q:
                other.check_parameter(self)
                poly = self.Q([ZZ(c) % self.q for c in other.poly.list()])
                return polynomial(self.q, self.N, self.Q(self.poly * poly))
            else:
                self.check_parameter(other)
                poly = other.Q([ZZ(c) % other.q for c in self.poly.list()])
                return polynomial(other.q, other.N, other.Q(poly * other.poly))
        else:
            raise TypeError("Type not support")

    def __floordiv__(self, other):
        if isinstance(other, (int, Integer)):
            coeffs = [round(std_form(ZZ(c), self.q) / other) for c in self.poly.list()]
            return polynomial(self.q // other, self.N, coeffs)
        else:
            raise TypeError("Type not support")

    def __repr__(self):
        return f"{str(self.poly)} over Z[X]/(X^{self.N}+1) modulo {self.q}"

    def __eq__(self, other):
        return self.Q == other.Q and self.poly == other.poly

    def mapping(self, t):
        coeffs = self.poly.list()
        res = [0 for i in range(self.N)]

        for i in range(self.N):
            tmp = (i * t) % (2 * self.N)
            neg = tmp >= self.N
            tmp -= neg * self.N
            res[tmp] = coeffs[i] if neg == 0 else -coeffs[i]
        
        return polynomial(self.q, self.N, self.Q(res))
