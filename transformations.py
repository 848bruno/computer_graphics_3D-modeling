from OpenGL.GL import *

def apply_transformations(translation, rotation, scale):
    glTranslatef(translation[0], translation[1], translation[2])
    glRotatef(rotation[0], 1, 0, 0)  # Rotate around X-axis
    glRotatef(rotation[1], 0, 1, 0)  # Rotate around Y-axis
    glRotatef(rotation[2], 0, 0, 1)  # Rotate around Z-axis
    glScalef(scale[0], scale[1], scale[2])
