import sys
from PIL import Image

import pyglet
from pyglet.gl import *
from pyglet.window import key
#from OpenGL.GLUT import *

WINDOW   = 600
INCREMENT = 5

vertices = [(0,0)]
for i in range(5):
    vertices.append( (i,0) )
    vertices.append( (i,1) )
vertices.append( (4,1) )


ver = sum(vertices, ())



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

    # Cube 3D start rotation
    xRotation = yRotation = 45  

    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)  
        self.tex = loadTexture('crate.jpg')
        #self.tex = loadTexture('texture.jpg')

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        


    def on_draw(self):
        # Clear the current GL Window
        self.clear()

        glPushMatrix()

        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)
        
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1)
        glVertex3f(50, -50, 50)
        glTexCoord2f(1, 0)
        glVertex3f(50, -50, -50)
        glTexCoord2f(0, 0)
        glVertex3f(-50, -50, -50)
        glTexCoord2f(0, 1)
        glVertex3f(-50, -50, 50)
        
        glEnd()
        pyglet.graphics.draw(12, gl.GL_LINE_STRIP, ('v2i', ver ))
        """
        glBegin(GL_QUADS)
        glColor3ub(255, 255, 255)
        glVertex3f(50, 50, 50)
        glColor3ub(255, 255, 0)
        glVertex3f(50, -50, 50)
        glColor3ub(255, 0, 0)
        glVertex3f(-50, -50, 50)
        glVertex3f(-50, 50, 50)

        #2
        glColor3f(0, 0, 255)
        glVertex3f(50, 50, -50)
        glVertex3f(50, -50, -50)
        glVertex3f(-50, -50, -50)
        glVertex3f(-50, 50, -50)
        
        #3
        glColor3f(0, 255, 0)
        glVertex3f(50, 50, 50)
        glVertex3f(50, 50, -50)
        glVertex3f(-50, 50, -50)
        glVertex3f(-50, 50, 50)
        glEnd()
        """
        glPopMatrix()

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
        glTranslatef(0, 0, -400)


    def on_text_motion(self, motion):
        if motion == key.UP:
            self.xRotation -= INCREMENT
        elif motion == key.DOWN:
            self.xRotation += INCREMENT
        elif motion == key.LEFT:
            self.yRotation -= INCREMENT
        elif motion == key.RIGHT:
            self.yRotation += INCREMENT

            
if __name__ == '__main__':
    Window(WINDOW, WINDOW, 'Static Cube')
    pyglet.app.run()