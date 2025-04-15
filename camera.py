from OpenGL.GLU import *
from maths_utils import sqrt

class Camera:
    def __init__(self, target=None, distance=30.0, height=8.0):
        self.target = target
        self.distance = distance
        self.height = height
        self.position = [0.0, 0.0, 0.0]

    def update(self):
        if self.target is None:
            return

        tx, ty, tz = self.target.position
        vx, vy, vz = self.target.velocity

        speed_sq = vx * vx + vy * vy + vz * vz
        if speed_sq > 0.0001:
            speed = sqrt(speed_sq)
            nx = vx / speed
            ny = vy / speed
            nz = vz / speed
        else:
            nx, ny, nz = 0.0, 0.0, 1.0

        self.position[0] = tx - nx * self.distance
        self.position[1] = ty - ny * self.distance + self.height
        self.position[2] = tz - nz * self.distance

    def look(self):
        if self.target:
            gluLookAt(*self.position, *self.target.position, 0.0, 1.0, 0.0)
        else:
            gluLookAt(*self.position, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
