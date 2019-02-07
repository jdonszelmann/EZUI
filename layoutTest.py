# pylint:disable=no-member

import EZUI

string = "<:50:50:1:0:0>,<:100:50:0:1:0>,<:25:40:0:1:1>,<:100:40:1:1:0>,<:25:0:1:0:1>,<:50:0:1:0:0.5>,<:100:0:0:1:1>"
vectors = EZUI.stringToVectorArray(string)

layoutArr = EZUI.layout(vectors)
surface = EZUI.Surface(layoutArr)
print("Surface Valid: {}".format(surface.validate()))
window = EZUI.Window()
window.giveSurface(surface)
EZUI.Window.run()
