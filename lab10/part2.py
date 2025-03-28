#!/usr/bin/python3 -B

# Important Libraries
import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
import time, sys, numpy, importlib, random

# Our world that we will draw via pyglet
class Scene:

    # Update the world time based on time elapsed in the real world
    # since we started the Scene Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Particle Fountain", resizable=False, particles = []):

        # Define current world rotations (arcball)
        self.width = width
        self.height = height
        self.P1 = numpy.array([0,0,0])
        self.P2 = numpy.array([0,0,0])
        self.theta = 0.0
        self.u = numpy.array([0,0,0])
        self.wr = []
        self.particles = particles
        self.screenshot = 0

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
        def on_text_motion(motion):
            if motion == key.PAGEUP:
                self.zoom = self.zoom + 0.2
                self.zoom = max(0.1, self.zoom)
            elif motion == key.PAGEDOWN:
                self.zoom = self.zoom - 0.2
                self.zoom = max(0.1, self.zoom)

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.END:
                self.screenshot = self.screenshot + 1
                pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png') 

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
            for r in reversed(self.wr):
                glRotatef(numpy.degrees(r[0]), r[1][0], r[1][1], r[1][2])

            # Basic World Scaling, easier than the version needed for
            # the world based on M
            glScalef(self.zoom, self.zoom, self.zoom)

            # Lets draw all of the individual objects.
            glTranslatef(0.0, 0.0, -60.0)
            WireCube(20.0)
            for particle in self.particles:
                particle.draw(self.worldTime)

        def WireCube(dim):
            x_min, y_min, z_min = -0.5*dim, -0.5*dim, -0.5*dim
            x_max, y_max, z_max =  0.5*dim,  0.5*dim,  0.5*dim
            glBegin(GL_LINE_STRIP)
            glVertex3f(x_min, y_min, z_min)
            glVertex3f(x_max, y_min, z_min)
            glVertex3f(x_max, y_max, z_min)
            glVertex3f(x_min, y_max, z_min)
            glVertex3f(x_min, y_min, z_min)
            glVertex3f(x_min, y_min, z_max)
            glVertex3f(x_max, y_min, z_max)
            glVertex3f(x_max, y_max, z_max)
            glVertex3f(x_min, y_max, z_max)
            glVertex3f(x_min, y_min, z_max)
            glVertex3f(x_min, y_max, z_max)
            glVertex3f(x_min, y_max, z_min)
            glVertex3f(x_max, y_max, z_min)
            glVertex3f(x_max, y_max, z_max)
            glVertex3f(x_max, y_min, z_max)
            glVertex3f(x_max, y_min, z_min)
            glEnd()

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
    
class Particle:
    def __init__(self, thetaMin, thetaMax, S):
        theta = random.uniform(thetaMin, thetaMax)
        phi = numpy.radians(random.uniform(0, 360))
        self.acceleration = numpy.array([0.0, -9.8, 0.0])
        self.tlag = random.uniform(0, 60)
        self.initialposition = numpy.array([0.0, 0.0, 0.0])

        alpha = theta/thetaMax
        theta = numpy.radians(theta)
        V = numpy.array([numpy.sin(theta) * numpy.sin(phi), numpy.cos(theta), numpy.sin(theta) * numpy.cos(phi)])
        self.initialvelocity = S*(1-alpha**2)*V

    def draw(self, t):
        #if t is greater than or equal to tlag then we draw
        if t >= self.tlag:
            #use glbegin and whatnot to draw
            glBegin(GL_POINTS)
            position = self.initialposition + self.initialvelocity * t + 0.5 * self.acceleration * t**2
            glVertex3f(position[0], position[1], position[2])
            glEnd()

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    particles = []
    for x in range(0, 1000):
        particles.append(Particle(0.0, 20.0, 90.0))
    myGame = Scene(600, 600, "Particle Simulation", particles=particles)
    pyglet.app.run()
