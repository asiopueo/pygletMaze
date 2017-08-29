# This program draws a moving "car" with rotating wheels
# It demonstrates the use of the glPushMatrix and glPopMatrix to
# create a hierarchy of transformations.

from pyglet.gl import *

window = pyglet.window.Window(500,500)

angle = 0
carPosition = [100, 100, 0]
carDirection = 1

carbody = pyglet.graphics.vertex_list(4, ('v2f', [-75,0, 75,0, -75,50, 75,50]))
wheel = pyglet.graphics.vertex_list(4, ('v2f', [-20,-20,  20,-20,  -20,20,  20,20]))

def drawCar():
    glPushMatrix()
    glTranslatef(carPosition[0], carPosition[1], carPosition[2])
    carbody.draw(GL_TRIANGLE_STRIP)

    glColor3f(1, 1, 0)

    glPushMatrix()
    glTranslatef(-50, 0.0, 0.0)

    glRotatef(angle, 0, 0, 1)
    wheel.draw(GL_TRIANGLE_STRIP)

    glPopMatrix()

    glColor3f(1, 0, 0)

    glPushMatrix()
    glTranslatef(50, 0.0, 0.0)
    glRotatef(angle, 0, 0, 1)
    wheel.draw(GL_TRIANGLE_STRIP)
    glPopMatrix()
    glPopMatrix()

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0, 0, 1)
    drawCar()


def update(dt):
    global angle, carPosition, carDirection
    angle = angle - 180 * dt * carDirection
    carPosition[1] = carPosition[1] + dt * carDirection * 200
    if carPosition[1] > 400:
        carDirection = -1
    elif carPosition[1] < 100:
        carDirection = 1


pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()