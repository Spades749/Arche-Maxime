from OpenGL.GLU import *
from maths_utils import sqrt

class Camera:
    def __init__(self, target=None, distance=15.0, height=5.0):
        self.target = target      # L'Arche Maxim (avec .position et .velocity)
        self.distance = distance  # Distance derrière le vaisseau
        self.height = height      # Décalage vertical au-dessus du vaisseau
        self.position = [0.0, 0.0, 0.0]

    def update(self):
        if self.target is None:
            return

        # Position du vaisseau
        tx, ty, tz = self.target.position
        vx, vy, vz = self.target.velocity

        speed_sq = vx * vx + vy * vy + vz * vz

        if speed_sq > 0.0001:
            speed = sqrt(speed_sq)
            nx = vx / speed
            ny = vy / speed
            nz = vz / speed
        else:
            # Valeur par défaut si la vitesse est trop faible
            nx, ny, nz = 0.0, 0.0, 1.0  # Avance vers -Z

        # Caméra derrière le vaisseau (+ au-dessus)
        self.position[0] = tx - nx * self.distance
        self.position[1] = ty - ny * self.distance + self.height
        self.position[2] = tz - nz * self.distance

    def look(self):
        if self.target is None:
            gluLookAt(*self.position, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        else:
            gluLookAt(*self.position, *self.target.position, 0.0, 1.0, 0.0)
