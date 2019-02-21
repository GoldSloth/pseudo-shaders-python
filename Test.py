from ShaderLib import *
import numpy as np

def shader(arguments):
    u, v = arguments
    e = np.uint8(v * 255)
    return np.array([e, e, e, 255])

def shader2(arguments):
    u, v = arguments
    e = np.uint8(u * v * 255)
    return np.array([e, e, e, 255])

def masterShader(u, v, ls):
    e = ls["sh1"].getPixel(u, v)
    f = ls["sh2"].getPixel(u, v)
    return (e/2 + f/2)

sh1 = MultiThreadedShader(512, 512, 4)

sh1.runShader(shader)

sh1.saveImage("test1.png")

sh2 = MultiThreadedShader(512, 512, 4)

sh2.runShader(shader2)

sh2.saveImage("test2.png")

lsh = LayerShader(512, 512)

lsh.putShader("sh1", sh1)
lsh.putShader("sh2", sh2)

lsh.runShader(masterShader)

lsh.saveImage("test3.png")

nelsh = NumExprLayerShader(512, 512)

nelsh.sh1 = sh1.image
nelsh.sh2 = sh2.image

nelsh.runShader("sh1 * 0.1 + sh2 * 0.9")

nelsh.saveImage("test4.png")

bi = BaseImage("test4.png")

bi.saveImage("test5.png")
