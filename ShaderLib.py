import numpy as np
from PIL import Image
import numexpr
import multiprocessing
import time

class ShaderProcess:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self._img = np.ndarray((height, width, 4), dtype=np.uint8)
        self._img.fill(0)
    
    def _taskGenerator(self, width, height):
        for y in range(width):
            for x in range(height):
                v = y / self.height
                u = x / self.width
                yield (y, x, v, u)
        

    def runShader(self, shader, threads=4):
        self.p = multiprocessing.Pool(threads)
        t = time.time()
        result = self.p.map(shader, [n for n in self._taskGenerator(self.width, self.height)])
        for y in range(self.width):
            for x in range(self.height):
                self._img[y, x] = result[x * self.width + y]
        print("Task [{}] run took {} seconds".format(__name__, time.time()-t))
    
    def toImage(self, file):
        t = time.time()
        im = Image.fromarray(self._img)
        im.save(file, "PNG")
        print("Task [{}] image saving took {} seconds".format(__name__, time.time()-t))

    def getPixel(self, x, y):
        return tuple(self._img[x, y])

class MultiShader(ShaderProcess):
    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
        self.subShaders = {}

    def addSubShader(self, shaderID, shader, shaderProgram, threads=4):
        shader.runShader(shaderProgram, threads=threads)
        self.subShaders[shaderID] = shader


    def runShader(self, masterShader):
        for y in range(self._img.shape[0]):
            for x in range(self._img.shape[1]):
                v = y / self.height
                u = x / self.width
                
                self._img[y, x] = masterShader(y, x, u, v, self.subShaders)

class NumExprShader(MultiShader):
    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)

    def compileShader(self, expression, typeList):
        self.shader = numexpr.NumExpr(expression, typeList)
    
    def runCompiledShader(self)