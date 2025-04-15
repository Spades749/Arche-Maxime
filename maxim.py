from OpenGL.GL import *
from geometry import draw_cylinder, draw_hemisphere, draw_paddle

class Maxim:
    def __init__(self, position, radius, height):
        self.position = list(position)
        self.radius = radius
        self.height = height

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glColor3f(1.0, 0.8, 0.0)

        draw_cylinder(self.radius, self.height, slices=32)

        glPushMatrix()
        glTranslatef(0.0, self.height / 2.0, 0.0)
        draw_hemisphere(self.radius, slices=32, stacks=16)
        glPopMatrix()

        for dx, angle in [(self.radius, 0), (-self.radius, 180)]:
            glPushMatrix()
            glTranslatef(dx, 0.0, 0.0)
            if angle:
                glRotatef(angle, 0.0, 1.0, 0.0)
            draw_paddle(self.height, self.radius)
            glPopMatrix()

        for dz, angle in [(self.radius, 90), (-self.radius, -90)]:
            glPushMatrix()
            glTranslatef(0.0, 0.0, dz)
            glRotatef(angle, 0.0, 1.0, 0.0)
            draw_paddle(self.height, self.radius)
            glPopMatrix()

        glPopMatrix()
