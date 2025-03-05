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

texture_coords = (
    (0, 0), (1, 0), (1, 1), (0, 1),
    (0, 0), (1, 0), (1, 1), (0, 1)
)

# Transformation variables
translate = [0, 0, -5]
rotate = [0, 0, 0]
scale = 1.0
texture_mode = False

def load_texture(image_path):
    """Load and configure a texture image"""
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                texture_surface.get_width(),
                texture_surface.get_height(),
                0, GL_RGBA, GL_UNSIGNED_BYTE,
                texture_data)
    return texture_id

def draw_cube(texture_id):
    """Render cube with current settings"""
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    if texture_mode:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        for i, surface in enumerate(surfaces):
            for j, vertex in enumerate(surface):
                glTexCoord2fv(texture_coords[j])
                glVertex3fv(vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)
    else:
        glBegin(GL_QUADS)
        for i, surface in enumerate(surfaces):
            glColor3fv(colors[i])
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()

    # Draw wireframe edges
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def set_projection():
    """Configure perspective projection"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    global translate, rotate, scale, texture_mode

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("3D Interactive Object Viewer")

    # Load texture (replace with your image path)
    texture_id = load_texture("assets/texture.png")

    # Lighting and material setup
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
    glMaterialf(GL_FRONT, GL_SHININESS, 50)

    set_projection()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

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
                
                # Toggle texture/color mode
                if event.key == pygame.K_t: 
                    texture_mode = not texture_mode
                
                # Reset
                if event.key == pygame.K_r:
                    translate = [0, 0, -5]
                    rotate = [0, 0, 0]
                    scale = 1.0
                    texture_mode = False

        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # Apply transformations
        glLoadIdentity()
        glTranslatef(*translate)
        glRotatef(rotate[0], 1, 0, 0)
        glRotatef(rotate[1], 0, 1, 0)
        glRotatef(rotate[2], 0, 0, 1)
        glScalef(scale, scale, scale)

        draw_cube(texture_id)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()