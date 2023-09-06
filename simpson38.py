def simp38_ndim(a,b,nint,func):
    nint = max(1, int((nint+2)/3))*3 # Make this change to nint to ensure that the intervals are a multiple of 3
    interval = float(abs(b-a)/nint)
    summ = 0
    for i in range(0, nint+1):
        spot = interval*i+a
        if i == 0:
            summ += func(spot)
        elif i % 3 == 0 and i != nint:
            summ += 2*func(spot)
        elif i % 3 != 0 and i != nint:
            summ += 3 * func(spot)
        elif i == nint:
            summ += func(spot)
    summ = 3*summ*interval/8
    print(summ)
    return summ

nint = 0
a = -1.5
b = 1.5


def func(x):
    return x ** 4 - x**3

simp38_ndim(a,b,nint,func)

