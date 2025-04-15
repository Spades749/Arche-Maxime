import math

def distance3d(p1, p2):
    """Calcule la distance euclidienne entre deux points 3D p1 et p2."""
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def deg2rad(deg):
    """Convertit des degrés en radians."""
    return deg * math.pi / 180.0

def rad2deg(rad):
    """Convertit des radians en degrés."""
    return rad * 180.0 / math.pi
