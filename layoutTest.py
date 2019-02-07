import EZUI

string = "100,50,een.50,100,twee.100,100,drie"
vectors = EZUI.stringToVectorArray(string)

print(vectors)

layoutArr = EZUI.layout(vectors)
surface = EZUI.Surface(layoutArr)
window = EZUI.Window()
window.giveSurface(surface)
EZUI.Window.run()