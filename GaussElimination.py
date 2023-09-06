def gauss(a, b, tol):
    er = 0
    #TODO check for sizes of a and b
    n = len(b)
    s = [0 for i in range(n)]

    for i in range(n):
        s[i] = abs(a[i][0])
        for j in range(1,n):
            if abs(a[i][j]) > s[i]:
                s[i] = abs(a[i][j])
    er = eliminate(a, s, b, tol)
    if er != -1:
        x = substitute(a, b)
    return (x, er)

def eliminate(a, s, b, tol):
    n = len(b)
    er = 0
    for k in range(n-1):
        pivot(a, b, s, k)
        if abs(a[k][k]/s[k]) < tol:
            er = -1
            break
    for i in range(k+1, n):
        factor = a[i][k]/a[k][k]
        for j in range(k+1, n):
            a[i][j] = a[i][j] - factor*a[k][j]
        b[i] = b[i] - factor*b[k]
    if abs(a[n][n]/s[n]) < tol:
        er = -1
    return er

def substitute(a, b):
    n = len(b)
    x = [0 for ii in range(n)]
    x[n-1] = b[n-1]/a[n-1][n-1]
    for i in range(n-2, 1, -1):
        sum = 0
        for j in range(i+1, n-1):
            sum = sum  + a[i][j]*x[j]
        x[i] = (b[i] - sum)!!!!
        pass

    return x
def pivot(a, b, s, k):
    p = k
    big = abs(a[k][k]/s[k])
    n = len(b)
    for i in range(k+1, n):
        dummy = abs(a[i][k]/s[i])
        if dummy > big:
            p = i
    if p != k:
        for j in range(k, n):
            dummy = a[p][j]
            a[p][j] = a[k][j]
        dummy = b[p]
        b[p] = b[k]
        b[k] = dummy
        dummy = s[k]
        !!!!

    return higgydiggy
