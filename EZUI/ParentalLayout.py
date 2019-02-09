from pyglet.gl import *


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mul(self, vector):
        return Vector(self.x*vector.x, self.y*vector.y)

    def add(self, vector):
        return Vector(self.x+vector.x, self.y+vector.y)


class Surface:

    def __init__(self, TL=Vector(0, 100), BR=Vector(100, 0)):
        self.TL = TL
        self.BL = Vector(TL.x, BR.y)
        self.BR = BR
        self.TR = Vector(BR.x, TL.y)

        self.children = []

        self.r = 0
        self.g = 0
        self.b = 0
        self.q = 0

    def giveChild(self, child):
        self.children.append(child)

    def giveParent(self, parent):
        self.parent = parent

    def giveColor(self, r, g, b, q=1):
        self.r = r
        self.g = g
        self.b = b
        self.q = q

    def transformedSurface(self, size, offset):
        # Returns a transformed version of this surface
        TL = self.TL.mul(size).add(offset)
        BR = self.BR.mul(size).add(offset)
        return Surface(TL, BR)

    def surfaceSize(self):
        xsize = self.BR.x - self.TL.x
        ysize = self.TL.y - self.BR.y
        return Vector(xsize, ysize)

    def draw(self, size, offset=Vector(0, 0)):
        # Draws this surface and all it's children, each properly transformed
        # REMEMBER TO "glBegin(GL_QUADS)" and "glEND()" BEFORE AND AFTER THE MAIN DRAW
        drawSurface = self.transformedSurface(size, offset)
        glColor4f(self.r, self.g, self.b, self.q)
        glVertex2fv(drawSurface.TL)
        glVertex2fv(drawSurface.BL)
        glVertex2fv(drawSurface.BR)
        glVertex2fv(drawSurface.TR)

        for child in self.children:
            child.draw(drawSurface.surfaceSize(), drawSurface.BL)

    def giveSurface(self, vector, leftBound=True):
        # Give this surface a child surface, with either left,upperbound (default) or upper,leftbound.
        if leftBound:
            left = self.findLeftBound(vector)
            upper = self.findUpperBound(Vector(left, vector.y), True)
        else:
            upper = self.findUpperBound(vector)
            left = self.findLeftBound(Vector(vector.x, upper), True)

        surface = Surface(Vector(left, upper), vector)

        self.giveChild(surface)
        surface.giveParent(self)
        return surface

    def findLeftBound(self, vector, upperLeftBound=False):
        # Finds the lowestmost broundrary to the top of the vector, upperLeftBound dictates the behaviour or touching corners, depending on left or upperbound usage in giveSurface()
        highestX = 0
        for child in self.children:
            if ((upperLeftBound and child.TR.y >= vector.y) or child.TR.y > vector.y) and ((not upperLeftBound and child.BR.y <= vector.y) or child.BR.y < vector.y):
                childRight = child.RB.x
                if childRight > highestX and childRight <= vector.x:
                    highestX = childRight
        return highestX

    def findUpperBound(self, vector, leftUpperBound=False):
        # Finds the rightmost broundrary to the left of the vector, leftUpperBound dictates the behaviour or touching corners, depending on left or upperbound usage in giveSurface()
        lowestY = 100
        for child in self.children:
            if ((leftUpperBound and child.BL.x <= vector.x) or child.BL.x < vector.x)and ((not leftUpperBound and child.BR.x >= vector.x) or child.BR.x > vector.x):
                childBottom = child.RB.y
                if childBottom < lowestY and childBottom >= vector.y:
                    lowestY = childBottom
        return lowestY
