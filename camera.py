import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self):
        self.pos = [0, -10, 10]
        self.rot = [30, 0]  # x pitch, y yaw
        self.speed = 0.5

    def update(self, keys):
        if keys[pygame.K_z]:
            self.pos[2] -= self.speed
        if keys[pygame.K_s]:
            self.pos[2] += self.speed
        if keys[pygame.K_q]:
            self.pos[0] -= self.speed
        if keys[pygame.K_d]:
            self.pos[0] += self.speed

    def apply(self):
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])
