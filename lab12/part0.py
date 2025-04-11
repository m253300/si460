import pyglet
from pyglet.gl import *
import numpy as py
import sys

class Scene:
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        self.screenshot = 0
        self.vals = [py.array([0.0, 0.0, 0.0, 0.0], dtype='float64')]
        self.width = width
        self.height = height
        self.mouseclickXYZ = py.array([0.0, 0.0, 0.0], dtype='float64')

        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        @self.window.event
        def on_draw():
            self.window.clear()

            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
            glMatrixMode(gl.GL_MODELVIEW)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            glColor3f(1.0, 1.0, 1.0)

            glTranslatef(0.0, 0.0, -60.0)
            for x in reversed(self.vals):
                glRotatef(x[0], x[1], x[2], x[3])
            WireCube(20.0)

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

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.END:
                self.screenshot = self.screenshot + 1
                pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png') 

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            w = self.width
            h = self.height

            zp = self.calcZ(x, y)
            xp = -((w/2)-x)
            yp = y-(h/2)
            p2 = py.array([xp, yp, zp], dtype='float64')

            p1 = self.mouseclickXYZ

            angle = self.calcAngle(p1, p2)

            u = self.calcU(p1, p2)

            self.vals[-1]=(py.array([angle, u[0], u[1], u[2]], dtype='float64'))
        
        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            w = self.width
            h = self.height

            zp = self.calcZ(x, y)
            xp = -((w/2)-x)
            yp = y-(h/2)

            self.vals.append(py.array([0.0, 0.0, 0.0, 0.0], dtype='float64'))

            self.mouseclickXYZ = py.array([xp, yp, zp], dtype='float64')
    
    def calcZ(self, x, y):
        w = self.width
        h = self.height

        z = 0.01
        n1 = (x - (w/2.0))**2
        n2 = (y - (h/2.0))**2
        n3 = ((h/2.0)**2)

        if (n1 + n2 < n3):
            z = py.sqrt(n3 - n1 - n2)
        
        return z
    
    def calcAngle(self, p1, p2):
        return py.degrees(py.arccos((p1.dot(p2))/(py.linalg.norm(p2) * py.linalg.norm(p1))))

    def calcU(self, p1, p2):
        return (py.cross(p1, p2) / (py.linalg.norm(p2) * py.linalg.norm(p1)))
            
if __name__ == '__main__':
    myGame = Scene(600, 500, "Transformations")
    pyglet.app.run()
