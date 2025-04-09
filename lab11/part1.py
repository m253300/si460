#!/usr/bin/python3

# Load in the appropriate pyglet libraries
import pyglet
from pyglet.gl import *
import makeTopoMap as map

# Define the window
window = pyglet.window.Window(600, 600, resizable=False, caption='ex1.py')

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

    tlc = (-(rows-1)/2, (cols-1)/2)

    # implement algorithm to go through the matrix x
    glBegin(GL_POINTS)

    # Mark center with blue dot
    glColor3f(0.0, 0.0, 1.0)   # Blue
    glVertex3f(0.0, 0.0, 0.0)
    #glEnd()

    # Create grid with white dots
    glColor3f(1.0, 1.0, 1.0)   # White
    for i in range(rows):
        for j in range(cols):
            glVertex3f(tlc[0] + i, tlc[1] - j, 0.0)
    glEnd()

    label = pyglet.text.Label('Z',
            font_name='Times New Roman',
            font_size=2,
            x=0, y=0,
            anchor_x='center', anchor_y='center')
    label.draw()

    # Mark passes of the threshold with red dots
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)   # Red
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
            if tl < threshold < tr:
                x = tlc[0] + (i+0.5)
                y = tlc[1] - (j)
                print(f"({tl}, {tr}) @ ({x}, {y})")
                glVertex3f(x, y, 0.0)

            # (i, j+1) - (i+1, j+1)
            # tr - br
            if tr < threshold < br:
                x = tlc[0] + (i+1)
                y = tlc[1] - (j+0.5)
                print(f"({tr}, {br}) @ ({x}, {y})")
                glVertex3f(x, y, 0.0)

            # (i+1, j+1) - (i+1, j)
            # br - bl
            if br < threshold < bl:
                x = tlc[0] + (i+1)
                y = tlc[1] - (j+0.5)
                print(f"({br}, {bl}) @ ({x}, {y})")
                glVertex3f(x, y, 0.0)

            # (i+1, j) - (i, j)
            # bl - tl
            if bl < threshold < tl:
                x = tlc[0] + (i)
                y = tlc[1] - (j+0.5)
                print(f"({bl}, {tl}) @ ({x}, {y})")
                glVertex3f(x, y, 0.0)
    glEnd()

        

# Begin the main program loop
map = map.get_matrix(rows = 10, cols = 10, seed = 3, delta = 3, maxval = 20)
threshold = 6.5
print(map)
rows = len(map)
cols = len(map[0])
pyglet.app.run()