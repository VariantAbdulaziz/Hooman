from OpenGL.GL import *
import numpy as np
import pyrr


class SpriteRenderer:

    def __init__(self, program) -> None:
        self.program = program
        vertexes = np.array([
            0.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0,

            0.0, 1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
        ], dtype=np.float32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * vertexes.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * vertexes.itemsize, ctypes.c_void_p(2 * vertexes.itemsize))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self, position, scale, material):
        model = pyrr.matrix44.create_identity()
        model = pyrr.matrix44.multiply(
            m1=model,
            m2=pyrr.matrix44.create_from_scale(
                scale=pyrr.Vector3(scale), dtype=np.float32
            )
        )
        model = pyrr.matrix44.multiply(
            m1=model,
            m2=pyrr.matrix44.create_from_translation(
                vec=pyrr.Vector3(position), dtype=np.float32
            )
        )
        material.bind()

        self.program.use()

        glUniformMatrix4fv(
            glGetUniformLocation(self.program.getId(), "model"),
            1, GL_FALSE, model
        )

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

    def delete(self):
        glDeleteVertexArrays(1, (self.VBO,))
        glDeleteBuffers(1, (self.VAO,))
