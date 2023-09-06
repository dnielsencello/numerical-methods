import math

def quadroot(r,s):
    disc = r*r + 4*s
    if disc > 0:
        r1 = r + math.sqrt(disc)/2
        r2 = r - math.sqrt(disc)/2
        i1 = 0
        i2 = 0
    else:
        r1 = r/2
        r2 = r1
        i1 = math.sqrt(abs(disc))/2
        i2 = - i1
    return (r1, i1, r2, i2)

print(quadroot(0, -4))
print(quadroot(0, 4))

