from pgu import gui as pgui
import pygame
from assets import font, texture
from misc import WHITE, GREEN, LIGHT_GRAY
from entity.display import Arrow
import copy
class Box:

    def __init__(self, system, instance = None):
        self.instance = instance
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
            new_parent = Line(self, self.instance)
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

    def __init__(self, parent_class, instance):
        self.instance = instance
        self.parent_class = parent_class
        self.depth = 0
        self.parent = None
        self.color = "Red"
        self._target = None
        self.label = "Null"
        self.has_child = False
        self.drop_down_visible = True

        self.drop_down_box = pgui.Switch({'value':True})
        self.drop_down_box.style.off = texture["gray_triangle_off"]
        self.drop_down_box.style.on = texture["gray_triangle_on"]

        self.arrow_check = pgui.Switch()
        self.arrow_check.value = False
        self.arrow = Arrow(self.instance, self.target, GREEN, 1)
        self.arrow.visible = False
        def change_visiblity_arrow(value):
            self.arrow.visible = not self.arrow_check.value

        self.arrow_check.connect(pgui.CLICK, change_visiblity_arrow, None)

        if instance is not None:
            self.instance.create(self.arrow)
        # self.arrow_check.style.off = texture["gray_triangle_off"]
        # self.arrow_check.style.on = texture["gray_triangle_on"]


        def change_visiblity(value):
            self.drop_down_visible = not self.drop_down_box.value
            self.parent_class.update()

        self.drop_down_box.connect(pgui.CLICK, change_visiblity, None)
        self.name_box = pgui.Label(self.label)
        self.name_box.set_font(font["ui_font_1"])
        self.name_box.style.color = LIGHT_GRAY



        # self.container = pgui.Container(width=400)
        # self.container.add(self.name_box, 0, 0)
        # self.container.add(self.drop_down_box, 90, 0)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        self.arrow.target = t
        self._target = t


    def update(self):
        self.name_box.set_text(self.label)

    def add_gui(self, gui, x ,y):
        if self.has_child:
            gui.add(self.drop_down_box,  x, y)
        if self.target is not None:
            gui.add(self.arrow_check, x + 190 - self.depth * 18, y + 10)

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


class InfoBlock:


    def __init__(self, instance = None):
        if instance is None:
            class Fake_It_Till_You_Make_It:
                day=0
                scrap=0
                influence=0
                velocity=0
                fuel=0
            instance = Fake_It_Till_You_Make_It()
        self.instance = instance
        self.container = pgui.Container(width=300, height=100)
        self.position = 1620, 0
        self.container.add(pgui.Image(texture["stat_block_background"]), 0,0)
        self.label_velocity=pgui.Label("")
        self.label_date = pgui.Label("")
        self.label_fuel = pgui.Label("")
        self.label_influence = pgui.Label("")
        self.label_scrap = pgui.Label("")

        self.label_velocity.set_font(font["ui_font_2"])
        self.label_date.set_font(font["ui_font_2"])
        self.label_fuel.set_font(font["ui_font_2"])
        self.label_influence.set_font(font["ui_font_2"])
        self.label_scrap.set_font(font["ui_font_2"])

        self.container.add(self.label_velocity, 30,16)
        self.container.add(self.label_date, 150, 16)
        self.container.add(self.label_fuel, 30, 76)
        self.container.add(self.label_influence, 150, 46)
        self.container.add(self.label_scrap, 30, 46)
        self.update()

    def update(self):
        self.label_velocity.set_text("velocity %s"%self.instance.velocity)
        self.label_date.set_text("day %s" % self.instance.day)
        self.label_fuel.set_text("fuel %s" % self.instance.fuel)
        self.label_influence.set_text("influence %s" % self.instance.influence)
        self.label_scrap.set_text("scrap %s" % self.instance.scrap)

    def add_to_gui(self, gui):
        gui.add(self.container, self.position[0], self.position[1])


class WeaponBar:


    def __init__(self, ship = None):
        self.ship = ship
        self.container = pgui.Container(width=300, height=100)
        self.position = 15,15
        #List of 3 null slots
        self.weapon_slot = {}

        self.button_group = pgui.Group()
        for i in range(3):
            button = pgui.Radio(self.button_group, i, width=100, height=100)
            button.style.width = 128
            button.style.height= 128
            print(button.__sizeof__())
            self.container.add(button, i * 143, 0)
            self.weapon_slot[i] = None
            self.__setattr__("button%s" % i, button)

        def switch_weapon(value):
            key = value.value
            if self.ship is not None:
                print(self.weapon_slot)
                self.ship.weapon = self.weapon_slot[key]

        self.button_group.connect(pgui.CHANGE, switch_weapon, self.button_group)

        self.update()

    def select(self, key):
     weapon_button = self.__getattribute__("button%s" % key)
     ##self.ship.weapon = self.weapon_slot[key]
     weapon_button.click()

    #Set proper icons and shit
    def update(self):
        for key in self.weapon_slot.keys():
            weapon_button = self.__getattribute__("button%s" % key)
            if self.weapon_slot.get(key) is None:
                weapon_button.style.on = self.highlighted_icon(texture["weapon0_icon"])
                weapon_button.style.off = texture["weapon0_icon"]
            else:
                weapon = self.weapon_slot.get(key)
                weapon_button.style.on = self.highlighted_icon(weapon.icon)
                weapon_button.style.off = weapon.icon

    def highlighted_icon(self, my_tex):
        new_tex= my_tex.copy()
        new_tex.blit(texture["weapon_highlight"], (0,0))
        return new_tex

    def add_to_gui(self, gui):
        gui.add(self.container, self.position[0], self.position[1])


class HealthBar:


    def __init__(self, ship = None):
        self.ship = ship
        self.container = pgui.Container(width=300, height=100)
        self.position = 15,165
        #List of 3 null slots

        self.button_group = pgui.Group()
        for i in range(3):
            button = pgui.Radio(self.button_group, i, width=100, height=100)
            button.style.width = 128
            button.style.height= 128
            print(button.__sizeof__())
            self.container.add(button, i * 143, 0)
            self.weapon_slot[i] = None
            self.__setattr__("button%s" % i, button)

        def switch_weapon(value):
            key = value.value
            if self.ship is not None:
                print(self.weapon_slot)
                self.ship.weapon = self.weapon_slot[key]

        self.button_group.connect(pgui.CHANGE, switch_weapon, self.button_group)

        self.update()

    def select(self, key):
     weapon_button = self.__getattribute__("button%s" % key)
     ##self.ship.weapon = self.weapon_slot[key]
     weapon_button.click()

    #Set proper icons and shit
    def update(self):
        for key in self.weapon_slot.keys():
            weapon_button = self.__getattribute__("button%s" % key)
            if self.weapon_slot.get(key) is None:
                weapon_button.style.on = self.highlighted_icon(texture["weapon0_icon"])
                weapon_button.style.off = texture["weapon0_icon"]
            else:
                weapon = self.weapon_slot.get(key)
                weapon_button.style.on = self.highlighted_icon(weapon.icon)
                weapon_button.style.off = weapon.icon

    def highlighted_icon(self, my_tex):
        new_tex= my_tex.copy()
        new_tex.blit(texture["weapon_highlight"], (0,0))
        return new_tex

    def add_to_gui(self, gui):
        gui.add(self.container, self.position[0], self.position[1])
