from maths_utils import sin, cos, PI

def draw_cylinder(radius, height, slices=16):
    from OpenGL.GL import glBegin, glEnd, glVertex3f, GL_QUADS, GL_TRIANGLE_FAN
    half_h = height / 2.0

    glBegin(GL_QUADS)
    for i in range(slices):
        t1 = 2 * PI * i / slices
        t2 = 2 * PI * (i + 1) / slices
        x1 = radius * cos(t1); z1 = radius * sin(t1)
        x2 = radius * cos(t2); z2 = radius * sin(t2)
        glVertex3f(x1, -half_h, z1)
        glVertex3f(x1,  half_h, z1)
        glVertex3f(x2,  half_h, z2)
        glVertex3f(x2, -half_h, z2)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, half_h, 0.0)
    for i in range(slices + 1):
        t = 2 * PI * i / slices
        x = radius * cos(t); z = radius * sin(t)
        glVertex3f(x, half_h, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, -half_h, 0.0)
    for i in range(slices + 1):
        t = 2 * PI * i / slices
        x = radius * cos(t); z = radius * sin(t)
        glVertex3f(x, -half_h, z)
    glEnd()

def draw_sphere(radius, slices=16, stacks=16, phi_start=0.0, phi_end=PI):
    from OpenGL.GL import glBegin, glEnd, glVertex3f, GL_TRIANGLE_FAN, GL_QUAD_STRIP
    from maths_utils import sin, cos

    if phi_start == 0.0:
        next_phi = (phi_end - phi_start) / stacks
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, radius, 0.0)
        phi = next_phi
        for j in range(slices + 1):
            t = 2 * PI * j / slices
            x = radius * sin(phi) * cos(t)
            y = radius * cos(phi)
            z = radius * sin(phi) * sin(t)
            glVertex3f(x, y, z)
        glEnd()
        start_stack = 1
    else:
        start_stack = 0

    for i in range(start_stack, stacks - 1):
        phi1 = phi_start + (phi_end - phi_start) * i / stacks
        phi2 = phi_start + (phi_end - phi_start) * (i + 1) / stacks
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            t = 2 * PI * j / slices
            x1 = radius * sin(phi1) * cos(t)
            y1 = radius * cos(phi1)
            z1 = radius * sin(phi1) * sin(t)
            x2 = radius * sin(phi2) * cos(t)
            y2 = radius * cos(phi2)
            z2 = radius * sin(phi2) * sin(t)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
        glEnd()

    if phi_end == PI:
        phi = phi_end - (phi_end - phi_start) / stacks
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, -radius, 0.0)
        for j in range(slices + 1):
            t = 2 * PI * j / slices
            x = radius * sin(phi) * cos(t)
            y = radius * cos(phi)
            z = radius * sin(phi) * sin(t)
            glVertex3f(x, y, z)
        glEnd()

def draw_hemisphere(radius, slices=16, stacks=8):
    draw_sphere(radius, slices, stacks, 0.0, PI / 2)

def draw_paddle(height, width):
    from OpenGL.GL import glBegin, glEnd, glVertex3f, GL_QUADS
    half_h = height / 2.0
    half_w = width / 2.0
    glBegin(GL_QUADS)
    glVertex3f(0.0,  half_h, -half_w)
    glVertex3f(0.0, -half_h, -half_w)
    glVertex3f(0.0, -half_h,  half_w)
    glVertex3f(0.0,  half_h,  half_w)
    glEnd()
