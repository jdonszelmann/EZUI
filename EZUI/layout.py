from pyglet.gl import *
import random


class Vector():

    def __init__(self, x, y, name=None, color=None):
        self.x = x
        self.y = y
        self.name = name
        if color == None:
            self.color = [self.x*0.01, self.y*0.01, random.uniform(0, 1), 1]
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

    def validate(self):
        if self.x0 >= self.x1 or self.y0 <= self.y1:
            return False
        if self.x0 < 0 or self.x1 > 100 or self.y0 > 100 or self.y0 < 0:
            return False

        i = 0
        if self.children != None:
            while i < len(self.children):
                c = self.children[i]
                if not c.validate():
                    return False
                if c.y0 > self.y1 or c.x1 > self.x1:
                    return False
                if i > 1:
                    cv = self.children[i-1]
                    if c.x0 != cv.x1 or c.y0 != cv.y0:
                        return False
                i += 1
        return True

    def giveParent(self, parent):
        self.parent = parent

    def draw(self, window):
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])
        glVertex2f(self.x0*0.01*window.width, self.y1*0.01*window.height)
        glVertex2f(self.x0*0.01*window.width, self.y0*0.01*window.height)
        glVertex2f(self.x1*0.01*window.width, self.y0*0.01*window.height)
        glVertex2f(self.x1*0.01*window.width, self.y1*0.01*window.height)

        # if using tree structure (not necessary per sé):
        if self.children != None:
            for child in self.children:
                child.draw(window)


'''
    def validate(self):
        if x0>=x1 or y0<=y1:
            return False
        if self.children!=None:
            for child in self.children:
                if(not child.validate):
                    return False
                if child.y0<self.y1 or child.x1>self.x1:
                    return True
'''


class Surface():

    def __init__(self, layoutArray):
        self.vectorQuadArr = layoutArray[0]
        self.children = layoutArray[1]

    def draw(self, window):
        # either:
        glBegin(GL_QUADS)
        for child in self.children:
            child.draw(window)
        glEnd()
        # using the tree structure referenced in line 35
        # or:
        '''
        for vectorQuad in self.vectorQuadArr:
            vectorQuad.draw()
            # without the tree structure
        '''

    def validate(self):
        i = 0
        if self.children != None:
            while i < len(self.children):
                c = self.children[i]
                if not c.validate():
                    return False
                if i > 1:
                    cv = self.children[i-1]
                    if c.x0 != cv.x1 or c.y0 != cv.y0:
                        return False
                i += 1
        return True


def layout(lijstPunten, x0=0, y0=100, i=0, subx=None):
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
                tempv = findVectorLeft(vectorQuadArr, v)
                if tempv == None:
                    templayout = layout(lijstPunten, 0,
                                        newQuad.y1, i, newQuad.x1)
                else:
                    templayout = layout(
                        lijstPunten, tempv.x1, newQuad.y1, i, newQuad.x1)

                tempArr = templayout[0]

                for quad in tempArr:
                    vectorQuadArr.append(quad)
                    i += 1

                newQuad.giveChildren(templayout[1])

            else:
                if subx != None and v.x > subx:
                    return [vectorQuadArr, childrenArr]
                else:
                    newQuad = VectorQuad(newQuad.x1, newQuad.y0, v)
                    vectorQuadArr.append(newQuad)
                    childrenArr.append(newQuad)
                    i += 1

    return [vectorQuadArr, childrenArr]


def findVectorLO(arrayList, newVector):
    pass


def findVectorLeft(arrayList, newVector):
    tempVector = None
    for vector in arrayList:
        if vector.y1 <= newVector.y:
            if tempVector == None or tempVector.x1 < vector.x1:
                tempVector = vector
    return tempVector


def stringToVectorArray(string):
    vectorArray = []
    tempVectorArray = string.split(">,")
    for vectorString in tempVectorArray:
        vectorString = vectorString.replace("<", "")
        vectorString = vectorString.replace(">", "")
        vectorString = vectorString.split(":")

        name = vectorString[0]
        x = int(vectorString[1])
        y = int(vectorString[2])

        if len(vectorString) >= 6:
            r = float(vectorString[3])
            g = float(vectorString[4])
            b = float(vectorString[5])
            if len(vectorString) == 7:
                q = float(vectorString[6])
            else:
                q = 1
            color = [r, g, b, q]
        else:
            color = None

        vector = Vector(x, y, name, color)

        vectorArray.append(vector)
    return vectorArray

# two temporary methods to test with:


def kleuren(v):
    if v.children != None:
        for child in v.children:
            childcolor(child)
            if child.children != None:
                kleuren(child)


# temp test
def childcolor(v):
    if v.parent != None:
        rand = random.uniform(0, 0.2)
        for i in range(3):
            v.color[i] = v.parent.color[i]*0.9 + rand
