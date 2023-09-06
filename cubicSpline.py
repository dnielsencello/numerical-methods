# take the second derivative of a function, the first and last second derivative are always 0, if you solve for the remaining second derivative,
# to interpolate you are going to integrate to get the y value
# indexing is the same with psuedocode
# ranges start at 2 index all my f,g,r subtract 1, e -2
def interpolate(x, y, d2x, xu):
    flag = 0
    n = len(x)
    i = 1
    success = True
    while i != n + 1 and flag != 1:
        if xu >= x[i - 1] and xu <= x[i]:
            c1 = d2x[i - 1] / 6 / (x[i] - x[i - 1])
            c2 = d2x[i] / 6 / (x[i] - x[i - 1])
            c3 = y[i - 1] / (x[i] - x[i - 1]) - d2x[i - 1] * (x[i] - x[i - 1]) / 6
            c4 = y[i] / (x[i] - x[i - 1]) - d2x[i] * (x[i] - x[i - 1]) / 6
            t1 = c1 * ((x[i] - xu) ** 3)
            t2 = c2 * ((xu - x[i - 1]) ** 3)
            t3 = c3 * (x[i] - xu)
            t4 = c4 * (xu - x[i - 1])
            yu = t1 + t2 + t3 + t4
            t1 = -3 * c1 * ((xu - x[i - 1]) ** 2)
            t2 = 3 * c2 * ((xu - x[i - 1]) ** 2)
            t3 = -c3
            t4 = c4
            dy = t1 + t2 + t3 + t4
            t1 = 6 * c1 * (xu - x[i - 1])
            t2 = 6 * c2 * (xu - x[i - 1])
            d2y = t1 + t2
            flag = 1
        else:
            i = i + 1
        success = True
    if flag == 0:
        print("Outside Range")
    return (yu, success)


def cubic_spline(x, y):
    n = len(x)
    e, f, g, r, originalx = [0] * n, [0] * n, [0] * n, [0] * n, [0]*n
    for i in range(len(x)):
        originalx[i] = x[i]
    tridiag(originalx, y, n, e, f, g, r)
    d2x = thomasAlgorithm(e, f, g, r, n, originalx)
    return d2x

def tridiag(x, y, n, e, f, g, r):
    # ri = ei*y"i-1+fi*y"+gi*y"
    for i in range(1, n - 1):
        if i > 1:
            e[i] = (x[i] - x[i - 1])
        f[i] = 2 * (x[i + 1] - x[i - 1])
        if i < n - 1:
            g[i] = (x[i + 1] - x[i])
        r[i] = 6 / (x[i + 1] - x[i]) * (y[i + 1] - y[i])
        r[i] = r[i] + 6 / (x[i] - x[i - 1]) * (y[i - 1] - y[i])
    return


def thomasAlgorithm(e, f, g, r, n, originalx):
    d2x = originalx
    for k in range(2, n):
        e[k] = e[k] / f[k - 1]
        f[k] = f[k] - e[k] * g[k - 1]
    for k in range(2, n):
        r[k] = r[k] - e[k] * r[k - 1]
    # x[n-1] = r[n-1]/f[n-1]
    d2x[n - 1] = 0
    d2x[0] = 0
    for k in range(n - 2, 0, -1):
        d2x[k] = (r[k] - g[k] * originalx[k + 1]) / f[k]
    return d2x


x = [3, 4.5, 7, 9]
y = [2.5, 1, 2.5, 0.5]

d2x = cubic_spline(x, y)
yu, success = interpolate(x, y, d2x, 5)
print(yu)
print(success)