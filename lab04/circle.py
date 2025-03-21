# Caleb Koutrakos (m253300)

import pyglet
from pyglet.gl import *
import sys
import numpy

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

    glBegin(GL_LINE_LOOP)

    numOfSides = int(sys.argv[1])
    #print(numOfSides)
    degAngInc = 360/numOfSides
    #print(degAngInc)
    radAngInc = degAngInc * (numpy.pi/180)
    #print(radAngInc)
    for i in range(numOfSides):
        #math to calc x and y
        x = 50 + 25 * numpy.cos(radAngInc*i)
        y = 50 + 25 * numpy.sin(radAngInc*i)
        #print("(" + str(x) + ", " + str(y) + ")")
        glVertex3f(x, y, 0.0)
    
    glEnd()

# Begin the main program loop
pyglet.app.run()