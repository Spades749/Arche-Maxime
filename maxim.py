from geometry import assemble_maxim
from maths_utils import somme_vect, prod_vect_scal, dist, vect
from OpenGL.GL import glBegin, glVertex3f, glEnd, glColor3f, GL_POINTS

class ArcheMaxim:
    def __init__(self, R=2, H=6, n=10000, masse=100):
        self.R = R
        self.H = H
        self.n = n
        self.masse = masse
        self.pos = [0, 0, 0]
        self.v = [0, 0, 0]
        self.points = assemble_maxim(n, R, H)
        self.stop = False

    def step(self, F, h, lune_pos, lune_radius):
        if self.stop:
            return
        a = prod_vect_scal(F, 1 / self.masse)
        new_pos = somme_vect(self.pos, prod_vect_scal(self.v, h))
        new_v = somme_vect(self.v, prod_vect_scal(a, h))

        if dist(new_pos, lune_pos) <= lune_radius + self.R:
            self.stop = True
            print("🚀 Collision avec la lune !")
            return

        dp = vect(self.pos, new_pos)
        self.points = [somme_vect(p, dp) for p in self.points]
        self.pos = new_pos
        self.v = new_v

    def draw(self):
        glColor3f(1, 1, 0)  # Arche Maxim en jaune
        glBegin(GL_POINTS)
        for p in self.points:
            glVertex3f(*p)
        glEnd()
