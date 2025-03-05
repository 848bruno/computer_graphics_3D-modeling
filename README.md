# 3D Interactive Object Viewer

![3D Cube Demo](screenshot.png)

An interactive 3D viewer application implementing basic computer graphics concepts with OpenGL and Pygame.

## Features

- **3D Visualization**:
  - Renders a textured cube with perspective projection
  - Real-time transformations (translation, rotation, scaling)
  - Depth buffering for proper occlusion

- **Visual Effects**:
  - Dynamic lighting (ambient + diffuse + specular)
  - Toggleable texture/color modes
  - Automatic checkerboard texture generation
  - Wireframe overlay visualization

- **Controls**:
  - Keyboard-based transformations
  - Reset functionality
  - Texture mode switching

## Installation

1. **Prerequisites**:
   - Python 3.6+
   - pip package manager

2. **Install dependencies**:
   ```bash
   pip install pygame PyOpenGL PyOpenGL_accelerate







##

   **Run the application**:
```bash
python main.py

  ##Controls
Key	Action
Arrow Keys	X/Y Translation
Page Up/Down	Z Translation
X/Y/Z	Rotate about respective axis
+/-	Scale object
R	Reset transformations
T	Toggle texture/color mode
Customization
Textures:

Place any image file named texture.png in the project directory

Supported formats: PNG, JPG, BMP

Recommended size: 512x512 pixels

Visual Settings:

Modify vertices array in code to change cube dimensions

Adjust colors in colors tuple

Change lighting parameters in main()

Implementation Details
Core Components:

OpenGL transformation matrices

GLUT-style perspective projection

Phong-style lighting model

Texture mapping with UV coordinates

Double buffered rendering

Key Functions:

draw_cube(): Handles vertex rendering with material/texture

load_texture(): Manages texture loading/fallback

create_checkerboard_texture(): Generates default pattern

set_projection(): Configures viewing frustum

Dependencies
Pygame: Window management and input

PyOpenGL: OpenGL bindings

PyOpenGL Accelerate: Performance optimizations

License
Open-source under MIT License. Feel free to modify and distribute.