from OpenGL.GL import *
import numpy as np
import pyrr

import enum
from utils.palette import Palette
from utils.game_object import GameObject
from utils.material import Material

from utils.sprite_renderer import SpriteRenderer
from utils.shader import Shader



class GameState(enum.Enum):
    ACTIVE = 0
    MENU = 1


class Game:
    
    def __init__(self, display) -> None:
        self.theme = Palette.light()
        self.score = 0
        self.maxScore = 0

        self.gameState = GameState.ACTIVE
        self.width, self.height = display

        glClearColor(*self.theme.secondary, 1.0)
        glViewport(0, 0, self.width, self.height)

        hooman_materials = [Material("textures/wall.jpg"), Material("textures/thousand.png")]
        cactus_materials = [Material("textures/wall.jpg")]

        self.hooman = GameObject([10, self.height/3, 0], [100, 100, 1], [0, 3], hooman_materials)
        self.cactus = GameObject([self.width + 100, self.height/3, 0], [50, 100, 1], [400, 0], cactus_materials)

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


    def processInput(self, dt, isJumping):

        if self.gameState == GameState.ACTIVE:

            self.cactus.position[0] -= (dt * self.cactus.velocity[0])

            if self.cactus.position[0] < self.hooman.position[0] - 100:
                self.cactus.position[0] = self.width + 10

                self.score += 1
                if self.score > self.maxScore:
                    self.maxScore = self.score
        
            if isJumping:
                self.cactus.position[0] -= (dt * self.cactus.velocity[0]/5)
                self.hooman.frame = -2
                acc = -10
                self.hooman.velocity[1] += acc * dt
                self.hooman.position[1] += self.hooman.velocity[1]
                if self.hooman.position[1] <= self.cactus.position[1]:
                    self.hooman.velocity[1] = 3
                    self.hooman.position[1] = self.cactus.position[1]
                    isJumping = False
            else:
                self.hooman.frame = (self.hooman.frame + 1 ) % (len(self.hooman.materials) - 1)
            

            if (self.cactus.position[0] <= self.hooman.position[0]+self.hooman.size[0] and 
                self.hooman.position[0] <= self.cactus.position[0]+self.cactus.size[0] and
                self.hooman.position[1] <= self.cactus.position[1]+self.cactus.size[1] ):

                self.gameState = GameState.MENU
                isJumping = False
            
            return isJumping

        if self.gameState == GameState.MENU:
            if isJumping:
                self.gameState = GameState.ACTIVE
                self.score = 0
                self.cactus.position = [self.width + 100, self.height/3, 0]
                self.hooman.position = [10, self.height/3, 0]
                return True
            
            return False


    def render(self):
        self.hooman.draw(self.renderer)
        self.cactus.draw(self.renderer)

        if self.gameState == GameState.MENU:
            self.hooman.frame = -1

    def delete(self):
        self.program.delete()
        self.renderer.delete()
