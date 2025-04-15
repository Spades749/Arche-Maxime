from maths_utils import sin, cos, pi

def cylindre(n, R, h):
    n2 = int(n**(1/3))
    dteta = 2 * pi / n2
    dz = h / n2
    zmin = -h / 2
    points = []
    for r in range(n2):
        for t in range(n2):
            for z in range(n2):
                rr = R * r / n2
                x = rr * cos(t * dteta)
                y = rr * sin(t * dteta)
                zz = zmin + z * dz
                points.append([x, y, zz])
    return points

def demi_sphere(n, R, z_offset):
    n2 = int(n**(1/2))
    dteta = pi / n2
    dphi = 2 * pi / n2
    points = []
    for t in range(n2):
        for p in range(n2):
            x = R * sin(t * dteta) * cos(p * dphi)
            y = R * sin(t * dteta) * sin(p * dphi)
            z = R * cos(t * dteta) + z_offset
            points.append([x, y, z])
    return points

def sphere(n, R, center):
    n2 = int(n**(1/2))
    dteta = pi / n2
    dphi = 2 * pi / n2
    points = []
    for t in range(n2):
        for p in range(n2):
            x = R * sin(t * dteta) * cos(p * dphi) + center[0]
            y = R * sin(t * dteta) * sin(p * dphi) + center[1]
            z = R * cos(t * dteta) + center[2]
            points.append([x, y, z])
    return points

def assemble_maxim(n, R, H):
    body = cylindre(n, R, H)
    dome = demi_sphere(n, R, -H/2)
    rames = []
    for i in range(-4, 5):
        for j in range(4):
            rames.append([R+0.2, i * 0.5, -H/4 + j*0.1])
            rames.append([-R-0.2, i * 0.5, -H/4 + j*0.1])
    return body + dome + rames