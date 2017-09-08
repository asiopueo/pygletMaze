import sys
from PIL import Image

import pyglet
from pyglet import gl
from pyglet.gl import *
from pyglet.window import key

import re
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
INCREMENT = 1


"""
MAP_WIDTH = 3
MAP_HEIGHT = 3

map = ["   ",
       " * ",
       "   "]


MAP_WIDTH = 15
MAP_HEIGHT = 5

map = ["               ",
       " **********    ",
       " *********     ",
       "       ***     ",
       "               "]
"""


MAP_WIDTH = 20
MAP_HEIGHT = 10

map = ["                    ",
       " ****************** ",
       " *      **        * ",
       " *      *****     * ",
       " *                * ",
       " ****       **      ",
       " *          **    * ",
       " *          **    * ",
       " ****************** ",
       "                    "]


def getVertexCoords(chart, row, column):
    back = [(1,0,0), (1,1,0), (0,1,0), (0,0,0)]
    vertices = [[(e[0]+column, e[1]-row, e[2]) for e in back]]

    if chart[row-1][column] == " ":
        top = [(1,1,0), (1,1,1), (0,1,1), (0,1,0)]
        vertices.append([(e[0]+column, e[1]-row, e[2]) for e in top])
    if chart[row][column-1] == " ":
        left = [(0,1,0), (0,1,1), (0,0,1), (0,0,0)]
        vertices.append([(e[0]+column, e[1]-row, e[2]) for e in left])
    if chart[row+1][column] == " ":
        bottom = [(0,0,0), (0,0,1), (1,0,1), (1,0,0)]
        vertices.append([(e[0]+column, e[1]-row, e[2]) for e in bottom])
    if chart[row][column+1] == " ":
        right = [(1,0,0), (1,0,1), (1,1,1), (1,1,0)]
        vertices.append([(e[0]+column, e[1]-row, e[2]) for e in right])
    return vertices

def getTextureCoords(chart, row, column):
    vertices = [[(1,0), (1,1), (0,1), (0,0)]]

    if chart[row-1][column] == " ":
        vertices.append([(1,0), (1,1), (0,1), (0,0)])
    if chart[row][column-1] == " ":
        vertices.append([(1,0), (1,1), (0,1), (0,0)])
    if chart[row+1][column] == " ":
        vertices.append([(1,0), (1,1), (0,1), (0,0)])
    if chart[row][column+1] == " ":
        vertices.append([(1,0), (1,1), (0,1), (0,0)])

    return vertices

def getNormalCoords(chart, row, column):
    vertices = [[(0,0,1), (0,0,1), (0,0,1), (0,0,1)]]

    if chart[row-1][column] == " ":
        vertices.append([(0,-1,0), (0,-1,0), (0,-1,0), (0,-1,0)])
    if chart[row][column-1] == " ":
        vertices.append([(1,0,0), (1,0,0), (1,0,0), (1,0,0)])
    if chart[row+1][column] == " ":
        vertices.append([(0,1,0), (0,1,0), (0,1,0), (0,1,0)])
    if chart[row][column+1] == " ":
        vertices.append([(-1,0,0), (-1,0,0), (-1,0,0), (-1,0,0)])
    return vertices





p = re.compile('\**\S')    # '\S' means all but whitespace

vertexList = []
textureList = []
normalList = []

for index in range(MAP_HEIGHT):
    tmpRow = []
    for m in p.finditer(map[index]):
        tmpRow.append(m.span())

    for segment in tmpRow:
        vertexCoords = []
        textureCoords = []
        normalCoords = []

        segmentStart, segmentEnd = segment
        for i in range(segmentStart, segmentEnd):
            if i < MAP_WIDTH-1:
                vertexCoords.append(getVertexCoords(map, index, i))
                textureCoords.append(getTextureCoords(map, index, i))
                normalCoords.append(getNormalCoords(map, index, i))

        vertexCoords = [item for sublist in vertexCoords for subsublist in sublist for item in subsublist]
        textureCoords = [item for sublist in textureCoords for subsublist in sublist for item in subsublist]
        normalCoords = [item for sublist in normalCoords for subsublist in sublist for item in subsublist]

        vertexList.append(sum(vertexCoords, ()))
        textureList.append(sum(textureCoords, ()))
        normalList.append(sum(normalCoords, ()))

#print(vertexList)



def loadTexture(filename):
    img = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    textureIDs = (pyglet.gl.GLuint * 1) ()
    glGenTextures(1,textureIDs)
    textureID = textureIDs[0]
    print('generating texture', textureID, 'from', filename)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes())
    glBindTexture(GL_TEXTURE_2D, 0)

    return textureID



class Window(pyglet.window.Window):

    xRotation = 0
    yRotation = 0 
    #zRotation = 0
    xTranslation = 0
    yTranslation = 0
    zTranslation = -10

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)  

        self.tex = loadTexture('crate.jpg')
        #self.tex = loadTexture('texture.jpg')

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, self.tex)

        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(1., 1., 1., 1.))
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)


    def on_draw(self):
        # Clear the current GL Window
        self.clear()
        glMatrixMode(GL_MODELVIEW)
        gl.glColor3f(155,155,155)


        glLoadIdentity()
        glTranslatef(self.xTranslation, 0, 0)
        glTranslatef(0, self.yTranslation, 0)
        glTranslatef(0, 0, self.zTranslation)
        
        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)
        
        #glRotatef(self.yRotation,0,1,0)
        #glTranslatef(0,0,self.zTranslation)

        #glPushMatrix()
        """
        glBegin(GL_TRIANGLES)
        glVertex4f(1,0,0,1)
        glVertex4f(0,1,0,1)
        glVertex4f(0,0,0,1)
        glEnd()
        """
        #glPopMatrix()
        
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (GLfloat*3) (.7,.7,.7))
        for vc, tc, nc in zip(vertexList, textureList, normalList):
            pyglet.graphics.draw(len(vc)//3, gl.GL_QUADS, ('v3f', vc ), ('t2f', tc), ('n3f', nc))
        


    def on_resize(self, width, height):
        # set the Viewport
        glViewport(0, 0, width, height)
        # using Projection mode
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspectRatio = width / height
        gluPerspective(35, aspectRatio, 1, 1000)

        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        #glTranslatef(0., 0., -1)


    def on_text_motion(self, motion):
        if motion == key.UP:
            self.xRotation -= INCREMENT
        elif motion == key.DOWN:
            self.xRotation += INCREMENT
        elif motion == key.LEFT:
            self.yRotation -= INCREMENT
        elif motion == key.RIGHT:
            self.yRotation += INCREMENT
        

    def on_key_press(self, symbol, modifiers):
        if symbol == key.NUM_8:
            self.zTranslation += INCREMENT/12
        elif symbol == key.NUM_2:
            self.zTranslation -= INCREMENT/12
        elif symbol == key.NUM_4:
            self.xTranslation += INCREMENT/12
        elif symbol == key.NUM_6:
            self.xTranslation -= INCREMENT/12
        elif symbol == key.NUM_9:
            self.yTranslation -= INCREMENT/12
        elif symbol == key.NUM_3:
            self.yTranslation += INCREMENT/12
        elif symbol == key.ESCAPE:
            exit()


def update(dt):
    pass


            
if __name__ == '__main__':
    Window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Stuff')
    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.app.run()










