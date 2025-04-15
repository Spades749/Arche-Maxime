import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from maxim import ArcheMaxim
from camera import Camera
from geometry import sphere
import random

def draw_points(points, color=(0.6, 0.6, 0.6), size=10):
    glColor3f(*color)
    glPointSize(size)
    glBegin(GL_POINTS)
    for p in points:
        glVertex3f(*p)
    glEnd()

def generate_stars(nb=500):
    stars = []
    for _ in range(nb):
        x = random.uniform(-100, 100)
        y = random.uniform(-100, 100)
        z = random.uniform(-100, 100)
        stars.append([x, y, z])
    return stars

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Arche Maxim 3D")

    gluPerspective(45, (1280 / 720), 0.1, 1000.0)

    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)  # ← ajoute cette ligne
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(3)

    clock = pygame.time.Clock()
    cam = Camera()
    cam.pos = [0, -50, 10]  # caméra très en arrière
    arche = ArcheMaxim()
    lune_center = [0, 0, 50]
    lune_radius = 5
    lune_pts = sphere(500, lune_radius, lune_center)
    stars = generate_stars(800)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        keys = pygame.key.get_pressed()
        cam.update(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Point rouge au centre
        glColor3f(1, 0, 0)
        glPointSize(8)
        glBegin(GL_POINTS)
        glVertex3f(0, 0, 0)
        glEnd()

        cam.apply()

        draw_points(stars, (1, 1, 1), size=1)
        draw_points(lune_pts, (0.7, 0.7, 0.7), size=2)

        # Affiche la position de l'Arche (point cyan)
        glColor3f(0, 1, 1)
        glPointSize(6)
        glBegin(GL_POINTS)
        glVertex3f(*arche.pos)
        glEnd()

        # Arche Maxim
        arche.step([0, 0, 2], 0.1, lune_center, lune_radius)
        arche.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()