import pyglet
from pyglet.gl import *
import json
import os
from . import surface

path = os.path.dirname(os.path.abspath(__file__))


class Window(pyglet.window.Window, surface.Surface):
    def __init__(self):
        with open(os.path.join(path, "config.json")) as f:
            self.configfile = json.load(f)

        pyglet.window.Window.__init__(
            self,
            self.configfile["window"]["defaultwidth"],
            self.configfile["window"]["defaultheight"],
            resizable=True
        )
        surface.Surface.__init__(
            self,
            "root",
            (0, 0),
            (100, 100)
        )

        # enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # make polygons filled
        glPolygonMode(GL_FRONT, GL_FILL)
        # set background color
        glClearColor(1.0, 1.0, 1.0, 1.0)

        pyglet.clock.schedule_interval(self.update, 1 / 60)

    @classmethod
    def run(cls):
        pyglet.app.run()

    def update(self, dt):
        """
        called n times per second to update all UI elements
        """
        pass

    def on_draw(self):
        """
        draws all content to screen
        """
        glClear(GL_COLOR_BUFFER_BIT)

        glPushMatrix()
        # translate to make the origin top left
        glTranslatef(0, self.height, 0)
        glScalef(1, -1, 1)

        self.draw()
        glPopMatrix()
