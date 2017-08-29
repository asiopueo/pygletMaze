
from pyglet.gl import *

window = pyglet.window.Window()

class Hand:
    def __init__(self):
        self.pos = [0,0,0]
        self.ori = [0,0,0]
        self.geom = pyglet.graphics.vertex_list(4, ('v2f', [-15,-10, 15,-10, 20,10, -20,10]))
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0]+250,self.pos[1],0)
        glRotatef(self.ori[1],0,0,1)
        self.geom.draw(GL_QUADS)
        glPopMatrix()

class Finger:
    def __init__(self):
        self.pos = [0,0,0]
        self.geom = pyglet.graphics.vertex_list(3, ('v2f', [-10,-10, 10,-10, 0,10]))
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0]+250,self.pos[1],0)
        self.geom.draw(GL_TRIANGLES)
        glPopMatrix()

hand = Hand()
fingers = [ Finger(), Finger(), Finger(), Finger(), Finger() ]

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    hand.draw()
    for f in fingers:
        f.draw()


def update(dt):
    pass



##############################
# Leap code
##############################

import Leap
from math import *

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print("Leap initialized")
    def on_connect(self, controller):
        print("Leap connected")
    def on_disconnect(self, controller):
        print("Leap disconnected")
    def on_exit(self, controller):
        print("Leap exited")

    def on_frame(self, controller):
        global hand, fingers
        frame = controller.frame()
        if not frame.hands.is_empty:
            leaphand = frame.hands[0]
            leapfingers = leaphand.fingers
            for i in range(min(len(fingers),len(leapfingers))):
                fingers[i].pos = leapfingers[i].tip_position

            normal = leaphand.palm_normal
            direction = leaphand.direction
            hand.pos = leaphand.palm_position
            hand.ori = [ degrees(direction.pitch), degrees(normal.roll), degrees(direction.yaw) ]

listener = SampleListener()
controller = Leap.Controller()
controller.add_listener(listener)

##############################

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()

controller.remove_listener(listener)