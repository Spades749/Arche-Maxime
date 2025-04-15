pi = 3.1415926535

def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)

def cos(x):
    s = 0
    for i in range(10):
        s += (-1)**i * x**(2*i) / fact(2*i)
    return s

def sin(x):
    s = 0
    for i in range(10):
        s += (-1)**i * x**(2*i+1) / fact(2*i+1)
    return s

def somme_vect(A, B):
    return [A[i] + B[i] for i in range(len(A))]

def prod_vect_scal(A, k):
    return [k * A[i] for i in range(len(A))]

def vect(A, B):
    return [B[i] - A[i] for i in range(len(A))]

def prod_vect_vect(A, B):
    return [
        A[1]*B[2] - A[2]*B[1],
        A[2]*B[0] - A[0]*B[2],
        A[0]*B[1] - A[1]*B[0]
    ]
