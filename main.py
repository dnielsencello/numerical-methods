def taylor_series_expansion_of_e(x,n):
    y=0
    i=0
    fac = 1
    while i <= n:
        fac = fac*i if i != 0 else fac
        y += (1/fac)*x**i
        i += 1
    return y
answer = taylor_series_expansion_of_e(5,4)
print(answer)

de