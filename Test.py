from ShaderLib import ShaderProcess, MultiShader
import numpy as np

def shader(xe):
    x = xe[0]
    y = xe[1]
    u = xe[2]
    v = xe[3]
    e = np.uint8(v * 255)
    return np.array([e, e, e, 255])

def masterShader(x, y, u, v, ls):
    e = ls["sh1"].getPixel(x, y)[0] * (1-u) * v ** 2
    return np.array([e, e, e, 255])

sh = ShaderProcess(height=2048, width=2048)

sh.runShader(shader)

sh.toImage("test3.png")

# msh = MultiShader(height=256, width=256)

# msh.addSubShader("sh1", sh, shader)

# msh.runShader(masterShader)

# msh.toImage("test2.png")
