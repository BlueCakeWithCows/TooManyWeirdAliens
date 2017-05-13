from entity.actor import Entity
from misc import add_rectangular, sub_rectangular, scale_rectangular
from pygame import Rect
from pgu import text, gui as pgui
from assets import value
class Window:
    debug = False
    update_list = []
    gui_list = []

    def __init__(self):
        self.camera = Camera(self, None)

        self.gui = pgui.App()
        self.gui_container = pgui.Container(width=value["init.virtual_width"], height=value["init.virtual_height"])
        self.gui.init(self.gui_container)

    def draw(self, screen):
        for i in self.update_list:
            if i.is_gui() or self.camera.on_screen(i):
                i.draw(screen, self.camera.position)

        if self.debug:
            for i in self.update_list:
                i.debug_draw(screen, self.camera.position)

        self.gui.paint(screen)

        return

    def update_gui(self):
        self.gui_container.widgets.clear()
        for i in self.gui_list:
            x,y = i.position
            i.add_to_gui(self.gui_container)
        self.gui.init(self.gui_container)
    def add_gui(self, element):
        self.gui_list.append(element)
        element.add_to_gui(self.gui_container)

    def remove_gui(self, element):
        self.gui_list.remove(element)
        element.remove_from_gui(self.gui_container)

    def update(self, deltaTime):
        self.listen(deltaTime)
        for i in self.update_list:
            i.update(deltaTime)
        self.camera.update(deltaTime)
        return

    # Override below methods
    def listen(self, deltaTime):
        pass

    def pass_event(self, event):
        self.gui.event(event)


class Camera(Entity):

    def __init__(self, instance, target, offset= (0,0)):
        Entity.__init__(self, instance)
        self.target = target
        self.offset = offset
        self.rect = Rect(sub_rectangular(self.position, (0, 0)), scale_rectangular(self.offset, -2))
    def on_screen(self, o):
        if o.drawable is not None and o.drawable.image is not None and o.drawable.position is not None:
            r = Rect(o.drawable.position, (o.drawable.image.get_size()))
            return r.colliderect(self.rect)
        return True

    def point_on_screen(self, o):
        return self.rect.collidepoint(o)

    def update(self, delta_time):
        if self.target is not None:
            self.position = add_rectangular(self.target.position, self.offset)
            self.rect = Rect(sub_rectangular(self.position, (0, 0)), scale_rectangular(self.offset, -2))

