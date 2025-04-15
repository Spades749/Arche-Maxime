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
pygame.display.set_caption("Arche Maxim - Ciel étoilé")

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glClearColor(0.0, 0.0, 0.0, 1.0)
glPointSize(2)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45.0, width / float(height), 0.1, 300.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

ark = Maxim(position=[20.0, 0.0, 0.0], radius=2.0, height=4.0)
cam = Camera(target=ark, offset=[0.0, 5.0, 15.0])

moon_radius = 5.0
moon_position = [0.0, 0.0, -100.0]

stars = []
for _ in range(200):
    r = random.uniform(50.0, 100.0)
    u = random.uniform(-1.0, 1.0)
    theta = random.uniform(0.0, 2 * mu.PI)
    x = r * mu.sqrt(1 - u*u) * mu.cos(theta)
    y = r * mu.sqrt(1 - u*u) * mu.sin(theta)
    z = r * u
    stars.append([x, y, z])

clock = pygame.time.Clock()
angle = 0.0
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    angle += mu.deg2rad(0.5)
    ark.position[0] = 20.0 * mu.cos(angle)
    ark.position[2] = 20.0 * mu.sin(angle)
    cam.update()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    cx, cy, cz = cam.position
    tx, ty, tz = ark.position
    gluLookAt(cx, cy, cz, tx, ty, tz, 0.0, 1.0, 0.0)

    # lune
    glPushMatrix()
    glTranslatef(*moon_position)
    glColor3f(0.8, 0.8, 0.8)
    geometry.draw_sphere(moon_radius, slices=32, stacks=16)
    glPopMatrix()

    # Arche
    ark.draw()

    # étoiles
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for s in stars:
        glVertex3f(*s)
    glEnd()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
