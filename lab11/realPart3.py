import pyglet
from pyglet.gl import *
import numpy as np
import sys
import makeTopoMap as map

class Scene:
    def __init__(self, width=600, height=600, caption="Koutrakos - Lab 12", resizable=False, map=[[]]):

        self.screenshot = 0
        self.vals = [np.array([0.0, 0.0, 0.0, 0.0], dtype='float64')]
        self.width = width
        self.height = height
        self.mouseclickXYZ = np.array([0.0, 0.0, 0.0], dtype='float64')
        self.map = map

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

            glTranslatef(0.0, 0.0, -(1.2*len(self.map[0])))
            for x in reversed(self.vals):
                glRotatef(x[0], x[1], x[2], x[3])
            drawMap(self.map)

        def drawMap(map):
            for i in np.arange(0.5, 20.0, 1):
                drawContour(i, 0.3+0.05*(i-0.5), map)

        def interpolate(a, b, t):
            return (t-a)/(b-a)
        
        def drawContour(t, color, map):
            rows = len(map)
            cols = len(map[0])

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
            p2 = np.array([xp, yp, zp], dtype='float64')

            p1 = self.mouseclickXYZ

            angle = self.calcAngle(p1, p2)

            u = self.calcU(p1, p2)

            self.vals[-1]=(np.array([angle, u[0], u[1], u[2]], dtype='float64'))
        
        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            w = self.width
            h = self.height

            zp = self.calcZ(x, y)
            xp = -((w/2)-x)
            yp = y-(h/2)

            self.vals.append(np.array([0.0, 0.0, 0.0, 0.0], dtype='float64'))

            self.mouseclickXYZ = np.array([xp, yp, zp], dtype='float64')
    
    def calcZ(self, x, y):
        w = self.width
        h = self.height

        z = 0.01
        n1 = (x - (w/2.0))**2
        n2 = (y - (h/2.0))**2
        n3 = ((h/2.0)**2)

        if (n1 + n2 < n3):
            z = np.sqrt(n3 - n1 - n2)
        
        return z
    
    def calcAngle(self, p1, p2):
        return np.degrees(np.arccos((p1.dot(p2))/(np.linalg.norm(p2) * np.linalg.norm(p1))))

    def calcU(self, p1, p2):
        return (np.cross(p1, p2) / (np.linalg.norm(p2) * np.linalg.norm(p1)))
            
if __name__ == '__main__':
    map = map.get_matrix(seed = 3, rows = 100, cols = 60)
    myGame = Scene(caption="Koutrakos - Lab 11 - Part 3", map=map)
    pyglet.app.run()
