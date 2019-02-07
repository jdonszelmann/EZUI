from pyglet.gl import *


class Vector():

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class VectorQuad():

    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def giveChildren(self, children):
        self.children = children
        for child in children:
            child.giveParent(self)

    def giveParent(self, parent):
        self.parent = parent

    def draw(self):
        glBegin(GL_Quad)
        glVertex2f(self.x0, self.y0)
        glVertex2f(self.x0, self.y1)
        glVertex2f(self.x1, self.y1)
        glVertex2f(self.x1, self.y0)
        glEnd()

        # if using tree structure (not necessary per sé):
        if self.children != None:
            for child in self.children:
                child.draw()


class Surface():

    def __init__(self, layoutArray):
        self.vectorQuadArr = layoutArray[0]
        self.childrenArr = layoutArray[1]

    def draw(self):
        # either:
        for child in self.childrenArr:
            child.draw()
            # using the tree structure referenced in line 35
        # or:
        for vectorQuad in self.vectorQuadArr:
            vectorQuad.draw()
            # without the tree structure


def layout(lijstPunten, x0, y0, i):
    vectorQuadArr = []
    childrenArr = []

    while i < len(lijstPunten):
        v = lijstPunten[i]

        if i == 0:
            newQuad = VectorQuad(x0, y0, v.x, v.y)
            vectorQuadArr.append(newQuad)
            childrenArr.append(newQuad)
            i += 1

        else:
            if v.x <= newQuad.x1:
                templayout = layout(lijstPunten, newQuad.x0, newQuad.y1, i)
                tempArr = templayout[0]

                for quad in tempArr:
                    vectorQuadArr.append(quad)
                    i += 1

                newQuad.giveChildren(templayout[1])

            else:
                newQuad = VectorQuad(newQuad.x1, newQuad.y0, v.x, v.y)
                vectorQuadArr.append(newQuad)
                childrenArr.append(newQuad)
                i += 1

    return [vectorQuadArr, childrenArr]
