#!/usr/bin/python3 -B

# Important Libraries
import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
import time, sys, numpy, importlib

# Our world that we will draw via pyglet
class Scene:

    # Update the world time based on time elapsed in the real world
    # since we started the Scene Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        # Define current world rotations (arcball)
        self.width = width
        self.height = height
        self.P1 = numpy.array([0,0,0])
        self.P2 = numpy.array([0,0,0])
        self.theta = 0.0
        self.u = numpy.array([0,0,0])
        self.wr = []

        # Lets allow some zooming, used in conjunction with the
        # portion of code in draw that scales the world into a 100x100 area
        self.zoom = 1.0

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        # Fix transparent issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Lets set a global clock
        self.worldTime = 0.0
        self.startTime = time.time()

        # Schedule a Clock to update the time
        pyglet.clock.schedule_interval(self.updateClock, 1.0/120.0)

        # Handle Mouse Press (arcball)
        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            z = self.zxy(x,y,self.width, self.height)
            x = -1.0 * (self.width/2.0 - x)
            y = y - self.height/2.0
            self.wr.append([0.0, numpy.array([0,0,0])])
            self.P1 = numpy.array([x,y,z])

        # Handle Mouse Drag (arcball)
        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            z = self.zxy(x,y,self.width, self.height)
            x = -1.0 * (self.width/2.0 - x)
            y = y - self.height/2.0
            self.P2 = numpy.array([x,y,z])
            theta, u = self.vector_angle(self.P1, self.P2)
            self.wr[-1] = [theta, u]

        # Allow for basic zooming in our 100x100 world.
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.PAGEUP:
                self.zoom = self.zoom + 0.2
                self.zoom = max(0.1, self.zoom)
            elif symbol == key.PAGEDOWN:
                self.zoom = self.zoom - 0.2
                self.zoom = max(0.1, self.zoom)

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():

            # Clear the window (a good way to start things)
            self.window.clear()

            # Set the ViewPort and Frustum
            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 10000.0)
            glMatrixMode(gl.GL_MODELVIEW)

            # Setup the environment to handle depth
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            # Set the Modelview matrix to the identity matrix
            glLoadIdentity()

            # Translate the world to give us more space, the more
            # we push things back the smaller they start out as...
            glTranslatef(0.0,0.0,-450.0)

            # Rotate the world based on the arcball algorithm
            for r in self.wr:
                glRotatef(numpy.degrees(r[0]), r[1][0], r[1][1], r[1][2])

            # Basic World Scaling, easier than the version needed for
            # the world based on M
            glScalef(self.zoom, self.zoom, self.zoom)

            # Lets draw all of the individual objects.

    # Determine the z value based on x,y (mouse) w,h (screen) for arcball
    def zxy(self,x,y,w,h):
      if ((x - (w/2.0))**2 + (y - (h/2.0))**2) < ((h/2.0)**2):
          return numpy.sqrt((h/2.0)**2 - (x - (w/2.0))**2 - (y - (h/2.0))**2)
      return 0.01

    # Determine the appropriate vectors and angles for the arcball algorithm
    def vector_angle(self, p1, p2):
      theta = numpy.arccos((p1.dot(p2))/(numpy.linalg.norm(p2) * numpy.linalg.norm(p1)))
      u = (numpy.cross(p1, p2) / (numpy.linalg.norm(p2) * numpy.linalg.norm(p1)))
      return theta, u

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    myGame = Scene(600, 600, "Particle Simulation")
    pyglet.app.run()
