import enum


class GameState(enum.Enum):
    ACTIVE = 0
    MENU = 1


class Game:
    def __init__(self, display) -> None:
        pass
    
    def processInput(self, dt, isJumping):
        pass
    
    def render(self):
        pass

    def delete(self):
        pass