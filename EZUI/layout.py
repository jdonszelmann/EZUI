from pyglet.gl import *


class Vector():

    def __init__(self, x, y, name, color=None):
        self.x = x
        self.y = y
        self.name = name
        if color == None:
            self.color = [x*0.01, y*0.01, (x+y)*0.005]
        else:
            self.color = color

    def __repr__(self):
        return "<Vector: Name = {}, x = {}, y = {}>\n".format(self.name, self.x, self.y)


class VectorQuad():

    def __init__(self, x0, y0, vector):
        self.x0 = x0
        self.x1 = vector.x
        self.y0 = y0
        self.y1 = vector.y
        self.name = vector.name
        self.color = vector.color
        self.children = None
        self.parent = None

    def giveChildren(self, children):
        self.children = children
        for child in children:
            child.giveParent(self)

    def giveParent(self, parent):
        self.parent = parent

    def draw(self, window):
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_QUADS)
        glVertex2f(self.x0*0.01*window.width, self.y0*0.01*window.width)
        glVertex2f(self.x0*0.01*window.width, self.y1*0.01*window.width)
        glVertex2f(self.x1*0.01*window.width, self.y1*0.01*window.width)
        glVertex2f(self.x1*0.01*window.width, self.y0*0.01*window.width)
        glEnd()

        # if using tree structure (not necessary per sé):
        if self.children != None:
            for child in self.children:
                child.draw(window)


class Surface():

    def __init__(self, layoutArray):
        self.vectorQuadArr = layoutArray[0]
        self.childrenArr = layoutArray[1]

    def draw(self, window):
        # either:
        for child in self.childrenArr:
            child.draw(window)
        # using the tree structure referenced in line 35
        # or:
        '''
        for vectorQuad in self.vectorQuadArr:
            vectorQuad.draw()
            # without the tree structure
        '''


def layout(lijstPunten, x0=0, y0=0, i=0):
    vectorQuadArr = []
    childrenArr = []
    first = True

    while i < len(lijstPunten):
        v = lijstPunten[i]

        if first == True:
            first = False
            newQuad = VectorQuad(x0, y0, v)
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
                newQuad = VectorQuad(newQuad.x1, newQuad.y0, v)
                vectorQuadArr.append(newQuad)
                childrenArr.append(newQuad)
                i += 1

    return [vectorQuadArr, childrenArr]


def stringToVectorArray(string):
    vectorArray = []
    tempVectorArray = string.split(".")
    for vectorString in tempVectorArray:
        coordarr = vectorString.split(",")
        x = int(coordarr[0])
        y = int(coordarr[1])
        name = coordarr[2]
        if(len(coordarr) == 4):
            color = coordarr[3]
            vector = Vector(x, y, name, color)
        else:
            vector = Vector(x, y, name)
        vectorArray.append(vector)
    return vectorArray
