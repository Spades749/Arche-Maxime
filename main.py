import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from camera import Camera
from maxim import Maxim
import maths_utils as mu
import geometry

pygame.init()
width, height = 1280, 720
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Arche Maxim")

# OpenGL initialisation
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glClearColor(0.0, 0.0, 0.0, 1.0)
glPointSize(2)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45.0, width / float(height), 0.1, 300.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Lune
moon_radius = 5.0
moon_position = [0.0, 0.0, -100.0]

# Arche Maxim + vitesse
ark = Maxim(position=[20.0, 0.0, 0.0], radius=2.0, height=4.0)
ark.set_velocity_towards(moon_position, speed=10.0)

# Caméra third person dynamique, suit l'Arche par l'arrière
cam = Camera(target=ark, distance=18.0, height=6.0)

# Génération d'étoiles
stars = []
for _ in range(200):
    r = random.uniform(50.0, 100.0)
    u = random.uniform(-1.0, 1.0)
    theta = random.uniform(0.0, 2 * mu.PI)
    x = r * mu.sqrt(1 - u * u) * mu.cos(theta)
    y = r * mu.sqrt(1 - u * u) * mu.sin(theta)
    z = r * u
    stars.append([x, y, z])

# Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Mise à jour
    ark.update(dt, moon_position, moon_radius)
    cam.update()

    # Affichage
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    cam.look()  # Mise à jour de la caméra

    # Lune
    glPushMatrix()
    glTranslatef(*moon_position)
    glColor3f(0.8, 0.8, 0.8)
    geometry.draw_sphere(moon_radius, slices=32, stacks=16)
    glPopMatrix()

    # Arche
    ark.draw()

    # Étoiles
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for s in stars:
        glVertex3f(*s)
    glEnd()

    # Finalisation frame
    pygame.display.flip()

pygame.quit()
