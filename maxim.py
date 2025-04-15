import pygame
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
        self.escaped_earth = False
        self.escape_timer = 0.0
        self.counting_escape = False
        self.rotate_model = False
        self.forces = []
        self.ui_forces = []  # ← Ajout : forces pour affichage UI

        self.angular_velocity = 0.0
        self.rotation_angle = 0.0
        self.mass = 10.0
        self.I = 0.5 * self.mass * radius * radius

    def apply_gravity_from(self, source_pos, source_mass, source_radius, moon_pos):
        G = 0.5
        dx = source_pos[0] - self.position[0]
        dy = source_pos[1] - self.position[1]
        dz = source_pos[2] - self.position[2]
        dist_sq = dx * dx + dy * dy + dz * dz

        if dist_sq < (source_radius + 150) ** 2:
            dist = mu.sqrt(dist_sq)
            force_mag = G * source_mass / dist_sq
            ax = force_mag * dx / dist
            ay = force_mag * dy / dist
            az = force_mag * dz / dist
            self.velocity[0] += ax
            self.velocity[1] += ay
            self.velocity[2] += az
        else:
            if not self.escaped_earth:
                self.escaped_earth = True
                self.counting_escape = True
                self.rotate_model = True

                direction = [moon_pos[i] - self.position[i] for i in range(3)]
                dist = mu.sqrt(sum(d * d for d in direction))
                direction = [d / dist for d in direction]
                speed = dist / 12.0
                self.velocity = [direction[i] * speed for i in range(3)]

                print("🌌 L’Arche Maxim a quitté l’attraction terrestre !")

    def set_velocity_towards(self, target, speed):
        direction = [target[i] - self.position[i] for i in range(3)]
        dist = mu.distance3d(self.position, target)
        if dist == 0:
            self.velocity = [0.0, 0.0, 0.0]
        else:
            factor = speed / dist
            self.velocity = [direction[i] * factor for i in range(3)]

    def apply_force(self, r, F):
        moment = mu.cross_product_3d(r, F)
        torque_y = moment[1]
        angular_acc = torque_y / self.I
        self.angular_velocity += angular_acc
        self.forces.append((r, F))
        self.ui_forces.append((r, F))  # ← Ajout : enregistre force pour UI

    def mouvement(self, F, r, dt):
        acc = [f / self.mass for f in F]
        delta_v = mu.vector_scale(acc, dt)
        self.velocity = mu.vector_add(self.velocity, delta_v)
        self.apply_force(r, F)

    def update(self, dt, target, target_radius):
        if self.stopped:
            return
        for i in range(3):
            self.position[i] += self.velocity[i] * dt
        self.rotation_angle += mu.rad2deg(self.angular_velocity) * dt
        if self.counting_escape:
            self.escape_timer += dt
        if mu.distance3d(self.position, target) <= self.radius + target_radius:
            print("🚀 Collision avec la lune !")
            if self.counting_escape:
                print(f"⏱️ Temps depuis sortie Terre : {self.escape_timer:.1f} secondes")
            self.stopped = True
            self.counting_escape = False

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        if self.rotate_model:
            glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)

        glColor3f(1.0, 0.8, 0.0)
        draw_cylinder(self.radius, self.height, slices=32)

        glPushMatrix()
        glTranslatef(0.0, self.height / 2.0, 0.0)
        draw_hemisphere(self.radius, slices=32, stacks=16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, self.height / 4.0, self.radius + 0.01)
        glColor3f(1.0, 1.0, 0.0)
        draw_hemisphere(self.radius * 0.4, slices=16, stacks=8)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, self.height + 0.5, -self.radius / 1.5)
        glColor3f(0.6, 0.6, 0.6)
        draw_cylinder(self.radius * 0.2, 2.0, slices=16)
        glPopMatrix()

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

        for side in [-1, 1]:
            for i in range(8):
                glPushMatrix()
                glTranslatef(side * self.radius, -self.height / 2 + 0.5, -2 + i * 0.6)
                glRotatef(90 * side, 0.0, 1.0, 0.0)
                draw_paddle(self.height * 0.6, self.radius * 0.5)
                glPopMatrix()

        glPopMatrix()
