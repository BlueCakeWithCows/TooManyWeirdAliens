def update(list_collidables):
    for i in range(len(list_collidables)):
        position, radius = list_collidables[i].position, list_collidables[i].radius
        for x in range(i+1, len(list_collidables)):
            if list_collidables[x].is_colliding(position, radius):
                print("Hipsta!")
