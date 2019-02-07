import EZUI

string = "100,50,een.100,40,vier.50,0,twee.100,0,drie"
vectors = EZUI.stringToVectorArray(string)

print(vectors)

layoutArr = EZUI.layout(vectors)
surface = EZUI.Surface(layoutArr)
window = EZUI.Window()
window.giveSurface(surface)
EZUI.Window.run()