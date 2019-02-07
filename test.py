
import EZUI


window = EZUI.Window()
window.addChildren(
    EZUI.Surface("leftroot", (0, 0), (50, 100), subsufaces=[
        EZUI.Surface("leftrootbottom", (0, 50), (100, 50), subsufaces=[
            EZUI.Surface("leftrootbottomleft", (0, 0), (50, 100)),
            EZUI.Surface("leftrootbottomright", (50, 0), (50, 100)),
        ]),
    ]),
    EZUI.Surface("rightroot", (50, 0), (50, 100), subsufaces=[
        EZUI.Surface("rightroottop", (0, 0), (100, 70)),
        EZUI.Surface("rightrootbottom", (0, 70), (100, 30)),
    ])
)
EZUI.Window.run()
