'Bracketing Closed f(x)=0'
def bisection(x0, x1, tol, maxit, f):
    f0 = f(x0)
    f1 = f(x1)
    iterations = 0
    success = False
    x2 = 0
    while iterations < maxit and abs(f0) > tol:
        x2 = (x0 + x1)/2
        f2 = f(x2)

        if abs(f2) < tol:
            success = True
            return x2, success
        if f0*f2 > 0:
            x0, f0 = x2, f2
        if f1*f2 > 0:
            x1, f1 = x2, f2
        iterations += 1
    return x2, success
