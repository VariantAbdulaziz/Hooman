class Palette:

    def __init__(self, primary, secondary) -> None:
        self.primary = primary
        self.secondary = secondary

    def light():
        return Palette((0.4, 0.4, 0.4), (0.8, 0.8, 0.8))

    def dark():
        return Palette((0.8, 0.8, 0.8), (0.4, 0.4, 0.4))
