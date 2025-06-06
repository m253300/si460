#!/usr/bin/python3

# Load in the appropriate pyglet libraries
import pyglet
from pyglet.gl import *
import makeTopoMap as map
import numpy as np

class Scene:
    def __init__(self, width=600, height=600, caption='Koutrakos - Lab 11 - Part 3', resizable=False):

        # Define the window
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        # Define how we should draw whats inside the window
        @self.window.event
        def on_draw():
            # self.window.clear()

            # glViewport(0, 0, width, height)
            # glMatrixMode(gl.GL_PROJECTION)
            # glLoadIdentity()
            # glFrustum(-cols/4, cols/4, -rows/4, rows/4, 0.5, 20)
            # glMatrixMode(gl.GL_MODELVIEW)

            # glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            # glLoadIdentity()

            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            if cols > rows:
                glOrtho(-cols/2, cols/2, -cols/2, cols/2, -20.0, 0)
            else:
                glOrtho(-rows/2, rows/2, -rows/2, rows/2, -20.0, 0)
            
            glMatrixMode(gl.GL_MODELVIEW)
            glLoadIdentity()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            #gluLookAt(0.0, -0.1, 0.4, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

            # draw the contour for each threshold 0.5-19.5 incrementing by 0.5
            for i in np.arange(0.5, 20.0, 1):
                drawContour(i, 0.3+0.05*(i-0.5))

        def interpolate(a, b, t):
            return (t-a)/(b-a)

        def drawContour(t, color):
            glBegin(GL_LINES)
            glColor3f(color, color, color)   # Shades of gray

            tlc = (-(cols-1)/2, (rows-1)/2)

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
                        glVertex3f(x, y, t)

                    # (i, j+1) - (i+1, j+1)
                    # tr - br
                    if tr < t < br or tr > t > br:
                        interp = interpolate(tr, br, t)
                        x = tlc[0] + (j+1)
                        y = tlc[1] - (i+interp)
                        glVertex3f(x, y, t)

                    # (i+1, j+1) - (i+1, j)
                    # br - bl
                    if br < t < bl or br > t > bl:
                        interp = interpolate(bl, br, t)
                        x = tlc[0] + (j+interp)
                        y = tlc[1] - (i+1)
                        glVertex3f(x, y, t)

                    # (i+1, j) - (i, j)
                    # bl - tl
                    if bl < t < tl or bl > t > tl:
                        interp = interpolate(tl, bl, t)
                        x = tlc[0] + (j)
                        y = tlc[1] - (i+interp)
                        glVertex3f(x, y, t)
            glEnd()

# Begin the main program loop
map = map.get_matrix(seed = 3, rows = 100, cols = 60)
rows = len(map)
cols = len(map[0])
myScene = Scene(600, 600)
pyglet.app.run()