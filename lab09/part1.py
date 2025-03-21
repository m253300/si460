#!/usr/bin/python3

import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *

class Scene:
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        @self.window.event
        def on_draw():
            self.window.clear()

            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            #glOrtho(0, width, 0, height, -1, 1)
            glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
            glMatrixMode(gl.GL_MODELVIEW)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            glColor3f(1.0, 1.0, 1.0)

            gluLookAt(0.0, 0.0, 60.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
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

    # @self.window.event
    # def on_mouse_press(x, y, button, modifiers):
    #     print(str(['mouse press', x, y, "button = ", button, "modifiers = ", modifiers]))

    #     #store the x, y values because this is the first vertex
    #     if 100 < x < 500 and 100 < y < 450:
    #         point = [x, y]
    #         self.vertices.append(point)

    # @self.window.event
    # def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    #     print(str(['mouse drag', x, y, dx, dy, "buttons = ", buttons, "modifiers = ", modifiers]))

    #     #store all the x and y values
    #     if 100 < x < 500 and 100 < y < 450:
    #         point = [x, y]
    #         self.vertices.append(point)

    # @self.window.event
    # def on_mouse_release(x, y, button, modifiers):
    #     print(str(['mouse release', x, y, "button = ", button, "modifiers = ", modifiers]))

    #     #store all the x and y values
    #     if 100 < x < 500 and 100 < y < 450:
    #         point = [x, y]
    #         self.vertices.append(point)

    # @self.window.event
    # def on_key_press(symbol, modifiers):
    #     print(str(['key press', "symbol = ", symbol, "modifiers = ", modifiers]))

    #     if symbol == 99:
    #         self.vertices = []
    #     elif symbol == 113:
    #         if len(sys.argv) == 3 and sys.argv[1] == '-s':
    #             f = open(sys.argv[2], "w")
    #             for point in self.vertices:
    #                 f.write(f"{point[0]}, {point[1]}\n")
    #             f.close()
    #         sys.exit()

        # @self.window.event
        # def on_key_press(symbol, modifiers):
        #     #print(str(['key press', "symbol = ", symbol, "modifiers = ", modifiers]))

        #     if symbol == 65363: # right arrow
        #         print("right")
        #     elif symbol == 65361: # left arrow
        #         print("left")

        @self.window.event
        def on_text_motion(motion):
            #print(str(['key held down', "motion = ", motion]))
            
            if motion == 65363: # right arrow
                print("right")
            elif motion == 65361: # left arrow
                print("left")

if __name__ == '__main__':
    myGame = Scene(600, 500, "Transformations")
    # debugging = pyglet.window.event.WindowEventLogger()
    # myGame.window.push_handlers(debugging)
    pyglet.app.run()
