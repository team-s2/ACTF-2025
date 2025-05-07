load("poly.sage")

def build_gadget(q, B):
    t = ceil(log(q, B))
    return [B^i for i in range(t)]

def gadget_decomposition(poly, B):
    q = poly.Q.base_ring().cardinality()
    N = poly.Q.degree()
    t = ceil(log(q, B))
    cur = poly.poly
    decomp_poly = []

    for i in range(t):
        coeffs = [ZZ(c) % B for c in cur.list()]
        gi = poly.Q(coeffs)
        decomp_poly.append(polynomial(q, N, gi))
        cur = poly.Q([ZZ(c) // B for c in (cur - gi).list()])

    return decomp_poly

def gadget_recomposition(gadget_poly, B):
    q = gadget_poly[0].Q.base_ring().cardinality()
    N = gadget_poly[0].Q.degree()
    t = ceil(log(q, B))
    poly = polynomial(q, N, "0")

    for i in range(t):
        poly +=  gadget_poly[i] * B^i

    return poly
