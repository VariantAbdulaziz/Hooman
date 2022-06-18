from OpenGL.GL import *
import numpy as np
import pyrr
from random import randint

import enum
from utils.palette import Palette
from utils.game_object import GameObject
from utils.material import Material

from utils.sprite_renderer import SpriteRenderer
from utils.shader import Shader

FLOOR = 100
GRAVITY = -10
AVATAR_OFFSET = 15


class GameState(enum.Enum):
    RUNNING = 0
    MENU = 1
    JUMPING = 2


class Game:
    
    def __init__(self, display) -> None:
        self.theme = Palette.dark()
        self.score = 0
        self.maxScore = 0
        self.prevState = None
        self.state = GameState.RUNNING
        self.width, self.height = display

        glClearColor(*self.theme.secondary, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, self.width, self.height)

        hooman_materials = [Material(f"textures/avatar/Run ({i}).png") for i in range(1, 10)] + \
                           [Material("textures/avatar/Jump (1).png"), Material("textures/avatar/Dead (1).png")]
        cactus_materials = [Material(f"textures/obstacles/Cactus ({i}).png") for i in range(1, 4)]
        ground_materials = [Material("textures/env/BG.png")]

        self.ground = GameObject([0, 0, 0], [self.width, self.height, 0], [0, 0], ground_materials)
        self.hooman = GameObject([10, FLOOR - AVATAR_OFFSET, 0], np.array([402, 511, 0])/4, [0, 6], hooman_materials)
        self.cactus = GameObject([self.width + 100, FLOOR, 0], [50, 100, 0], [400, 0], cactus_materials)

        projection = pyrr.matrix44.create_orthogonal_projection(0, self.width, 0, self.height, -1, 1, np.float32)

        self.program = Shader("triangle.vertex.shader", "triangle.fragment.shader")
        self.program.use()

        glUniformMatrix4fv(
            glGetUniformLocation(self.program.getId(), "projection"),
            1, GL_FALSE, projection
        )
        self.renderer = SpriteRenderer(self.program)

        glUniform1i(glGetUniformLocation(self.program.getId(), "image"), 0)
        glUniform3fv(glGetUniformLocation(self.program.getId(), "spriteColor"), 1, self.theme.primary)

    def update(self, dt):

        if self.prevState != GameState.MENU and self.state != GameState.MENU:

            self.cactus.position[0] -= (dt * self.cactus.velocity[0])

            if self.cactus.position[0] < self.hooman.position[0] - 100:
                self.cactus.position[0] = self.width + 10
                self.cactus.frame = randint(0, 2)

                self.score += 1
                if self.score > self.maxScore:
                    self.maxScore = self.score
        
            if self.state == GameState.JUMPING:
                self.hooman.frame = -2
                self.hooman.velocity[1] += GRAVITY * dt
                self.hooman.position[1] += self.hooman.velocity[1]
                if self.hooman.position[1] <= self.cactus.position[1] - AVATAR_OFFSET:
                    self.hooman.velocity[1] = 6
                    self.hooman.position[1] = self.cactus.position[1] - AVATAR_OFFSET
                    self.state = GameState.RUNNING
            else:
                self.hooman.frame = (self.hooman.frame + 1) % (len(self.hooman.materials) - 2)

            if (self.cactus.position[0] <= self.hooman.position[0]+self.hooman.size[0] - 5 * AVATAR_OFFSET and
                self.hooman.position[0] + AVATAR_OFFSET <= self.cactus.position[0]+self.cactus.size[0] and
                self.hooman.position[1] + AVATAR_OFFSET <= self.cactus.position[1]+self.cactus.size[1]):

                self.prevState = self.state
                self.state = GameState.MENU
        elif self.prevState == GameState.MENU and self.state != GameState.MENU:
            self.prevState = self.state
            self.score = 0
            self.cactus.position = [self.width + 100, FLOOR, 0]
            self.hooman.position = [10, FLOOR - AVATAR_OFFSET, 0]
            self.cactus.frame = (randint(0, 8)) % len(self.cactus.materials)
        else:
            self.hooman.frame = -1

    def render(self):
        self.ground.draw(self.renderer)
        self.cactus.draw(self.renderer)
        self.hooman.draw(self.renderer)

    def delete(self):
        self.program.delete()
        self.renderer.delete()
