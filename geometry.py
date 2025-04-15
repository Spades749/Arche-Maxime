from math import sin, cos, pi
from OpenGL.GL import *

def draw_cylinder(radius, height, slices=16):
    """Dessine un cylindre plein centré à l'origine (axe Y vertical, hauteur totale donnée)."""
    half_h = height / 2.0
    # Surface latérale du cylindre
    glBegin(GL_QUADS)
    for i in range(slices):
        theta1 = 2 * pi * i / slices
        theta2 = 2 * pi * (i + 1) / slices
        # Points sur le cercle en bas et en haut pour cette tranche
        x1 = radius * cos(theta1); z1 = radius * sin(theta1)
        x2 = radius * cos(theta2); z2 = radius * sin(theta2)
        # Quatre sommets du quadrilatère (bas1, haut1, haut2, bas2)
        glVertex3f(x1, -half_h, z1)
        glVertex3f(x1,  half_h, z1)
        glVertex3f(x2,  half_h, z2)
        glVertex3f(x2, -half_h, z2)
    glEnd()
    # Dessine le disque du haut (face supérieure)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, half_h, 0.0)  # centre du disque du haut
    for i in range(slices + 1):
        theta = 2 * pi * (i % slices) / slices
        x = radius * cos(theta); z = radius * sin(theta)
        glVertex3f(x, half_h, z)
    glEnd()
    # Dessine le disque du bas (face inférieure)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, -half_h, 0.0)  # centre du disque du bas
    for i in range(slices + 1):
        theta = 2 * pi * (i % slices) / slices
        x = radius * cos(theta); z = radius * sin(theta)
        glVertex3f(x, -half_h, z)
    glEnd()

def draw_sphere(radius, slices=16, stacks=16, phi_start=0.0, phi_end=pi):
    """Dessine une sphère (ou portion sphérique) de rayon donné, centrée à l'origine.
    phi_start et phi_end permettent de limiter la sphère (latitude) pour dessiner par ex. une demi-sphère."""
    # Partie supérieure (pôle nord) si on commence à phi 0
    if phi_start == 0.0:
        next_phi = (phi_end - phi_start) / stacks
        glBegin(GL_TRIANGLE_FAN)
        # Pôle nord
        glVertex3f(0.0, radius, 0.0)
        phi = next_phi
        for j in range(slices + 1):
            theta = 2 * pi * (j % slices) / slices
            x = radius * sin(phi) * cos(theta)
            y = radius * cos(phi)
            z = radius * sin(phi) * sin(theta)
            glVertex3f(x, y, z)
        glEnd()
        start_stack = 1
    else:
        start_stack = 0
    # Tranches intermédiaires (quad strips) entre phi_start et phi_end
    for i in range(start_stack, stacks - 1):
        phi1 = phi_start + (phi_end - phi_start) * i / stacks
        phi2 = phi_start + (phi_end - phi_start) * (i + 1) / stacks
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            theta = 2 * pi * (j % slices) / slices
            x1 = radius * sin(phi1) * cos(theta)
            y1 = radius * cos(phi1)
            z1 = radius * sin(phi1) * sin(theta)
            x2 = radius * sin(phi2) * cos(theta)
            y2 = radius * cos(phi2)
            z2 = radius * sin(phi2) * sin(theta)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
        glEnd()
    # Partie inférieure (pôle sud) si on termine à phi = pi
    if phi_end == pi:
        phi = phi_end - (phi_end - phi_start) / stacks
        glBegin(GL_TRIANGLE_FAN)
        # Pôle sud
        glVertex3f(0.0, -radius, 0.0)
        for j in range(slices + 1):
            theta = 2 * pi * (j % slices) / slices
            x = radius * sin(phi) * cos(theta)
            y = radius * cos(phi)
            z = radius * sin(phi) * sin(theta)
            glVertex3f(x, y, z)
        glEnd()

def draw_hemisphere(radius, slices=16, stacks=8):
    """Dessine la demi-sphère supérieure (dôme) de rayon donné."""
    draw_sphere(radius, slices, stacks, phi_start=0.0, phi_end=pi/2)

def draw_paddle(height, width):
    """Dessine une rame (planche rectangulaire verticale) centrée à l'origine, dans le plan Y-Z, face normale vers +X."""
    half_h = height / 2.0
    half_w = width / 2.0
    glBegin(GL_QUADS)
    # On dessine un quadrilatère dans le plan Y-Z (on peut considérer les deux faces identiques sans éclairage)
    glVertex3f(0.0,  half_h, -half_w)  # coin haut-intérieur
    glVertex3f(0.0, -half_h, -half_w)  # coin bas-intérieur
    glVertex3f(0.0, -half_h,  half_w)  # coin bas-extérieur
    glVertex3f(0.0,  half_h,  half_w)  # coin haut-extérieur
    glEnd()
