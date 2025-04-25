import pyglet
from pyglet.gl import *
import numpy as np
import sys

class Scene:
    def __init__(self, width=600, height=600, caption="Koutrakos - Lab 12", resizable=False, map=[[]], zoom=20):

        self.screenshot = 0
        self.vals = [np.array([0.0, 0.0, 0.0, 0.0], dtype='float64')]
        self.width = width
        self.height = height
        self.mouseclickXYZ = np.array([0.0, 0.0, 0.0], dtype='float64')
        self.map = map
        self.zoom = zoom

        self.typing = 0
        self.number = []
        self.row = 0
        self.col = 0
        self.newHeight = 0

        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        @self.window.event
        def on_draw():
            self.window.clear()

            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 2000.0)
            glMatrixMode(gl.GL_MODELVIEW)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            glColor3f(1.0, 1.0, 1.0)

            glTranslatef(0.0, 0.0, -6.5*self.zoom)
            glScalef(5., 5., 2.)
            for x in reversed(self.vals):
                glRotatef(x[0], x[1], x[2], x[3])
            drawMesh(self.map)

        def colorDict(map):
            flatMap = [item for sublist in map for item in sublist]
            flatMapUnique = list(set(flatMap))
            flatMapUnique.sort()
            inc = 0.7/len(flatMapUnique)
            colors = {}

            i = 0
            for x in flatMapUnique:
                colors[x] = (0.3 + inc*i)
                i+=1

            return colors

        def drawMesh(map):
            rows = len(map)
            cols = len(map[0])

            tlc = (-(cols-1)/2, (rows-1)/2)

            colors = colorDict(map)

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

                    #tl, tr, bl
                    glBegin(GL_TRIANGLES)
                    glColor3f(colors[tl], colors[tl], colors[tl])
                    glVertex3f(tlc[0] + j, tlc[1] - i, tl)

                    glColor3f(colors[tr], colors[tr], colors[tr])
                    glVertex3f(tlc[0] + j + 1, tlc[1] - i, tr)

                    glColor3f(colors[bl], colors[bl], colors[bl])
                    glVertex3f(tlc[0] + j, tlc[1] - (i + 1), bl)
                    glEnd()

                    #tr, bl, br
                    glBegin(GL_TRIANGLES)
                    glColor3f(colors[tr], colors[tr], colors[tr])
                    glVertex3f(tlc[0] + j + 1, tlc[1] - i, tr)

                    glColor3f(colors[bl], colors[bl], colors[bl])
                    glVertex3f(tlc[0] + j, tlc[1] - (i + 1), bl)

                    glColor3f(colors[br], colors[br], colors[br])
                    glVertex3f(tlc[0] + j + 1, tlc[1] - (i + 1), br)
                    glEnd()

        @self.window.event
        def on_key_press(symbol, modifiers):
            if not self.typing:
                if symbol == pyglet.window.key.END:
                    self.screenshot = self.screenshot + 1
                    pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png')

            if symbol == pyglet.window.key.ENTER:
                self.typing += 1
                if self.typing == 1:
                    self.row = 0
                    self.col = 0
                    self.newHeight = 0
                    self.number = []
                    print("Enter row # to edit")
                elif self.typing == 2:
                    self.row = concatNums(self.number)
                    self.number = []
                    print(f"Row: {self.row}")
                    print("Enter col # to edit")
                elif self.typing == 3:
                    self.col = concatNums(self.number)
                    self.number = []
                    print(f"Col: {self.col}")
                    print("Enter height")
                elif self.typing == 4:
                    self.newHeight = concatNums(self.number)
                    self.number = []
                    print(f"Height: {self.newHeight}\n")

                    if 5 <= self.row < len(self.map) and 5 <= self.col < len(self.map):
                        self.map[self.row][self.col] = self.newHeight
                    self.typing = 0
                    self.row = 0
                    self.col = 0
                    self.newHeight = 0

            if 48<=symbol<=57:
                self.number.append(symbol-48)

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

        @self.window.event
        def on_mouse_scroll(x, y, dx, dy):
            if dy < 0:
                self.zoom += 2
            else:
                self.zoom -= 2

        @self.window.event
        def on_text_motion(motion):
            if motion == pyglet.window.key.DOWN and len(self.map) >= 5:
                self.map = createMatrix(len(self.map)-1)
            elif motion == pyglet.window.key.UP:
                self.map = createMatrix(len(self.map)+1)
    
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

def createMatrix(size):
    arr = []
    for x in range(size):
        row = []
        for y in range(size):
            row.append(0)
        arr.append(row)
    return arr

def concatNums(list):
    if len(list) == 0:
        return 0
    string = ''
    for x in list:
        string += str(x)
    return int(string)
            
if __name__ == '__main__':
    myGame = Scene(caption="Koutrakos - Lab 12 - Part 4", map=createMatrix(40), zoom=30)
    # debugging = pyglet.window.event.WindowEventLogger()
    # myGame.window.push_handlers(debugging)
    pyglet.app.run()
