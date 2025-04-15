from OpenGL.GL import *
from geometry import draw_cylinder, draw_hemisphere, draw_paddle
import maths_utils as mu

class Maxim:
    def __init__(self, position, radius, height):
        self.position = list(position)
        self.radius = radius
        self.height = height
        self.velocity = [0.0, 0.0, 0.0]
        self.stopped = False

    def set_velocity_towards(self, target, speed):
        direction = [target[i] - self.position[i] for i in range(3)]
        dist = mu.distance3d(self.position, target)
        if dist == 0:
            self.velocity = [0.0, 0.0, 0.0]
        else:
            factor = speed / dist
            self.velocity = [direction[i] * factor for i in range(3)]

    def update(self, dt, target, target_radius):
        if self.stopped:
            return
        for i in range(3):
            self.position[i] += self.velocity[i] * dt
        if mu.distance3d(self.position, target) <= self.radius + target_radius:
            print("🚀 Collision avec la lune !")
            self.stopped = True

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)

        # Rotation automatique basée sur la direction
        vx, vy, vz = self.velocity
        if vx != 0.0 or vy != 0.0 or vz != 0.0:
            dir_len = mu.sqrt(vx * vx + vy * vy + vz * vz)
            if dir_len > 0.0001:
                # On aligne l'avant du modèle (face -Z) avec la direction de la vélocité
                yaw = mu.rad2deg(mu.atan2(vx, -vz))  # Yaw : tourne autour de Y
                pitch = mu.rad2deg(mu.atan2(vy, mu.sqrt(vx * vx + vz * vz)))  # Pitch : tourne autour de X
                glRotatef(yaw, 0.0, 1.0, 0.0)
                glRotatef(-pitch, 1.0, 0.0, 0.0)  # vers le haut = -pitch

        # Corps principal
        glColor3f(1.0, 0.8, 0.0)
        draw_cylinder(self.radius, self.height, slices=32)

        # Dôme doré au sommet
        glPushMatrix()
        glTranslatef(0.0, self.height / 2.0, 0.0)
        draw_hemisphere(self.radius, slices=32, stacks=16)
        glPopMatrix()

        # Visage doré à l'avant (Z+ car modèle tourné vers -Z par défaut)
        glPushMatrix()
        glTranslatef(0.0, self.height / 4.0, self.radius + 0.01)
        glColor3f(1.0, 1.0, 0.0)
        draw_hemisphere(self.radius * 0.4, slices=16, stacks=8)
        glPopMatrix()

        # Cheminée à l'arrière (Z-)
        glPushMatrix()
        glTranslatef(0.0, self.height + 0.5, -self.radius / 1.5)
        glColor3f(0.6, 0.6, 0.6)
        draw_cylinder(self.radius * 0.2, 2.0, slices=16)
        glPopMatrix()

        # Hélices arrière
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * (self.radius + 0.2), 0.0, -self.radius * 1.5)
            glRotatef(90, 1.0, 0.0, 0.0)
            glColor3f(0.2, 0.5, 1.0)
            for i in range(8):
                glPushMatrix()
                glRotatef(i * 45, 0.0, 0.0, 1.0)
                glBegin(GL_QUADS)
                glVertex3f(-0.05, 0.0, 0.0)
                glVertex3f(0.05, 0.0, 0.0)
                glVertex3f(0.05, 0.8, 0.0)
                glVertex3f(-0.05, 0.8, 0.0)
                glEnd()
                glPopMatrix()
            glPopMatrix()

        # Rames (latérales)
        for side in [-1, 1]:
            for i in range(8):
                glPushMatrix()
                glTranslatef(side * self.radius, -self.height / 2 + 0.5, -2 + i * 0.6)
                glRotatef(90 * side, 0.0, 1.0, 0.0)
                draw_paddle(self.height * 0.6, self.radius * 0.5)
                glPopMatrix()

        glPopMatrix()
