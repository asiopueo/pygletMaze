import sys, time, math
from pyglet.gl import *
from euclid import *
from Spring import *

window = pyglet.window.Window(512,512)

GravityAccel = Vector3(0, -98, 0)
AirDrag = 2
BounceCoeff = 0.8

class Object:
    def __init__(self, position, velocity, mass, color):
        self.point = PointMass(position,velocity,mass)
        self.color = color
        self.triangle = pyglet.graphics.vertex_list(3, ('v2f', [-2,-2, 2,-2, 0,2]))
    def draw(self):
        glColor3f(self.color[0], self.color[1], self.color[2])
        glPushMatrix()
        glTranslatef(self.point.position[0], self.point.position[1], self.point.position[2])
        self.triangle.draw(GL_TRIANGLES)
        glPopMatrix()
    def calculateForce(self):
        self.point.clearForce()
        self.point.addForce(self.point.mass * GravityAccel)
        self.point.addForce(self.point.velocity * -AirDrag)
    def update(self,dt):
        self.point.update(dt)

num = 10

objects = []
for i in range(0,num):
    objects.append(Object(Vector3(i*20.0+300, 400, 0), Vector3(0,0,0), 5.0, [0,1,0]))
objects[0].point.mobile = False

springs = []
for i in range(0,num-1):
    springs.append(Spring(objects[i].point,objects[i+1].point,-1,2000))

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    for o in objects: o.draw()
    for s in springs: s.draw()


active = False

@window.event
def on_key_press(key,modifiers):
    if key == pyglet.window.key.R:
        objects[0].point.mobile = True
    elif key == pyglet.window.key.SPACE:
        global active
        active = not active

def update(dt):
    if active:
        for o in objects: o.calculateForce()
        for s in springs: s.calculateForce()
        for o in objects: o.update(dt)

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()