import math


def brentsopt(xl, xu, tol, f):
    hey = False
    phi = (1 + math.sqrt(5)) / 2
    rho = 2 - phi
    u = xl + rho * (xu - xl)
    v = u
    w = u
    x = u
    fu = f(u)
    fv = fu
    fw = fu
    fx = fu
    xm = 0.5 * (xl + xu)
    d = 0
    e = 0
    while abs(x - xm) >= tol:
        para = abs(e) > tol
        if para:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            s = 2 * (q - r)
            if s > 0:
                p = -p
            s = abs(s)
            para = abs(p) < abs(0.5 * s * e) and p > s * (xl - x) and p < s * (xu - x)
            if para:
                e = d
                d = p / s
        if not para:
            if x >= xm:
                e = xl - x
            else:
                e = xu - x
            d = rho * e
        u = x + d
        fu = f(u)
        if fu <= fx:
            if u >= x:
                xl = x
            else:
                xu = x
            v = w
            fv = fw
            w = x
            fw = fx
            x = u
            fx = fu
        else:
            if u < x:
                xl = u
            else:
                xu = u
            if fu <= fw or w == x:
                v = w
                fv = fw
                w = u
                fw = fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu
        xm = 0.5 * (xl + xu)

    return u  # where x is the solution
