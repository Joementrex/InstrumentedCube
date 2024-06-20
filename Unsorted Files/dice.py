import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define sensor positions for each face
sensor_positions = [
    [(0, 0, 0)],  # Center sensor
    [(0.5, 0.5, 0), (-0.5, 0.5, 0), (-0.5, -0.5, 0), (0.5, -0.5, 0)]  # Corner sensors
] * 6  # Repeat for each face

# Simulate sensor values (0-100) for each sensor
sensor_values = [random.randint(0, 100) for _ in range(30)]

def draw_cube():
    glBegin(GL_POINTS)
    for face_index, positions in enumerate(sensor_positions):
        for i, (x, y, z) in enumerate(positions):
            glColor3f(sensor_values[face_index * 5 + i] / 100.0, 0.0, 1.0 - sensor_values[face_index * 5 + i] / 100.0)
            glVertex3f(x, y, z)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    draw_cube()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b'3D Cube with Sensors')
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == '__main__':
    main()
