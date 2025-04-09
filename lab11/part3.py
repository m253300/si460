#!/usr/bin/python3

# Load in the appropriate pyglet libraries
import pyglet
from pyglet.gl import *
import makeTopoMap as map
import numpy as np

# Define the window
window = pyglet.window.Window(600, 600, resizable=False, caption='Koutrakos - Lab 11 - Part 3')

# Define how we should draw whats inside the window
@window.event
def on_draw():
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-(rows-1)/2 - 1, (rows-1)/2 + 1, -(cols-1)/2 - 1, (cols-1)/2 + 1, -2.0, 1.0)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # draw the contour for each threshold 0.5-19.5 incrementing by 0.5
    for i in np.arange(0.5, 20.0, 1):
        drawContour(i)

def interpolate(a, b, t):
    return (t-a)/(b-a)

def drawContour(t):
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)   # White

    tlc = (-(rows-1)/2, (cols-1)/2)

    for i in range(rows-1):
        for j in range(cols-1):
            # top-left (tl) - (i, j)
            tl = map[i][j]

            # top-right (tr) - (i, j+1)
            tr = map[i][j+1]

            # bottom-right (br) - (i+1, j+1)
            br = map[i+1][j+1]

            # bottom-left (bl) - (i+1, j)
            bl = map[i+1][j]

            # check:
            # (i, j) - (i, j+1)
            # tl - tr
            if tl < t < tr or tl > t > tr:
                interp = interpolate(tl, tr, t)
                x = tlc[0] + (j+interp)
                y = tlc[1] - (i)
                glVertex3f(x, y, 0.0)

            # (i, j+1) - (i+1, j+1)
            # tr - br
            if tr < t < br or tr > t > br:
                interp = interpolate(tr, br, t)
                x = tlc[0] + (j+1)
                y = tlc[1] - (i+interp)
                glVertex3f(x, y, 0.0)

            # (i+1, j+1) - (i+1, j)
            # br - bl
            if br < t < bl or br > t > bl:
                interp = interpolate(bl, br, t)
                x = tlc[0] + (j+interp)
                y = tlc[1] - (i+1)
                glVertex3f(x, y, 0.0)

            # (i+1, j) - (i, j)
            # bl - tl
            if bl < t < tl or bl > t > tl:
                interp = interpolate(tl, bl, t)
                x = tlc[0] + (j)
                y = tlc[1] - (i+interp)
                glVertex3f(x, y, 0.0)
    glEnd()

# Begin the main program loop
map = map.get_matrix(rows = 10, cols = 10, seed = 3, delta = 3, maxval = 20)
rows = len(map)
cols = len(map[0])
pyglet.app.run()