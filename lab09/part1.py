import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
import numpy as py
import sys

class Scene:
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        self.cameraX = 0.0
        self.cameraZ = 60.0
        self.angle = 0.0
        self.screenshot = 0

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

            gluLookAt(self.cameraX, 0.0, self.cameraZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
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
        def on_text_motion(motion):
            #print(str(['key held down', "motion = ", motion]))
            
            if motion == 65363: # right arrow
                self.angle += 1
            elif motion == 65361: # left arrow
                self.angle -= 1
            
            self.cameraX = 0.0 + 60.0*py.cos(self.angle*(py.pi/180))
            self.cameraZ = 0.0 + 60.0*py.sin(self.angle*(py.pi/180))

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.END:
                self.screenshot = self.screenshot + 1
                pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png')

if __name__ == '__main__':
    myGame = Scene(600, 500, "Transformations")
    # debugging = pyglet.window.event.WindowEventLogger()
    # myGame.window.push_handlers(debugging)
    pyglet.app.run()