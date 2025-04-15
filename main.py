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

# 🌕 Lune (fixée suffisamment loin pour ~10-15s de trajet)
moon_radius = 5.0
moon_position = [0.0, 0.0, 1000.0]


# 🚀 Arche Maxim
ark = Maxim(position=[0.0, 0.0, -earth_radius - 2.0], radius=2.0, height=4.0)

# 🎯 Vitesse initiale vers la lune
initial_speed = 11.2  # m/s
ark.set_velocity_towards(moon_position, speed=initial_speed)

# 🎥 Caméra
cam = Camera(target=ark, distance=30.0, height=8.0)

# ✨ Étoiles
stars = []
for _ in range(200):
    r = random.uniform(50.0, 100.0)
    u = random.uniform(-1.0, 1.0)
    theta = random.uniform(0.0, 2 * mu.PI)
    x = r * mu.sqrt(1 - u * u) * mu.cos(theta)
    y = r * mu.sqrt(1 - u * u) * mu.sin(theta)
    z = r * u
    stars.append([x, y, z])

# 🕒 Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # ⚙️ Physique
    ark.apply_gravity_from(earth_position, earth_mass, earth_radius)
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

    # 🌕 Lune (fixe)
    glPushMatrix()
    glTranslatef(*moon_position)
    glColor3f(0.8, 0.8, 0.8)
    geometry.draw_sphere(moon_radius, slices=32, stacks=16)
    glPopMatrix()

    # 🚀 Arche
    ark.draw()

    # ✨ Étoiles
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for s in stars:
        glVertex3f(*s)
    glEnd()

    pygame.display.flip()

pygame.quit()