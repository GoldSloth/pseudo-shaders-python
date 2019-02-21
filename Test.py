from ShaderLib import *
import numpy as np

def shader(arguments):
    u, v = arguments
    e = np.uint8(v * 255)
    return np.array([e, e, e, 255])

def masterShader(u, v, ls):
    e = ls["sh1"].getPixel(u, v)[0] * (1-u) * v ** 2
    return np.array([e, e, e, 255])

sh = MultiThreadedShader(512, 512, 4)

sh.runShader(shader)

sh.saveImage("test1.png")


