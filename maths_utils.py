pi = 3.1415926535

def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

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

def dist(A, B):
    return sum((A[i] - B[i])**2 for i in range(len(A)))**0.5
