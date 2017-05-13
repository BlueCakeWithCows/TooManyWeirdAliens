from pgu import gui as pgui
from assets import font, texture
from misc import WHITE
class Box:

    def __init__(self, system):
        self.container = pgui.Container(width=350, height =600)
        self.position=1550,80
        self.system = system
        self.lines = []
        self.update_recursion(self.system)


    def empty(self):
        self.container.widgets.clear()

    def update(self):
        self.empty()

        y = 0
        x = 0
        for line in self.lines:
            if line.parent is None or line.parent.can_drop_down():
                y = y + 26
                x = 18 *line.depth
                line.add_gui(self.container, x, y)



    def add_to_gui(self, gui):
        gui.add(self.container, self.position[0], self.position[1])

    def remove_from_gui(self, gui):
        gui.remove(self)


    def update_recursion(self, my_dict, depth=0, parent = None, truename = None):
        if my_dict.get(truename, None) is not None:
            new_parent = Line(self)
            new_parent.label = truename
            new_parent.target = my_dict.get(truename)
            new_parent.depth = depth
            new_parent.parent = parent
            new_parent.update()
            if parent is not None:
                parent.has_child = True

            parent = new_parent
            self.lines.append(new_parent)
        for key in list(my_dict.keys()):
            value = my_dict[key]
            if isinstance(value ,dict):
                self.update_recursion(value, depth + 1, parent, key)

    def draw(self, screen):
        self.gui.paint(screen)


class Line:

    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.depth = 0
        self.parent = None
        self.color = "Red"
        self.target = None
        self.label = "Null"
        self.has_child = False
        self.drop_down_visible = True

        self.drop_down_box = pgui.Switch({'value':True,'width':5, 'height':5})
        self.drop_down_box.style.off = texture["gray_triangle_off"]
        self.drop_down_box.style.on = texture["gray_triangle_on"]
        self.drop_down_box.resize(100,100)

        def change_visiblity(value):
            self.drop_down_visible = not self.drop_down_box.value
            self.parent_class.update()

        self.drop_down_box.connect(pgui.CLICK, change_visiblity, None)
        self.name_box = pgui.Label(self.label)
        self.name_box.set_font(font["ui_font_1"])
        self.name_box.style.color = WHITE



        self.container = pgui.Container(width=400)
        self.container.add(self.name_box, 0, 0)
        self.container.add(self.drop_down_box, 90, 0)

    def update(self):
        self.name_box.set_text(self.label)

    def add_gui(self, gui, x ,y):
        if self.has_child:
            gui.add(self.drop_down_box,  x, y)
        gui.add(self.name_box, x+30, y)

    def can_drop_down(self):
        p = self
        while p is not None:
            if not p.drop_down_visible:
                return False
            p = p.parent
        return True

    def draw(self, screen):
        self.drop_down_box.paint()
