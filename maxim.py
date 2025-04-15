from OpenGL.GL import *
from math import sin, cos, pi
from geometry import draw_cylinder, draw_hemisphere, draw_paddle

class Maxim:
    """Représentation 3D de l'Arche Maxim composée d'un cylindre, d'un dôme (demi-sphère) et de quatre rames."""
    def __init__(self, position=(0.0, 0.0, 0.0), radius=2.0, height=4.0):
        self.position = [position[0], position[1], position[2]]
        self.radius = radius
        self.height = height

    def draw(self):
        """Dessine l'Arche Maxim à sa position actuelle."""
        glPushMatrix()
        # Positionnement de l'Arche dans la scène
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # Couleur de l'Arche (doré)
        glColor3f(1.0, 0.8, 0.0)
        # Corps principal: cylindre
        draw_cylinder(self.radius, self.height, slices=32)
        # Dôme supérieur: demi-sphère au sommet du cylindre
        glPushMatrix()
        glTranslatef(0.0, self.height/2.0, 0.0)  # place le dôme en haut du cylindre
        draw_hemisphere(self.radius, slices=32, stacks=16)
        glPopMatrix()
        # Rames (4 planches aux points cardinaux)
        paddle_height = self.height    # hauteur de la rame = hauteur du cylindre
        paddle_width = self.radius     # largeur de la rame = rayon du cylindre
        # Rame droite (+X)
        glPushMatrix()
        glTranslatef(self.radius, 0.0, 0.0)      # décalage sur le côté droit
        # (face déjà orientée vers +X, pas de rotation nécessaire)
        draw_paddle(paddle_height, paddle_width)
        glPopMatrix()
        # Rame gauche (-X)
        glPushMatrix()
        glTranslatef(-self.radius, 0.0, 0.0)     # décalage sur le côté gauche
        glRotatef(180.0, 0.0, 1.0, 0.0)          # pivote la rame pour faire face vers -X
        draw_paddle(paddle_height, paddle_width)
        glPopMatrix()
        # Rame avant (+Z)
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.radius)      # décalage à l'avant
        glRotatef(90.0, 0.0, 1.0, 0.0)           # pivote la rame pour faire face vers +Z
        draw_paddle(paddle_height, paddle_width)
        glPopMatrix()
        # Rame arrière (-Z)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -self.radius)     # décalage à l'arrière
        glRotatef(-90.0, 0.0, 1.0, 0.0)          # pivote la rame pour face vers -Z
        draw_paddle(paddle_height, paddle_width)
        glPopMatrix()
        # Fin du dessin de l'Arche
        glPopMatrix()
