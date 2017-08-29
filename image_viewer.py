import pyglet

window = pyglet.window.Window()
image = pyglet.resource.image('images/test1.jpg')

@window.event
def on_draw():
	window.clear()
	image.blit(0, 0)

pyglet.app.run()





