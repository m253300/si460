# Caleb Koutrakos (m253300)

import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
import numpy
import sys

# Our OpenGL Graphical Environment!
class Scene:

    # Initialize and run our environment
    def __init__(self, width=600, height=500, caption="Would you like to play a game?", resizable=False, vertices=[]):

        self.vertices = vertices

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        # Fix transparency issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            self.window.clear()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            label = pyglet.text.Label('Etch A Sketch',
                font_name='Times New Roman',
                font_size=24,
                x=300, y=470,
                anchor_x='center', anchor_y='center')
            label.draw()

            glBegin(GL_TRIANGLE_FAN)
            numOfSides = 50
            degAngInc = 360/numOfSides
            radAngInc = degAngInc * (numpy.pi/180)
            for i in range(numOfSides):
                x = 50 + 40 * numpy.cos(radAngInc*i)
                y = 50 + 40 * numpy.sin(radAngInc*i)
                glVertex3f(x, y, 0.0)
            glEnd()

            glBegin(GL_TRIANGLE_FAN)
            numOfSides = 50
            degAngInc = 360/numOfSides
            radAngInc = degAngInc * (numpy.pi/180)
            for i in range(numOfSides):
                x = 550 + 40 * numpy.cos(radAngInc*i)
                y = 50 + 40 * numpy.sin(radAngInc*i)
                glVertex3f(x, y, 0.0)
            glEnd()

            glBegin(GL_LINE_LOOP)
            glVertex3f(100, 100, 0.0)
            glVertex3f(100, 450, 0.0)
            glVertex3f(500, 450, 0.0)
            glVertex3f(500, 100, 0.0)
            glEnd()

            glBegin(GL_POINTS)
            for point in self.vertices:
                glVertex3f(point[0], point[1], 0.0)
            glEnd()

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            print(str(['mouse press', x, y, "button = ", button, "modifiers = ", modifiers]))

            #store the x, y values because this is the first vertex
            if 100 < x < 500 and 100 < y < 450:
                point = [x, y]
                self.vertices.append(point)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            print(str(['mouse drag', x, y, dx, dy, "buttons = ", buttons, "modifiers = ", modifiers]))

            #store all the x and y values
            if 100 < x < 500 and 100 < y < 450:
                point = [x, y]
                self.vertices.append(point)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            print(str(['mouse release', x, y, "button = ", button, "modifiers = ", modifiers]))

            #store all the x and y values
            if 100 < x < 500 and 100 < y < 450:
                point = [x, y]
                self.vertices.append(point)

        @self.window.event
        def on_key_press(symbol, modifiers):
            print(str(['key press', "symbol = ", symbol, "modifiers = ", modifiers]))

            if symbol == 99:
                self.vertices = []
            elif symbol == 113:
                if len(sys.argv) == 3 and sys.argv[1] == '-s':
                    f = open(sys.argv[2], "w")
                    for point in self.vertices:
                        f.write(f"{point[0]}, {point[1]}\n")
                    f.close()
                sys.exit()

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '-l':
        vertices = []
        f = open(sys.argv[2], "r")
        lines = f.readlines()
        for line in lines:
            vals = line.split(", ")
            point = [int(vals[0]), int(vals[1])]
            vertices.append(point)
        myGame = Scene(600, 500, "Lab 5 - Etch-a-Sketch", False, vertices)
    else:
        myGame = Scene(600, 500, "Lab 5 - Etch-a-Sketch", False)
    #debugging = pyglet.window.event.WindowEventLogger()
    #myGame.window.push_handlers(debugging)
    pyglet.app.run()
