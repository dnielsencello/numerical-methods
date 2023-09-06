def ludecomp(a, b, tol):
    x = []
    success = False

    o, s, er = decompose(a, b, tol)
    if er != -1:
        x = substitute(a, o, b)
        success = True
    return x, success

def decompose(a, b, tol):
    n = len(a)
    o = [0 for i in range(n)]
    s = [0 for i in range(n)]
    k = int
    er = 0
    for i in range(n):
        o[i] = i
        s[i] = abs(a[i][0])

        for j in range(2, n):
            if abs(a[i][j]) > s[i]:
                s[i] = abs(a[i][j])
        'end do'
    'end do'
    for k in range(0, n-1):
        pivot(a, b, o, s, k)
        if abs(a[o[k]][k]/s[o[k]]) < tol:
            er = -1
            'exit do'
        'end if'
        for i in range(k + 1, n):
            factor = a[o[i]][k]/a[o[k]][k]
            a[o[i]][k] = factor
            for j in range(k+1, n):
                a[o[i]][j] = a[o[i]][j] - factor*a[o[k]][j]
            'end do for j in range(k+2, n-1)'
        'end do for i in range9k+2, n - 1)'
        if abs(a[o[k]][k]/s[o[k]]) < tol:
            er = -1
            print(a[o[k]][k]/s[o[k]])
    return o, s, er

def pivot(a, b, o, s, k):
    n = len(a)
    p = k
    big = abs(a[k][k]/s[o[k]])
    for ii in range(k+1, n):
        dummy = abs(a[o[ii]][k]/s[o[ii]])
        if dummy > big:
            big = dummy
            p = ii
    dummy = o[p]
    o[p] = o[k]
    o[k] = dummy



def substitute(a, o, b):

    n = len(a)
    x = [0 for i in range(n)]
    for i in range(1, n):
        sum = b[o[i]]
        for j in range(i):
            sum = sum - a[o[i]][j]*b[o[j]]
        b[o[i]]=sum
    x[n-1] = b[n-1]/a[n-1][n-1]
    for i in range(n-2, -1, -1):
        sum = 0
        for j in range(i+1, n):
            sum = sum + a[i][j]*x[j]
        x[i] = (b[o[i]] - sum)/a[o[i]][i]
    hello = x
    return x




a = [[3, -0.1, -0.2], [0.1 , 7, -0.3], [0.3, -0.2, 10]]
b = [7.85, -19.3, 71.4]
tol = 0.001
ludecomp(a, b, tol)