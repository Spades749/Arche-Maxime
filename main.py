import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from maxim import ArcheMaxim
from camera import Camera
from geometry import sphere

def draw_points(points, color=(0.6, 0.6, 0.6)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for p in points:
        glVertex3f(*p)
    glEnd()

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Arche Maxim 3D")

    gluPerspective(45, (1280 / 720), 0.1, 1000.0)

    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(2)

    clock = pygame.time.Clock()
    cam = Camera()
    arche = ArcheMaxim()
    lune_center = [0, 0, 40]
    lune_radius = 5
    lune_pts = sphere(2000, lune_radius, lune_center)

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
        cam.apply()

        arche.step([0, 0, 20], 0.4, lune_center, lune_radius)
        arche.draw()
        draw_points(lune_pts, (0.7, 0.7, 0.7))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()