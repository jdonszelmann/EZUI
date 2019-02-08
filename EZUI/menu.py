
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

        # true if this surface is currently dragged around with the mouse
        self.dragged = False
        # the surface this menu is latched on to
        self.snappedsurface = None

        window.registerEventhandler(self)

    def __contains__(self, point):
        assert isinstance(point, (list, tuple)), "point must be list or tuple"
        assert len(point) == 2, "point must be 2d (length 2 list/tuple)"

        x = point[0]
        y = point[1]

        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height

    def closestSurface(self):
        averagepositionx = self.x + self.width/2
        averagepositiony = self.y + self.height / 2

        leaves = self.window.findLeafNodes()

        closest = None
        closestdistance = 1e100
        # iterate over all surfaces
        for i in leaves:
            averagex = i._absolutex + i._absolutewidth//2
            averagey = i._absolutey + i._absoluteheight//2

            distance = ((averagepositionx-averagex) ** 2 +
                        (averagepositiony-averagey)**2) ** 0.5

            # save the one with the closest distance from center to center
            if distance < closestdistance:
                closestdistance = distance
                closest = i
        return closest

    def mouse_release(self, x, y, buttons, modifiers):
        if self.dragged:
            if self.x + self.width > self.window.width:
                self.x = self.window.width - self.width
            if self.x < 0:
                self.x = 0
            if self.y + self.height > self.window.height:
                self.y = self.window.height - self.height
            if self.y < 0:
                self.y = 0
            self.dragged = False

            self.snappedsurface = self.closestSurface()

            self.x = self.snappedsurface._absolutex
            self.y = self.snappedsurface._absolutey
            self.width = self.snappedsurface._absolutewidth
            self.height = self.snappedsurface._absoluteheight

    def resize(self, width, height):
        if self.snappedsurface != None and not self.dragged:
            self.x = self.snappedsurface._absolutex
            self.y = self.snappedsurface._absolutey
            self.width = self.snappedsurface._absolutewidth
            self.height = self.snappedsurface._absoluteheight

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragged:
            self.x += dx
            self.y += dy

    def mouse_press(self, x, y, buttons, modifiers):
        if (x, y) in self:
            self.dragged = True

    def draw(self):
        if self.dragged:
            highlightsurface = self.closestSurface()
            glColor4f(1, 0, 0, 1)
            glBegin(GL_LINE_LOOP)
            glVertex2f(
                highlightsurface._absolutex,
                highlightsurface._absolutey
            )
            glVertex2f(
                highlightsurface._absolutex + highlightsurface._absolutewidth,
                highlightsurface._absolutey
            )
            glVertex2f(
                highlightsurface._absolutex + highlightsurface._absolutewidth,
                highlightsurface._absolutey + highlightsurface._absoluteheight
            )
            glVertex2f(
                highlightsurface._absolutex,
                highlightsurface._absolutey + highlightsurface._absoluteheight
            )
            glEnd()

        if self.dragged:
            glColor4f(51/255, 51/255, 51/255, 0.5)
        else:
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
