import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
import numpy as py
import sys

class Scene:
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        self.density = 10
        self.cameraX = 0.0
        self.cameraZ = 60.0
        self.angle = 90.0
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
            PointCloud(30.0)

        def PointCloud(radius):
            stepSizeX = self.density
            stepSizeY = self.density

            glBegin(GL_POINTS)

            for angleX in range(0, 360, stepSizeX):
                angX = angleX*(py.pi/180)
                for angleY in range(0, 180, stepSizeY):
                    angY = angleY*(py.pi/180)
                    # Solve for x, y, z
                    x = 0.0 + radius * py.cos(angX)*py.sin(angY)
                    y = 0.0 + radius * py.sin(angX)*py.sin(angY)
                    z = 0.0 + radius * py.cos(angY)
                    glVertex3f(x,y,z)

            glEnd()

        @self.window.event
        def on_text_motion(motion):
            #print(str(['key held down', "motion = ", motion]))
            
            if motion == 65362: # up arrow
                self.density -= 1
            elif motion == 65364: # down arrow
                self.density += 1
            elif motion == 65363: # right arrow
                self.angle += 1
                self.cameraX = 0.0 + 60.0*py.cos(self.angle*(py.pi/180))
                self.cameraZ = 0.0 + 60.0*py.sin(self.angle*(py.pi/180))
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
    #debugging = pyglet.window.event.WindowEventLogger()
    #myGame.window.push_handlers(debugging)
    pyglet.app.run()