from entity.actor import Entity
from misc import add_rectangular, sub_rectangular, scale_rectangular
from pygame import Rect
class Window:
    debug = False
    draw_list = []
    update_list = []

    def __init__(self):
        self.camera = Camera(self, None)

    def draw(self, screen):
        for i in self.draw_list:
            if i.is_gui() or self.camera.on_screen(i):
                i.draw(screen, self.camera.position)

        if self.debug:
            for i in self.draw_list:
                i.debug_draw(screen, self.camera.position)
        return

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
        pass


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

