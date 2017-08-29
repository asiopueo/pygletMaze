
# Demonstration of perspective projection
#
import sys, time
from pyglet.gl import *

window = pyglet.window.Window()
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

glLineWidth(5.0)
glEnable(GL_DEPTH_TEST)

text = pyglet.text.Label('',x=5,y=5,font_name='Times New Roman', font_size=20)

fovy = 60.0

@window.event
def on_draw():
    glViewport(0, 0, window.width, window.height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(window.width) / window.height
    gluPerspective(fovy, aspect, 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-100, -4, -100)
    glVertex3f(100, -4, -100)
    glVertex3f(100, -4, 100)
    glVertex3f(-100, -4, 100)
    glEnd()

    drawTriangles()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,640,0,480)
    glMatrixMode(GL_MODELVIEW)
    text.text = 'FOVY: %.0f degrees' % fovy
    text.draw()



def drawTriangles():
    for x in range(-3,3):
        for z in range(5,8):
            glColor3f((x+z)/11.0, (z-x)/11.0, 1)
            glPushMatrix()
            glTranslatef(x*20, -4, -z*5)
            glBegin(GL_LINE_LOOP)
            glVertex3f(-5, 0, 0)
            glVertex3f(5, 0, 0)
            glVertex3f(0, 15, 0)
            glEnd()
            glPopMatrix()


def update(dt):
    global fovy
    if keys[pyglet.window.key.LEFT]:
        fovy = fovy + 1
    elif keys[pyglet.window.key.RIGHT]:
        fovy = fovy - 1

pyglet.clock.schedule_interval(update,1/20.0)
pyglet.app.run()