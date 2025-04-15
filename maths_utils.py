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
        s += (-1)**i * (x**(2*i)) / fact(2*i)
    return s

def sin(x):
    s = 0
    for i in range(10):
        s += (-1)**i * (x**(2*i + 1)) / fact(2*i + 1)
    return s

def sqrt(x, iterations=10):
    r = x
    for _ in range(iterations):
        r = 0.5 * (r + x / r)
    return r

def atan(x):
    if x < -1.0:
        return -PI/2 - atan(1.0 / x)
    elif x > 1.0:
        return PI/2 - atan(1.0 / x)
    s = 0
    for i in range(10):
        coef = (-1)**i / (2*i + 1)
        s += coef * (x**(2*i + 1))
    return s

def atan2(y, x):
    if x > 0:
        return atan(y / x)
    elif x < 0 and y >= 0:
        return atan(y / x) + PI
    elif x < 0 and y < 0:
        return atan(y / x) - PI
    elif x == 0 and y > 0:
        return PI / 2
    elif x == 0 and y < 0:
        return -PI / 2
    return 0.0

def distance3d(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return sqrt(dx*dx + dy*dy + dz*dz)

def cross_product_3d(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def vector_length(v):
    return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def normalize3d(v):
    l = vector_length(v)
    return [v[i]/l for i in range(3)] if l > 0 else [0.0, 0.0, 0.0]

def vector_scale(v, s):
    return [v[i]*s for i in range(3)]

def vector_add(a, b):
    return [a[i]+b[i] for i in range(3)]

def draw_vector_arrow(pos, dir_vec, color=(1.0, 0.0, 0.0)):
    from OpenGL.GL import glBegin, glEnd, glColor3f, glVertex3f, GL_LINES
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex3f(*pos)
    endpoint = vector_add(pos, dir_vec)
    glVertex3f(*endpoint)
    glEnd()
