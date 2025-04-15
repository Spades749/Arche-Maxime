import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from camera import Camera
from maxim import Maxim
import maths_utils as mu
import geometry

# 🎮 Initialisation
pygame.init()
width, height = 1280, 720
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Arche Maxim")

# 🌕 Lune (cible finale)
moon_position = [0.0, 0.0, 1000.0]
moon_radius = 5.0

# 🎨 OpenGL
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glClearColor(0.0, 0.0, 0.0, 1.0)
glPointSize(2)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45.0, width / float(height), 0.1, 500.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# 🌍 Terre
earth_position = [0.0, 0.0, 0.0]
earth_mass = 1000.0
earth_radius = 10.0

# 🚀 Arche Maxim
ark = Maxim(position=[0.0, 0.0, -earth_radius - 2.0], radius=2.0, height=4.0)

# 🎯 Vitesse initiale
initial_speed = 11.2
ark.set_velocity_towards(moon_position, speed=initial_speed)

# 🎥 Caméra
cam = Camera(target=ark, distance=30.0, height=8.0)

# ✨ Étoiles
stars = []
star_count = 2000
z_min = -50.0
z_max = moon_position[2] + 100.0
for _ in range(star_count):
    x = random.uniform(-150.0, 150.0)
    y = random.uniform(-150.0, 150.0)
    z = random.uniform(z_min, z_max)
    base_brightness = random.uniform(0.3, 1.0)
    flicker_amp = random.uniform(0.1, 0.4)  # amplitude du clignotement
    flicker_freq = random.uniform(0.5, 3.0)  # fréquence en Hz
    flicker_phase = random.uniform(0.0, 2 * mu.PI)
    stars.append([x, y, z, base_brightness, flicker_amp, flicker_freq, flicker_phase])

# 🕒 Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # ⚙️ Physique
    ark.apply_gravity_from(earth_position, earth_mass, earth_radius, moon_position)
    ark.update(dt, moon_position, moon_radius)
    cam.update()

    # 🎨 Rendu
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    cam.look()

    # 🌍 Terre
    glPushMatrix()
    glTranslatef(*earth_position)
    glColor3f(0.0, 0.2, 1.0)
    geometry.draw_sphere(earth_radius, slices=32, stacks=16)
    glPopMatrix()

    # 🌕 Lune
    glPushMatrix()
    glTranslatef(*moon_position)
    glColor3f(0.8, 0.8, 0.8)
    geometry.draw_sphere(moon_radius, slices=32, stacks=16)
    glPopMatrix()

    # 🚀 Arche
    ark.draw()

    # ✨ Étoiles
    glBegin(GL_POINTS)
    t = pygame.time.get_ticks() / 1000.0
    for s in stars:
        x, y, z, base_brightness, amp, freq, phase = s
        flicker = amp * mu.sin(freq * t + phase)
        intensity = max(0.0, min(1.0, base_brightness + flicker))
        glColor3f(intensity, intensity, intensity)
        glVertex3f(x, y, z)
    glEnd()

    pygame.display.flip()

pygame.quit()
