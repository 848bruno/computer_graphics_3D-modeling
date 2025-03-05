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
mouse_dragging = False
last_mouse_pos = (0, 0)

def create_checkerboard_texture():
    """Generate a 64x64 checkerboard pattern"""
    texture_size = 64
    checkerboard = pygame.Surface((texture_size, texture_size))
    dark = (50, 50, 150, 255)
    light = (200, 200, 250, 255)
    
    for y in range(texture_size):
        for x in range(texture_size):
            color = dark if (x//8 + y//8) % 2 else light
            checkerboard.set_at((x, y), color)
    return checkerboard

def load_texture(image_path):
    """Load texture with enhanced handling"""
    try:
        try:
            texture_surface = pygame.image.load(image_path)
        except pygame.error:
            texture_surface = create_checkerboard_texture()
        
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Improved texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA,
                        texture_surface.get_width(),
                        texture_surface.get_height(),
                        GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        return texture_id
    except Exception as e:
        print(f"Texture error: {e}")
        return None

def draw_cube(texture_id):
    """Render cube with improved texture handling"""
    if texture_id and texture_mode:
        glDisable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor3f(1, 1, 1)  # Reset color for proper texture
        glBegin(GL_QUADS)
        for surface in surfaces:
            for i, vertex in enumerate(surface):
                glTexCoord2fv(texture_coords[i])
                glVertex3fv(vertices[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)
    else:
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
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
    global translate, rotate, scale, texture_mode, mouse_dragging, last_mouse_pos

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("3D Interactive Object Viewer")

    texture_id = load_texture("assets/texture.jpg")

    # Enhanced lighting setup
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (2, 2, 2, 1))  # Better position
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))  # Increased ambient
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))  # Stronger diffuse
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.5, 0.5, 0.5, 1))  # Adjusted specular
    glMaterialf(GL_FRONT, GL_SHININESS, 50)

    set_projection()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_dragging = True
                    last_mouse_pos = event.pos
                elif event.button == 4:  # Mouse wheel up
                    translate[2] += 0.5
                elif event.button == 5:  # Mouse wheel down
                    translate[2] -= 0.5

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_dragging = False

            if event.type == pygame.MOUSEMOTION and mouse_dragging:
                x, y = event.pos
                dx = x - last_mouse_pos[0]
                dy = y - last_mouse_pos[1]
                rotate[0] += dy * 0.5
                rotate[1] += dx * 0.5
                last_mouse_pos = (x, y)

            # Keyboard controls
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

        # Rendering
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
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