from OpenGL.GL import *

# Define vertices and edges of a cube
vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
    [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]   # Front face
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Function to draw the cube
def draw_cube():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)  # White lines
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
