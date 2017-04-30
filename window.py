from entity.actor import Entity


class Window:
    debug = False
    draw_list = []
    update_list = []

    def __init__(self):
        self.camera = Camera(self, None)

    def draw(self, screen):
        for i in self.draw_list:
            i.draw(screen, self.camera.position)

        if self.debug:
            for i in self.draw_list:
                i.debug_draw(screen, self.camera.position)
        return

    def update(self, deltaTime):
        self.listen(deltaTime)
        for i in self.update_list:
            i.update(deltaTime)
        return

    # Override below methods
    def listen(self, deltaTime):
        pass

    def pass_event(self, event):
        pass


class Camera(Entity):
    def __init__(self, instance, target):
        Entity.__init__(self, instance)
        self.target = target

    def update(self, delta_time):
        if self.target is not None:
            self.position = self.target.position()
