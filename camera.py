from OpenGL.GLU import *

class Camera:
    def __init__(self, target=None, offset=[0.0, 5.0, 15.0]):
        self.target = target
        self.offset = offset
        tx, ty, tz = target.position if target else [0.0, 0.0, 0.0]
        ox, oy, oz = offset
        self.position = [tx + ox, ty + oy, tz + oz]

    def update(self):
        if self.target is None:
            return
        tx, ty, tz = self.target.position
        ox, oy, oz = self.offset
        self.position = [tx + ox, ty + oy, tz + oz]

    def look(self):
        if self.target:
            gluLookAt(*self.position, *self.target.position, 0.0, 1.0, 0.0)
        else:
            gluLookAt(*self.position, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
