import numpy as np
from PIL import Image
import numexpr
import multiprocessing
import time

class BaseShader:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.image = np.ndarray((height, width, 4), dtype=np.uint8)
    
    def getPixel(self, u, v):
        vU = np.floor(u * self.width)
        vV = np.floor(v * self.height)
        return self.image[vU, vV]

    def saveImage(self, filename):
        im = Image.fromarray(self.image)
        im.save(filename, "PNG")

class MultiThreadedShader(BaseShader):
    def __init__(self, height, width, threads):
        self.threads = threads
        return super().__init__(height, width)
    
    def _taskGenerator(self):
        for y in range(self.width):
            for x in range(self.height):
                v = y / self.height
                u = x / self.width
                yield (v, u)

    def runShader(self, shader):
        # This code is rather nasty, but it works.
        self.p = multiprocessing.Pool(self.threads)
        result = self.p.map(shader, [n for n in self._taskGenerator()])
        for y in range(self.width):
            for x in range(self.height):
                self._img[y, x] = result[x * self.width + y]

class LayerShader(BaseShader):
    def __init__(self, height, width):
        self.subShaders = {}
        return super().__init__(width, height)

    def addSubShader(self, shaderID, shader, shaderProgram):
        shader.runShader(shaderProgram)
        self.subShaders[shaderID] = shader

    def runShader(self, masterShader):
        for y in range(self._img.shape[0]):
            for x in range(self._img.shape[1]):
                v = y / self.height
                u = x / self.width
                
                self._img[y, x] = masterShader(u, v, self.subShaders)

# class NumExprShader(MultiShader):
#     def __init__(self, width=800, height=600):
#         super().__init__(width=width, height=height)

#     def compileShader(self, expression, typeList):
#         self.shader = numexpr.NumExpr(expression, typeList)
    
#     def runCompiledShader(self)