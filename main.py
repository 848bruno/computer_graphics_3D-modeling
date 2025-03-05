# main.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Cube vertex coordinates and surfaces
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Cyan
)

# Transformation variables
translate = [0, 0, -5]
rotate = [0, 0, 0]
scale = 1.0

def draw_cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def set_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    global translate, rotate, scale

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("3D Interactive Object Viewer")

    set_projection()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # Enable depth testing and lighting
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                # Translation
                if event.key == pygame.K_LEFT: translate[0] -= 0.1
                if event.key == pygame.K_RIGHT: translate[0] += 0.1
                if event.key == pygame.K_UP: translate[1] += 0.1
                if event.key == pygame.K_DOWN: translate[1] -= 0.1
                if event.key == pygame.K_PAGEUP: translate[2] += 0.1
                if event.key == pygame.K_PAGEDOWN: translate[2] -= 0.1

                # Rotation
                if event.key == pygame.K_x: rotate[0] += 5
                if event.key == pygame.K_y: rotate[1] += 5
                if event.key == pygame.K_z: rotate[2] += 5
                
                # Scaling
                if event.key == pygame.K_PLUS: scale += 0.1
                if event.key == pygame.K_MINUS: scale -= 0.1
                
                # Reset
                if event.key == pygame.K_r:
                    translate = [0, 0, -5]
                    rotate = [0, 0, 0]
                    scale = 1.0

        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # Apply transformations
        glLoadIdentity()
        glTranslatef(*translate)
        glRotatef(rotate[0], 1, 0, 0)
        glRotatef(rotate[1], 0, 1, 0)
        glRotatef(rotate[2], 0, 0, 1)
        glScalef(scale, scale, scale)

        draw_cube()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()