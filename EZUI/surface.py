from collections.abc import Iterable
from .drawable import Drawable
from pyglet.gl import *
import math


class Surface(Drawable):

    names = {}

    def __init__(self, name, position, size, subsufaces=None):
        """
        name: to later identify this surface
        position: 2d coordinate (in percentages) of where the surface should start
        size: 2d <width,height> pair representing the size of the surface
        subsurfaces: list of child surfaces of this surface. useful for quick tree generation
        """

        assert isinstance(name, str), "name of surface {} must be string".format(
            name)
        assert name not in self.__class__.names, "name {} already in use".format(
            name)
        assert isinstance(position, (tuple, list)), "position of surface {} must be list or tuple".format(
            name)
        assert isinstance(size, (tuple, list)), "size of surface {} must be list or tuple".format(
            name)
        assert len(position) == 2, "position of surface {} must be 2d coordinate (2 numbers)".format(
            name)
        assert len(size) == 2, "size of surface {} must be 2d coordinate (2 numbers)".format(
            name)
        assert 0 <= position[0] <= 100, "position.x of surface {} must be between 0% and 100%".format(
            name)
        assert 0 <= position[1] <= 100, "position.y of surface {} must be between 0% and 100%".format(
            name)
        assert 0 <= size[0] <= 100-position[0], "width of surface {} must be between 0% and {}%".format(
            name,
            100-position[0])
        assert 0 <= size[1] <= 100-position[1], "height of surface {} must be between 0% and {}%".format(
            name,
            100-position[1])

        self.name = name
        self.position = position
        self.size = size

        self.__class__.names[name] = self

        self.parent = None  # set by parent through addChild
        # make an empty children list. will be filled with the subsurfaces parameter or addChild(ren)
        self.children = []

        # add subsurfaces to this surface through the subsurfaces parameter
        if subsufaces:
            assert isinstance(
                subsufaces, Iterable
            ), "subsurfaces list of surface {} must be iterable".format(self.name)
            for i in subsufaces:
                self.addChild(i)

        # these are for recursive drawing. DONT MODIFY THEM
        self._absolutewidth = None
        self._absoluteheight = None
        self._absolutex = None
        self._absolutey = None

    @classmethod
    def getSurfaceWithName(cls, name):
        assert name in cls.names, "could not find surface with name {}".format(
            name)
        return cls.names[name]

    @classmethod
    def getRoot(cls, node):
        if node.parent == None:
            return node
        else:
            return cls.getRoot(node.parent)

    @staticmethod
    def overlaps(A, B):
        def inrange(value, min, max):
            return value > min and value < max

        xoverlap = inrange(
            A.position[0],
            B.position[0],
            B.position[0] + B.size[0]
        ) or inrange(
            B.position[0],
            A.position[0],
            A.position[0] + A.size[0]
        )

        yoverlap = inrange(
            A.position[1],
            B.position[1],
            B.position[1] + B.size[1]
        ) or inrange(
            B.position[1],
            A.position[1],
            A.position[1] + A.size[1]
        )

        return xoverlap or yoverlap

    def addChild(self, child):

        assert child.parent == None, "Surface {} already has a parent and can have only one".format(
            child.name)

        assert all(
            [not Surface.overlaps(i, child) for i in self.children]
        ), "surface {} overlaps with other surfaces of this parent".format(child.name)

        child.parent = self
        self.children.append(child)

    def findLeafNodes(self):
        def findleafnodes(root, leafnodes=None):
            if leafnodes == None:
                leafnodes = []
            if len(root.children) == 0:
                leafnodes.append(root)
            for i in root.children:
                leafnodes += findleafnodes(i)
            return leafnodes

        return findleafnodes(self)

    def addChildren(self, *children):
        for i in children:
            self.addChild(i)

    def draw(self):
        if self.parent == None:
            from .main import Window
            assert isinstance(
                self, Window), "can only draw surface tree with a window as root"
            assert hasattr(self, "width"), "could not find width attribute"
            assert hasattr(self, "height"), "could not find height attribute"
            self._absolutewidth = math.ceil(self.width * self.size[0]/100)
            self._absoluteheight = math.ceil(self.height * self.size[1]/100)
            self._absolutex = math.ceil(0 + self.width * self.position[0]/100)
            self._absolutey = math.ceil(0 + self.height * self.position[1]/100)
        else:

            assert self.parent._absolutewidth != None
            assert self.parent._absoluteheight != None
            assert self.parent._absolutex != None
            assert self.parent._absolutey != None

            self._absolutewidth = math.ceil(
                self.parent._absolutewidth * self.size[0] / 100
            )
            self._absoluteheight = math.ceil(
                self.parent._absoluteheight * self.size[1] / 100
            )
            self._absolutex = math.ceil(
                self.parent._absolutex +
                self.parent._absolutewidth * self.position[0] / 100
            )
            self._absolutey = math.ceil(
                self.parent._absolutey +
                self.parent._absoluteheight * self.position[1] / 100
            )

        # debug stuff
        # print(self._absolutewidth)
        # print(self._absoluteheight)
        # print(self._absolutex)
        # print(self._absolutey)

        # only draw root nodes in the surface tree
        if len(self.children) == 0:
            glColor4f(51/255, self._absoluteheight/480, self._absolutewidth /
                      640+self._absolutex/640, 0.8)
            glBegin(GL_QUADS)
            glVertex2f(
                self._absolutex,
                self._absolutey
            )
            glVertex2f(
                self._absolutex + self._absolutewidth,
                self._absolutey
            )
            glVertex2f(
                self._absolutex + self._absolutewidth,
                self._absolutey + self._absoluteheight
            )
            glVertex2f(
                self._absolutex,
                self._absolutey + self._absoluteheight
            )
            glEnd()

        for i in self.children:
            i.draw()
