# Demonstration of depth buffering
# When depth buffering is active, the orbiting yellow planet
# will be properly hidden by the blue and red planets as it
# passes behind them.
# Depth buffering is toggled on & off by pressing the space bar.

import sys
import time
from pyglet.gl import *

window = pyglet.window.Window()

useDepthBuffer = 0

angle0 = 0
angle1 = 90
angle2 = 0

def drawPlanet(radius, color):
    glColor3f(color[0],color[1],color[2])
    glBegin(GL_QUADS)
    glVertex2f(-radius, -radius)
    glVertex2f(radius, -radius)
    glVertex2f(radius, radius)
    glVertex2f(-radius, radius)
    glEnd()
    
@window.event
def on_draw():
    global angle0, angle1, angle2, useDepthBuffer
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    if useDepthBuffer:
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    drawPlanet(0.2, [0, 0, 1])

    glPushMatrix()
    glRotatef(angle0, 1, 0, 0)
    glTranslatef(0.6, 0.0, 0.0)
    drawPlanet(0.1, [1, 0, 0])
    glPopMatrix()

    glPushMatrix()

    glRotatef(angle1, 0, 1, 0)
    glTranslatef(0.7, 0.0, 0.0)
    drawPlanet(0.08, [1, 1, 0])

    glPushMatrix()
    glRotatef(angle2, 0, 0, 1)
    glTranslatef(0.2, 0.0, 0.0)
    drawPlanet(0.03, [0.25, 1, 0.25])
    glPopMatrix()

    glPopMatrix()


@window.event
def on_key_press(key, modifiers):
    if key == pyglet.window.key.SPACE:
        global useDepthBuffer
        useDepthBuffer = not useDepthBuffer
        if useDepthBuffer:
            print("depth buffering on")
        else:
            print("depth buffering off")

def update(dt):
    global angle0, angle1, angle2
    angle0 = angle0 + 120 * dt
    angle1 = angle1 + 60 * dt
    angle2 = angle2 + 270 * dt

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()






