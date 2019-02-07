
import pyglet
from pyglet.gl import *
from .surface import Surface
from .drawable import Drawable


class Menu(Drawable):
    def __init__(self, window, title, dragable=True):
        self.title = ""
        self.dragable = dragable
        self.window = window

        self.x = 0
        self.y = 0
        self.width = 50
        self.height = 50

        self.dragged = False
        self.visible = True

        window.registerEventhandler(self)

    def __contains__(self, point):
        assert isinstance(point, (list, tuple)), "point must be list or tuple"
        assert len(point) == 2, "point must be 2d (length 2 list/tuple)"

        x = point[0]
        y = point[1]

        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height

    def mouse_release(self, x, y, buttons, modifiers):
        if self.x + self.width > self.window.width:
            self.x = self.window.width - self.width
        if self.x < 0:
            self.x = 0
        if self.y + self.height > self.window.height:
            self.y = self.window.height - self.height
        if self.y < 0:
            self.y = 0
        self.dragged = False

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragged:

            self.x += dx
            self.y += dy

    def mouse_press(self, x, y, buttons, modifiers):
        if (x, y) in self:
            self.dragged = True

    def draw(self):
        if self.visible:
            glColor4f(51/255, 51/255, 51/255, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(
                self.x,
                self.y
            )
            glVertex2f(
                self.x + self.width,
                self.y
            )
            glVertex2f(
                self.x + self.width,
                self.y + self.height
            )
            glVertex2f(
                self.x,
                self.y + self.height
            )
            glEnd()
