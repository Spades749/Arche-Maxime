PI = 3.1415926535

def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

def deg2rad(deg):
    return deg * PI / 180.0

def rad2deg(rad):
    return rad * 180.0 / PI

def cos(x):
    s = 0
    for i in range(10):
        s += (-1) ** i * x ** (2 * i) / fact(2 * i)
    return s

def sin(x):
    s = 0
    for i in range(10):
        s += (-1) ** i * x ** (2 * i + 1) / fact(2 * i + 1)
    return s

def sqrt(x, iterations=10):
    r = x
    for _ in range(iterations):
        r = 0.5 * (r + x / r)
    return r

def distance3d(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return sqrt(dx*dx + dy*dy + dz*dz)
