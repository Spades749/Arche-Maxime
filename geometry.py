from maths_utils import cos, sin, pi

def transpose(M):
    return [list(col) for col in zip(*M)]

def cylindre(n, R, h):
    n2 = int(n**(1/3))
    dr = R / n2
    dz = h / n2
    dteta = 2 * pi / n2
    zmin = -h / 2
    W = []

    for r in range(n2):
        for t in range(n2):
            for z in range(n2):
                x = r * dr * cos(t * dteta)
                y = r * dr * sin(t * dteta)
                zz = zmin + z * dz
                W.append([x, y, zz])
    return transpose(W)

def demi_sphere(n, R, z_offset):
    n2 = int(n**(1/2))
    dteta = pi / n2
    dphi = 2 * pi / n2
    W = []

    for t in range(n2):
        for p in range(n2):
            x = R * sin(t * dteta) * cos(p * dphi)
            y = R * sin(t * dteta) * sin(p * dphi)
            z = R * cos(t * dteta) + z_offset
            W.append([x, y, z])
    return transpose(W)

def assemble_maxim(n, R, H):
    body = cylindre(n, R, H)
    sphere = demi_sphere(n, R, -H/2)
    return [body[0] + sphere[0], body[1] + sphere[1], body[2] + sphere[2]]
