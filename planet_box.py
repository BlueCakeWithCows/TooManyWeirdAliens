import pgu as pgui
from assets import font
class Box:
    def __init__(self):
        pass

pbl = pgui.Label("Alixorian Xanorth II")
pbl.set_font(font)
pbl2 = pgui.Label("37342km")
pbl2.set_font(font2)
lo.add(pbl,0,20)
lo.add(pbl2, 150, 22)
lo.add(button,130,25)
selector = pgui.Select()
selector.add("Blue", 'blue')
selector.add("Green", 'green')
print(texture["repair_earth"])
gun = pgui.Image(texture["repair_earth"])
selector.add(gun , 'red')
lo.add(selector, 180, 22)

class Line:

    name = None
    checkbox = None
    drop_down = None
    color_box = None
    distance = None

    def __init__(self, name, target, color = "RED"):
        self.name = name
        self.name_box = pgui.Label(name)
        self.name_box.set_font()
        self.target = target
        self.distance = 1000

        pass
