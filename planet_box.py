from pgu import gui as pgui
from assets import font
class Box:



    def __init__(self):
        self.container = pgui.Container(width=500)

    def update(self):
        self.container = pgui.Container(width=500)
        


    def paint(self, screen):
        self.container.paint(screen)


class Line:

    checkbox = None
    drop_down = None
    color_box = None
    distance = None

    def __init__(self, name, target, color = "RED"):
        self.container = pgui.Container(width=400)
        self.name_box = pgui.Label(name)
        self.container.add(self.name_box, 0, 0)

        self.checkbox = pgui.Switch(True)
        self.container.add(self.checkbox, 100, 0)

    def add_gui(self, gui):
        gui.add(self.checkbox)
        gui.add(self.name_box)

    def draw(self, screen):
        self.checkbox.paint()

    def update(self, delta_time):
        pass
