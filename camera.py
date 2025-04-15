import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self):
        self.pos = [0, -50, 10]  # placé derrière l’Arche
        self.speed = 0.5

    def update(self, keys):
        if keys[pygame.K_z]:
            self.pos[1] += self.speed
        if keys[pygame.K_s]:
            self.pos[1] -= self.speed
        if keys[pygame.K_q]:
            self.pos[0] -= self.speed
        if keys[pygame.K_d]:
            self.pos[0] += self.speed
        if keys[pygame.K_SPACE]:
            self.pos[2] += self.speed
        if keys[pygame.K_LSHIFT]:
            self.pos[2] -= self.speed

    def apply(self):
        gluLookAt(
            self.pos[0], self.pos[1], self.pos[2],               # position de la caméra
            self.pos[0], self.pos[1] + 1, self.pos[2],           # regarde tout droit
            0, 0, 1                                               # axe Z vertical
        )