
import pyglet
from pyglet.gl import *
import json
import os

path = os.path.dirname(os.path.abspath(__file__))


class Window(pyglet.window.Window):
    def __init__(self):
        with open(os.path.join(path, "config.json")) as f:
            self.configfile = json.load(f)

        super().__init__(
            self.configfile["window"]["defaultwidth"],
            self.configfile["window"]["defaultheight"]
        )

        # enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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
        label = pyglet.text.Label(
            'Hello, world',
            font_name='Times New Roman',
            font_size=36,
            x=self.width//2, y=self.height//2,
            anchor_x='center', anchor_y='center',
            color=(0, 0, 0, 255)
        )

        label.draw()
