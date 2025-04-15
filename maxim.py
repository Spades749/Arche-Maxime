from geometry import assemble_maxim
from display import afficher
from physics import translation, translate

class ArcheMaxim:
    def __init__(self, R=2, H=6, n=10000, masse=100):
        self.R = R
        self.H = H
        self.n = n
        self.masse = masse
        self.position = [0, 0, 0]
        self.vitesse = [0, 0, 0]
        self.forme = assemble_maxim(n, R, H)

    def step(self, F, h):
        new_pos, new_vel = translation(self.masse, F, self.position, self.vitesse, h)
        self.forme = translate(self.forme, self.position, new_pos)
        self.position = new_pos
        self.vitesse = new_vel

    def afficher(self):
        afficher(self.forme)
