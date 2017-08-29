from pyglet.gl import *
from euclid import *

class PointMass:
    def __init__(self, position, velocity, mass):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.mass = mass
        self.force = Vector3(0, 0, 0)
        self.mobile = True
    def clearForce(self):
        self.force = Vector3(0,0,0)
    def addForce(self, force):
        self.force += force
    def update(self, dt):
        if self.mobile:
            acc = self.force / self.mass
            self.velocity += acc * dt
            self.position += self.velocity * dt

class Spring:
    def __init__(self, point1, point2, restLength, k):
        self.point1 = point1
        self.point2 = point2
        if restLength >= 0:
            self.restLength = restLength
        else:
            v = point1.position - point2.position
            self.restLength = v.magnitude()
        self.k = k
        self.line = pyglet.graphics.vertex_list(2, ('v2f', [0,0,0,0]))
    def calculateForce(self):
        v = self.point2.position - self.point1.position
        displacement = v.magnitude() - self.restLength
        v.normalize()
        force = self.k * displacement * v
        self.point1.addForce(force)
        self.point2.addForce(-force)
    def draw(self):
        self.line.vertices = self.point1.position[0:2] + self.point2.position[0:2]
        self.line.draw(GL_LINES)