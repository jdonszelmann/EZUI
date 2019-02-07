import EZUI

string = "50,50.100,50.100,40.25,0.50,0.100,0"
vectors = EZUI.stringToVectorArray(string)

print(vectors)

layoutArr = EZUI.layout(vectors)
surface = EZUI.Surface(layoutArr)
window = EZUI.Window()
window.giveSurface(surface)
EZUI.Window.run()