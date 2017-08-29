import sys
from PIL import Image


import pyglet
from pyglet import gl
from pyglet.gl import *
from pyglet.window import key

import re


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
INCREMENT = 1




map = ["******************",
       "*      **        *",
       "*      *****     *",
       "*                *",
       "****       **     ",
       "*          **    *",
       "*          **    *",
       "******************",]



p = re.compile('\**\S')    # '\S' means all but whitespace



height = len(map) 

vertexList = []
textureList = []
normalList = []


for index in range(height):
    tmpRow = []
    for m in p.finditer(map[index]):
        tmpRow.append(m.span())

    for segment in tmpRow:
        
        vertexCoords = []
        textureCoords = []
        normalCoords = []

        segmentStart, segmentEnd = segment
        for i in range(segmentStart, segmentEnd+1):
            vertexCoords.append( (i, index, 0) )
            vertexCoords.append( (i, index+1, 0) )
            textureCoords.append( (i, index) )
            textureCoords.append( (i, index+1) )
            normalCoords.append( (0, 0, 1) )
            normalCoords.append( (0, 0, 1) )

        vertexList.append(sum(vertexCoords, ()))
        textureList.append(sum(textureCoords, ()))
        normalList.append(sum(normalCoords, ()))

#print(normalList)



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

    xRotation = yRotation = 0 
    xTranslation = 0
    yTranslation = 0
    zTranslation = 0

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
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(1., 1., 1., 0.))


    def on_draw(self):
        # Clear the current GL Window
        self.clear()
        gl.glColor3f(155,155,155)

        glMatrixMode(GL_MODELVIEW)
        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)
        
        glMatrixMode(GL_PROJECTION)
        glTranslatef(self.xTranslation, 0, 0)
        glTranslatef(0, self.yTranslation, 0)
        glTranslatef(0, 0, self.zTranslation)

        glMaterialfv(GL_FRONT, GL_AMBIENT, (GLfloat*3) (.7,.7,.7))
        for vc, tc, nc in zip(vertexList, textureList, normalList):
            pyglet.graphics.draw(len(vc)//3, gl.GL_TRIANGLE_STRIP, ('v3f', vc ), ('t2i', tc), ('n3f', nc))

        


    def on_resize(self, width, height):
        # set the Viewport
        glViewport(0, 0, width, height)
        # using Projection mode
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspectRatio = width / height
        gluPerspective(35, aspectRatio, 1, 1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -80)


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
            self.zTranslation += INCREMENT/8
        elif symbol == key.NUM_2:
            self.zTranslation -= INCREMENT/8
        elif symbol == key.NUM_4:
            self.xTranslation += INCREMENT/8
        elif symbol == key.NUM_6:
            self.xTranslation -= INCREMENT/8
        elif symbol == key.NUM_9:
            self.yTranslation -= INCREMENT/8
        elif symbol == key.NUM_3:
            self.yTranslation += INCREMENT/8
        elif symbol == key.ESCAPE:
            exit()


def update(dt):
    pass


            
if __name__ == '__main__':
    Window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Stuff')
    pyglet.clock.schedule_interval(update,1/60.0)
    pyglet.app.run()





