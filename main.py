import math
import random
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_ESCAPE
from OpenGL.GL import *
from OpenGL.GLU import *

# Importation des modules personnalisés
from camera import Camera
from maxim import Maxim
import maths_utils
import geometry

# Initialisation de Pygame et création de la fenêtre OpenGL
pygame.init()
width, height = 1280, 720
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Configuration de la perspective et du rendu OpenGL
glEnable(GL_DEPTH_TEST)              # Activation du test de profondeur
glDepthFunc(GL_LESS)                # Garder les fragments les plus proches de la caméra
glClearColor(0.0, 0.0, 0.0, 1.0)     # Couleur de fond noire opaque
glPointSize(3.0)                    # Taille des points (étoiles) pour être bien visibles

# Projection en perspective (champ de vision 45°, ratio d'aspect, plan proche et lointain)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45.0, width / float(height), 0.1, 300.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Création des objets de la scène
ark = Maxim(position=(20.0, 0.0, 0.0), radius=2.0, height=4.0)   # Arche Maxim positionnée initialement
cam = Camera(target=ark, offset=(0.0, 5.0, 15.0))               # Caméra suivant l'Arche avec un décalage

# Création de la lune (sphère grise à une certaine position fixe)
moon_radius = 5.0
moon_position = (0.0, 0.0, -100.0)  # lune éloignée sur l'axe Z

# Génération d'un fond étoilé (points aléatoires dans l'espace 3D)
stars = []
num_stars = 200
min_dist = 50.0   # distance minimale des étoiles par rapport à l'origine
max_dist = 100.0  # distance maximale des étoiles
for _ in range(num_stars):
    # Génère un point aléatoire uniformément distribué dans une sphère creuse (entre min_dist et max_dist)
    r = random.uniform(min_dist, max_dist)
    u = random.uniform(-1.0, 1.0)
    theta = random.uniform(0.0, 2 * math.pi)
    # Conversion coordonnées sphériques -> cartésiennes
    x = r * math.sqrt(1 - u**2) * math.cos(theta)
    y = r * math.sqrt(1 - u**2) * math.sin(theta)
    z = r * u
    stars.append((x, y, z))

# Boucle principale de rendu
clock = pygame.time.Clock()
angle = 0.0  # angle de rotation pour le mouvement de l'Arche
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    # Mise à jour de la position de l'Arche (animation circulaire autour de l'origine pour l'exemple)
    angle += maths_utils.deg2rad(0.5)  # incrémente l'angle en radians
    ark.position[0] = 20.0 * math.cos(angle)
    ark.position[2] = 20.0 * math.sin(angle)
    # Mise à jour de la caméra pour suivre la nouvelle position de l'Arche
    cam.update()

    # Rendu de la scène 3D
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Efface le tampon de couleur et de profondeur
    glLoadIdentity()
    # Configuration de la vue caméra (point de vue)
    if cam.target:
        # Place la caméra à cam.position et regarde vers la position de l'Arche (target)
        cx, cy, cz = cam.position
        tx, ty, tz = cam.target.position
        gluLookAt(cx, cy, cz,  tx, ty, tz,  0.0, 1.0, 0.0)
    else:
        # Si aucune cible, on regarde par défaut vers l'origine
        gluLookAt(cam.position[0], cam.position[1], cam.position[2],
                  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

    # Dessine la lune
    glPushMatrix()
    glTranslatef(moon_position[0], moon_position[1], moon_position[2])
    glColor3f(0.8, 0.8, 0.8)  # couleur grise
    geometry.draw_sphere(moon_radius, slices=32, stacks=16)  # sphère pleine
    glPopMatrix()

    # Dessine l'Arche Maxim
    ark.draw()

    # Dessine les étoiles (en tant que points)
    glColor3f(1.0, 1.0, 1.0)  # couleur blanche pour les étoiles
    glBegin(GL_POINTS)
    for (sx, sy, sz) in stars:
        glVertex3f(sx, sy, sz)
    glEnd()

    # Affichage de la frame à l'écran
    pygame.display.flip()
    clock.tick(60)

# Quitte proprement
pygame.quit()
