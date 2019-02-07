from .menu import Menu
import pyglet
from pyglet.gl import *
import json
import os
from . import surface
from .drawable import Drawable

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

        self.eventhandlers = []

    def menu(self, *args):
        return Menu(self, *args)

    def registerEventhandler(self, obj):
        self.eventhandlers.append(obj)

    def deregisterEventhandler(self, obj):
        self.eventhandlers.remove(obj)

    def isregisteredEventhandler(self, obj):
        return obj in self.eventhandlers

    @classmethod
    def run(cls):
        pyglet.app.run()

    def update(self, dt):
        """
        called n times per second to update all UI elements
        """
        for i in self.eventhandlers:
            if hasattr(i, "update"):
                i.update()

    def on_mouse_motion(self, x, y, dx, dy):
        for i in self.eventhandlers:
            if hasattr(i, "mouse_motion"):
                i.mouse_motion(x, self.height-y, dx, -dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for i in self.eventhandlers:
            if hasattr(i, "mouse_press"):
                i.mouse_press(x, self.height-y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for i in self.eventhandlers:
            if hasattr(i, "mouse_release"):
                i.mouse_release(x, self.height-y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for i in self.eventhandlers:
            if hasattr(i, "mouse_drag"):
                i.mouse_drag(x, self.height-y, dx, -dy, buttons, modifiers)

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

        for i in self.eventhandlers:
            i.draw()

        glPopMatrix()
