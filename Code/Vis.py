#!/usr/bin/env python

"""Draw a cube on the screen. every frame we orbit
the camera around by a small amount and it appears
the object is spinning. note i've setup some simple
data structures here to represent a multicolored cube,
we then go through a semi-unopimized loop to draw
the cube points onto the screen. opengl does all the
hard work for us. :]
"""

import pygame
from pygame.locals import *


from OpenGL.GL import *
from OpenGL.GLU import *


# Some simple data for a colored cube
CUBE_POINTS = (
    (0.5, -0.5, -0.5),  (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),  (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),   (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),  (-0.5, 0.5, 0.5)
)

# Colors are 0-1 floating values
CUBE_COLORS = [
    [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]
]

CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

GREEN = [0, 1, 0]
GREY = [0.5, 0.5, 0.5]

def drawcube():
    "Draw the cube"
    allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))

    glBegin(GL_QUADS)
    for face_index, face in enumerate(CUBE_QUAD_VERTS):
        color = CUBE_COLORS[face_index]  # Get the color for this face
        glColor3fv(color)
        for vert in face:
            pos, _ = allpoints[vert]
            glVertex3fv(pos)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, _ = allpoints[vert]
            glVertex3fv(pos)
    glEnd()

        # Draw XYZ axis
    glBegin(GL_LINES)
    # X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    # Y axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    # Z axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()

def change_face_color(face_index, color):
    global CUBE_COLORS
    if 0 <= face_index < len(CUBE_COLORS):
        CUBE_COLORS[face_index] = color

def change_all_face_colors(color):
    global CUBE_COLORS
    CUBE_COLORS = [color for _ in CUBE_COLORS]

def colour_face(face):
    # Change all faces to grey
    change_all_face_colors(GREY)
    if face == 'Top':
        change_face_color(4, GREEN)
    elif face == 'Front':
        change_face_color(2, GREEN)
    elif face == 'Right':
        change_face_color(3, GREEN)
    elif face == 'Left':
        change_face_color(1, GREEN)
    elif face == 'Back':
        change_face_color(0, GREEN)


def main():
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)        # Use our zbuffer

    # Setup the camera
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,640/480.0,0.1,100.0)    # Setup lens
    glTranslatef(0.0, 0.0, -3.0)                # Move back
    glRotatef(25, 1, 0, 0)                       # Orbit higher

    while 1:
        # Check for quit'n events
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        # Clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Orbit camera around by 1 degree
        # glRotatef(1, 0, 1, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            colour_face('Top')
        if keys[pygame.K_2]:
            colour_face('Front')
        if keys[pygame.K_3]:
            colour_face('Right')
        if keys[pygame.K_4]:
            colour_face('Left')
        if keys[pygame.K_5]:
            colour_face('Back')


        if keys[pygame.K_w]:
            glRotatef(1, 1, 0, 0)  # Rotate up
        if keys[pygame.K_s]:
            glRotatef(1, -1, 0, 0)  # Rotate down
        if keys[pygame.K_a]:
            glRotatef(1, 0, -1, 0)  # Rotate left
        if keys[pygame.K_d]:
            glRotatef(1, 0, 1, 0)  # Rotate right

        drawcube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__': main()
