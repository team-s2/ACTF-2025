from random import getrandbits
from secrets import randbelow
import numpy as np

load("poly.sage")

def sample_gaussian_poly(Q):
    q = Q.base_ring().cardinality()
    N = Q.degree()
    return polynomial(q, N, Q([getrandbits(4) for _ in range(Q.degree()//2)] + [-getrandbits(4) for _ in range(Q.degree()//2)]))

def sample_uniform_poly(Q):
    q = Q.base_ring().cardinality()
    N = Q.degree()
    return polynomial(q, N, Q([np.random.choice([-1, 1]) * randbelow(int(q//2)) for _ in range(Q.degree())]))

def sample_ternery_poly(Q):
    q = Q.base_ring().cardinality()
    N = Q.degree()
    return polynomial(q, N, Q([np.random.choice([-1, 0, 1]) for _ in range(Q.degree())]))
