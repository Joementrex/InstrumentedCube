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

text = "None"


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
    elif face == 'None':
        change_all_face_colors(GREY)

# Tuple of RGB colours for each square of each face of the cube 
# 6 faces * 4 squares per face * 3 RGB values per square
BLUE = [0.0, 0.0, 1.0]

SQUARE_COLORS = [BLUE for _ in range(6 * 4)]

def draw_squares():
    "Draw small red squares on each face of the cube"
    square_size = 0.1
    square_half = square_size / 2
    face_centers = [
        [(0.25, 0.25, 0.5), (0.25, -0.25, 0.5), (-0.25, 0.25, 0.5), (-0.25, -0.25, 0.5)],  # Front
        [(0.25, 0.25, -0.5), (0.25, -0.25, -0.5), (-0.25, 0.25, -0.5), (-0.25, -0.25, -0.5)],  # Back
        [(0.25, 0.5, 0.25), (0.25, 0.5, -0.25), (-0.25, 0.5, 0.25), (-0.25, 0.5, -0.25)],  # Top
        [(0.25, -0.5, 0.25), (0.25, -0.5, -0.25), (-0.25, -0.5, 0.25), (-0.25, -0.5, -0.25)],  # Bottom
        [(0.5, 0.25, 0.25), (0.5, 0.25, -0.25), (0.5, -0.25, 0.25), (0.5, -0.25, -0.25)],  # Right
        [(-0.5, 0.25, 0.25), (-0.5, 0.25, -0.25), (-0.5, -0.25, 0.25), (-0.5, -0.25, -0.25)]   # Left
    ]

    for i, centers in enumerate(face_centers):
        # glColor3f(1.0, 0.0, 0.0)
        for center in centers:
            glPushMatrix()
            glTranslatef(*center)
            if i == 0:  # Front
                pass  # No rotation needed
            elif i == 1:  # Back
                glRotatef(180, 0, 1, 0)
            elif i == 2:  # Top
                glRotatef(90, 1, 0, 0)
            elif i == 3:  # Bottom
                glRotatef(-90, 1, 0, 0)
            elif i == 4:  # Right
                glRotatef(-90, 0, 1, 0)
            elif i == 5:  # Left
                glRotatef(90, 0, 1, 0)

            if i == 0 or i == 1:
                z = 0.1
            else:
                z = -0.1
            glBegin(GL_QUADS)
            # print(SQUARE_COLORS)
            # print(' ')
            glColor3fv(SQUARE_COLORS[i * 4 + centers.index(center)])
            glVertex3f(-square_half, -square_half, z)
            glVertex3f(square_half, -square_half, z)
            glVertex3f(square_half, square_half, z)
            glVertex3f(-square_half, square_half, z)
            glEnd()
            glPopMatrix()

def drawText(x, y, text):    
    font = pygame.font.Font(None, 36)                                     
    textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def drawTextPos(pos):
    global text
    text = f'Pos: {pos}'

def change_square_color(face, square_index, square_index2):
    global SQUARE_COLORS
    square_index = square_index - 1
    square_index2 = square_index2 - 1

    # # Change face index to index of SQUARE_COLORS 
    # # Receive: 0 is top, 1 is front, 2 is left, 3 is right, 4 is back
    # # Change to: 2 is top, 0 is front, 3 is left, 1 is right, 4 is back
    # face_index = [2, 0, 3, 1, 4][face_index]

    # Set all squares to blue
    for i in range(6):
        for j in range(4):
            SQUARE_COLORS[i * 4 + j] = BLUE

    if face == 'None':
        # Set all squares to blue
        for i in range(6):
            for j in range(4):
                SQUARE_COLORS[i * 4 + j] = BLUE
        return

    if face == 'Top':
        face_index = 2
        # Where 1 is top left, 2 is top right, 3 is bottom left, 4 is bottom right
        # Change to where 4 is top left, 2 is top right, 3 is bottom left, 1 is bottom right
        square_index = [3, 1, 2, 0][square_index]
        if square_index2 != -1:
            square_index2 = [3, 1, 2, 0][square_index2]
    elif face == 'Front':
        face_index = 0
        # Where top left is 1, top right is 2, bottom left is 3, bottom right is 4
        # Change to top right is 0, bottom right is 1, top left is 2, bottom left is 3
        square_index = [2, 0, 3, 1][square_index]
        if square_index2 != -1:
            square_index2 = [2, 0, 3, 1][square_index2]
    elif face == 'Left':
        face_index = 5
        # Where top left is 1, top right is 2, bottom left is 3, bottom right is 4
        # Change to top right is 1, bottom right is 0, 3 is top left, 2 is bottom left
        square_index = [1, 0, 3, 2][square_index]
        if square_index2 != -1:
            square_index2 = [1, 0, 3, 2][square_index2]
    elif face == 'Right':
        face_index = 4
        # Where top left is 1, top right is 2, bottom left is 3, bottom right is 4
        # Change to top right is 0, bottom right is 1, 3 is top left, 2 is bottom left
        square_index = [0, 1, 2, 3][square_index]
        if square_index2 != -1:
            square_index2 = [0, 1, 2, 3][square_index2]
    elif face == 'Back':
        face_index = 1
        # Where top left is 1, top right is 2, bottom left is 3, bottom right is 4
        # Change to top left is 0, 1 is bottom left, 2 is top right, 3 is bottom right
        square_index = [0, 2, 1, 3][square_index]
        if square_index2 != -1:
            square_index2 = [0, 2, 1, 3][square_index2]

    if 0 <= face_index < 6 and 0 <= square_index < 4:
        # print("\033[H\033[J")
        # print('Square index:', square_index)
        # print('Square index 2:', square_index2)
        # print(' ')
        # Set all squares to blue
        for i in range(6):
            for j in range(4):
                SQUARE_COLORS[i * 4 + j] = BLUE
        SQUARE_COLORS[face_index * 4 + square_index] = [1.0, 0.0, 0.0]
        if square_index2 != -1:
            SQUARE_COLORS[face_index * 4 + square_index2] = [1.0, 0.0, 0.0]
    # # For second square
    # if 0 <= face_index < 6 and 0 <= square_index2 < 4:
    #     SQUARE_COLORS[face_index * 4 + square_index2] = [1.0, 0.0, 0.0]
    # elif square_index2 == -1:
    #     pass

def main():
    pygame.init()
    pygame.font.init()
    # global font
    # font = pygame.font.Font(None, 36)
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
        if keys[pygame.K_w]:
            glRotatef(1, 1, 0, 0)  # Rotate up
        if keys[pygame.K_s]:
            glRotatef(1, -1, 0, 0)  # Rotate down
        if keys[pygame.K_a]:
            glRotatef(1, 0, -1, 0)  # Rotate left
        if keys[pygame.K_d]:
            glRotatef(1, 0, 1, 0)  # Rotate right

        # Draw text at the top left of the screen saying SAMPLE TEXT
        
        # drawText(10, 10, "SAMPLE TEXT")


        # Change the color of the square on the front face of the cube
        if keys[pygame.K_1]:
            SQUARE_COLORS[0] = [1.0, 0.0, 0.0]
            SQUARE_COLORS[1] = [0.0, 1.0, 0.0]
            SQUARE_COLORS[2] = [0.0, 0.0, 1.0]
            SQUARE_COLORS[3] = [1.0, 1.0, 1.0]

        draw_squares()
        drawText(0, 0, text)
        drawcube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__': main()
