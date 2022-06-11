from OpenGL.GL import *
from OpenGL.GL.shaders import *
import os


class Shader:
    def getFileContents(filename):
        p = os.path.join(os.getcwd(), "shaders", filename)
        return open(p, 'r').read()

    def __init__(self, vert_file_path, fragment_file_path) -> None:
        vertexShaderContent = Shader.getFileContents(vert_file_path)
        fragmentShaderContent = Shader.getFileContents(fragment_file_path)

        vertexShader = compileShader(vertexShaderContent, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragmentShaderContent, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()
        glAttachShader(self.program, vertexShader)
        glAttachShader(self.program, fragmentShader)
        glLinkProgram(self.program)

    def getId(self):
        return self.program

    def use(self):
        glUseProgram(self.program)

    def delete(self):
        glDeleteProgram(self.program)
