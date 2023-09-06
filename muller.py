import math
def mullers(xr, h, tolerance, maxit, f):
    success = False
    x2 = xr
    x1 = xr + h * xr
    x0 = xr - h * xr
    iterations = 0
    while iterations < maxit:
        iterations += 1
        h0 = x1 - x0
        h1 = x2 - x1
        d0 = (f(x1) - f(x0)) / h0
        d1 = (f(x2) - f(x1)) / h1
        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = f(x2)
        rad = math.sqrt(b * b - 4 * a * c)
        if abs(b + rad) > abs(b - rad):
            den = b + rad
        else:
            den = b - rad
        dxr = -2 * c / den
        xr = x2 + dxr
        if abs(dxr) <= abs(tolerance):
            success = True
            return xr, success
        x0 = x1
        x1 = x2
        x2 = xr
    return xr, success