# Caleb Koutrakos (m253300)

import pyglet
from pyglet.gl import *
import sys
import numpy
import random

# Define the window
window = pyglet.window.Window(400, 400, resizable=False, caption='Caleb Koutrakos - 253300')

# Define how we should draw whats inside the window
@window.event
def on_draw():
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 100.0, 0.0, 100.0, -2.0, 1.0)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    type = sys.argv[-1]
    print(type)
    if type == "GL_POINTS":
        glBegin(GL_POINTS)
    elif type == "GL_LINES":
        glBegin(GL_LINES)
    elif type == "GL_LINE_STRIP":
        glBegin(GL_LINE_STRIP)
    elif type == "GL_LINE_LOOP":
        glBegin(GL_LINE_LOOP)
    elif type == "GL_TRIANGLES":
        glBegin(GL_TRIANGLES)
    elif type == "GL_TRIANGLE_STRIP":
        glBegin(GL_TRIANGLE_STRIP)
    elif type == "GL_TRIANGLE_FAN":
        glBegin(GL_TRIANGLE_FAN)

    length = len(sys.argv)
    valsList = sys.argv[1:length-1]
    print(valsList)

    for i in range(0, len(valsList), 2):
        r = random.uniform(0, 1)
        g = random.uniform(0, 1)
        b = random.uniform(0, 1)
        point = valsList[i:i+2]
        x = float(point[0])
        y = float(point[1])
        glColor3f(r, g, b)
        glVertex3f(x, y, 0.0)
    
    glEnd()

# Begin the main program loop
pyglet.app.run()