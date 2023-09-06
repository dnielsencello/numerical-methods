def runge_kutta4_ndim(x, y, h, derivs):

    n = len(y)
    interval = h/2
    slope = [0] * n
    ynew = [0] * n
    klist = [[0]*n]*4
    klistfinal = [[0]*n]*4
    klistfinal[0] = derivs(x, y)

    for k in range(1, 4):
        if k == 3:
            interval = h
        for i in range(n):
            klist[k][i] = y[i] + klistfinal[k-1][i]*interval
        klistfinal[k] = derivs(x+interval, klist[k])

    for i in range(n):
        slope[i] = (klistfinal[0][i] + 2 * (klistfinal[1][i] + klistfinal[2][i]) + klistfinal[3][i]) / 6
        ynew[i] = y[i] + slope[i] * h
    return ynew


# def runge_kutta4_ndim(x, y, h, derivs):
    n = len(y)
    ynew = [0] * n
    k1 = [0] * n
    k2 = [0] * n
    k3 = [0] * n
    k4 = [0] * n
    k11 = [0] * n
    k22 = [0] * n
    k33 = [0] * n
    slope = [0] * n

    k1 = derivs(x, y)
    for i in range(n):
        k11[i] = y[i] + k1[i] * h / 2
    k2 = derivs(x + h / 2, k11)
    for i in range(n):
        k22[i] = y[i] + k2[i] * h / 2
    k3 = derivs(x + h / 2, k22)
    for i in range(n):
        k33[i] = y[i] + k3[i] * h
    k4 = derivs(x + h, k33)
    for i in range(n):
        slope[i] = (k1[i] + 2 * (k2[i] + k3[i]) + k4[i]) / 6
        ynew[i] = y[i] + slope[i] * h
    return ynew
