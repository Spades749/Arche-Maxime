import math

class Camera:
    """Caméra qui suit une cible 3D (ayant un attribut position) avec un décalage fixe."""
    def __init__(self, target=None, offset=(0.0, 5.0, 15.0)):
        self.target = target
        # Décalage (dx, dy, dz) par rapport à la position de la cible
        self.offset = offset
        # Position initiale de la caméra
        if self.target is not None:
            tx, ty, tz = self.target.position
        else:
            tx = ty = tz = 0.0
        ox, oy, oz = self.offset
        self.position = [tx + ox, ty + oy, tz + oz]

    def update(self):
        """Met à jour la position de la caméra pour suivre la cible."""
        if self.target is None:
            return
        tx, ty, tz = self.target.position
        ox, oy, oz = self.offset
        # Maintient le décalage par rapport à la cible
        self.position[0] = tx + ox
        self.position[1] = ty + oy
        self.position[2] = tz + oz
