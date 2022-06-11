class GameObject:
    def __init__(self, position, size, velocity, materials) -> None:
        self.position = position
        self.size = size
        self.velocity = velocity
        self.materials = materials
        self.frame = 0

    def draw(self, renderer):
        renderer.draw(self.position, self.size, self.materials[self.frame])
