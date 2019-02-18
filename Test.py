from ShaderLib import ShaderProcess
import numpy as np

def shader(x, y, w, h):
    return np.array([np.uint8(255 * x/w), np.uint8(255 * x/h), np.uint8(255 * (x * y)/(w * h)), 255])

sh = ShaderProcess()

sh.runAdditiveShader(shader)

sh.toImage("test.png")
