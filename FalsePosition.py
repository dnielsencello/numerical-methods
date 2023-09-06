'bracketing closed f(x)=0'
def false_position(x0, x1, tol, maxit, f):
    f0 = f(x0)
    f1 = f(x1)
    i0 = 0
    i1 = 0
    x2 = 0
    f2 = 100
    iterations = 0
    
    success = False

    while iterations < maxit and abs(f2) > tol:
        x2 = x1 - f1 * (x0 - x1) / (f0 - f1)
        f2 = f(x2)
        if f2 * f0 > 0:
            f0 = f2
            x0 = x2
            i0 += 1
            i1 = 0
            if i0 > 1:
                f1 = f1 / 2
        else:
            f1 = f2
            x1 = x2
            i1 += 1
            i0 = 0
            if i1 > 1:
                f0 = f0 / 2
        if abs(f2) < tol:
            success = True
            return x2, success
        iterations += 1
    return x2, success
