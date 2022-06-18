import pygame
from OpenGL.GL import *
import time
from game import Game, GameState


class App:

    def __init__(self):

        pygame.init()
        self.display = (800, 600)

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                            pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(self.display, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption('Hooman')

        self.mainloop()

    def mainloop(self):
        cur_time = time.time()
        game = Game(self.display)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.delete()
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    game.prevState = game.state
                    game.state = GameState.JUMPING
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            prev_time = cur_time
            cur_time = time.time()
            dt = cur_time - prev_time

            game.update(dt)
            game.render()

            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == "__main__":
    App()
