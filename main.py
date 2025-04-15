import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from camera import Camera
from maxim import Maxim
import maths_utils as mu
import geometry

def draw_text(x, y, text, font, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    surface = surface.convert_alpha()  # ← Garde l’alpha (important)
    text_data = pygame.image.tostring(pygame.transform.flip(surface, False, True), "RGBA", True)
    w, h = surface.get_size()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glColor4f(1, 1, 1, 1)  # ← transparence active
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + w, y)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x, y + h)
    glEnd()

    glDeleteTextures([tex_id])
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# 🎮 Init
pygame.init()
width, height = 1280, 720
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Arche Maxim")
font = pygame.font.Font("SPACE.otf", 20)  # ← police par défaut toujours dispo

# 🌕 Moon & Earth
moon_position = [0.0, 0.0, 1000.0]
moon_radius = 5.0
earth_position = [0.0, 0.0, 0.0]
earth_mass = 1000.0
earth_radius = 10.0

# 🚀 Arche & Cam
ark = Maxim(position=[0.0, 0.0, -earth_radius - 2.0], radius=2.0, height=4.0)
ark.set_velocity_towards(moon_position, speed=11.2)
cam = Camera(target=ark, distance=30.0, height=8.0)

# ✨ Stars
stars = []
for _ in range(2000):
    x = random.uniform(-150, 150)
    y = random.uniform(-150, 150)
    z = random.uniform(-50, moon_position[2] + 100)
    b = random.uniform(0.3, 1.0)
    amp = random.uniform(0.1, 0.4)
    freq = random.uniform(0.5, 3.0)
    phase = random.uniform(0.0, 2 * mu.PI)
    stars.append([x, y, z, b, amp, freq, phase])

# 🎨 OpenGL
glEnable(GL_DEPTH_TEST)
glClearColor(0.0, 0.0, 0.0, 1.0)
glPointSize(2)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45.0, width / float(height), 0.1, 500.0)
glMatrixMode(GL_MODELVIEW)

# 🕒 Loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    ark.apply_gravity_from(earth_position, earth_mass, earth_radius, moon_position)
    if ark.escaped_earth and not ark.stopped:
        ark.mouvement([0.0, 0.0, -1.5], [ark.radius, 0.0, 0.0], dt)
    ark.update(dt, moon_position, moon_radius)
    cam.update()

    # --- 3D Rendu ---
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    cam.look()

    glPushMatrix()
    glTranslatef(*earth_position)
    glColor3f(0.0, 0.2, 1.0)
    geometry.draw_sphere(earth_radius, 32, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(*moon_position)
    glColor3f(0.8, 0.8, 0.8)
    geometry.draw_sphere(moon_radius, 32, 16)
    glPopMatrix()

    ark.draw()

    # --- Flèche de vitesse 3D (vers la lune) ---
    glLineWidth(2)
    glColor3f(0.0, 1.0, 0.0)  # vert
    glBegin(GL_LINES)
    glVertex3f(*ark.position)
    end_point = mu.vector_add(ark.position, mu.vector_scale(ark.velocity, 4))
    glVertex3f(*end_point)
    glEnd()

    v = mu.vector_scale(mu.normalize3d(ark.velocity), 0.5)
    side1 = [v[1], -v[0], 0]
    side2 = [-v[1], v[0], 0]
    tip = mu.vector_add(end_point, v)
    left = mu.vector_add(end_point, side1)
    right = mu.vector_add(end_point, side2)

    glBegin(GL_TRIANGLES)
    glVertex3f(*tip)
    glVertex3f(*left)
    glVertex3f(*right)
    glEnd()

    # --- Étoiles scintillantes ---
    t = pygame.time.get_ticks() / 1000.0
    glBegin(GL_POINTS)
    for x, y, z, b, a, f, p in stars:
        flicker = a * mu.sin(f * t + p)
        brightness = max(0.0, min(1.0, b + flicker))
        glColor3f(brightness, brightness, brightness)
        glVertex3f(x, y, z)
    glEnd()

    # --- UI texte haut droite ---
    lines = []
    if ark.escaped_earth:
        lines.append(f"Temps: {ark.escape_timer:.1f}s")
    lines.append(f"Vitesse: {mu.vector_length(ark.velocity):.2f}")
    lines.append(f"Distance: {mu.distance3d(ark.position, moon_position):.1f}")
    for i, line in enumerate(lines):
        draw_text(width - 200, 20 + i * 25, line, font)

    # --- UI flèches de forces (2D) ---
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)

    for i, (_, F) in enumerate(ark.ui_forces):
        x0 = 60
        y0 = height - 80 - i * 40
        fx = F[0] * 200  # ← flèche plus longue
        fy = F[1] * 200
        glLineWidth(4)
        glColor3f(1.0, 0.0, 0.0)

        # Flèche rouge principale
        glBegin(GL_LINES)
        glVertex2f(x0, y0)
        glVertex2f(x0 + fx, y0 + fy)
        glEnd()

        # Tête de flèche
        angle = mu.atan2(fy, fx)
        arrow_size = 35
        left = [x0 + fx - arrow_size * mu.cos(angle - 0.3), y0 + fy - arrow_size * mu.sin(angle - 0.3)]
        right = [x0 + fx - arrow_size * mu.cos(angle + 0.3), y0 + fy - arrow_size * mu.sin(angle + 0.3)]

        glBegin(GL_TRIANGLES)
        glVertex2f(x0 + fx, y0 + fy)
        glVertex2f(*left)
        glVertex2f(*right)
        glEnd()

    ark.ui_forces.clear()

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    pygame.display.flip()

pygame.quit()
