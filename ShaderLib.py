import numpy as np
from PIL import Image
import numexpr
import multiprocessing
import time

class BaseShader:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = np.ndarray((width, height, 4), dtype=np.uint8)
    
    def getPixel(self, u, v):
        vU = int(u * self.width)
        vV = int(v * self.height)
        return self.image[vU, vV]

    def saveImage(self, filename):
        im = Image.fromarray(self.image)
        im.save(filename, "PNG")

class BaseImage(BaseShader):
    def __init__(self, filename):
        im = Image.open(filename)
        self.width = im.size[1]
        self.height = im.size[0]
        self.image = np.array(im.getdata()).reshape(im.size[1], im.size[0], 4).astype("uint8")


class MultiThreadedShader(BaseShader):
    def __init__(self, width, height, threads):
        self.threads = threads
        return super().__init__(width, height)
    
    def _taskGenerator(self):
        for x in range(self.width):
            for y in range(self.height):
                u = x / self.width
                v = y / self.height
                yield (u, v)

    def runShader(self, shader):
        # This code is rather nasty, but it works.
        self.p = multiprocessing.Pool(self.threads)
        result = self.p.map(shader, [n for n in self._taskGenerator()])
        for x in range(self.width):
            for y in range(self.height):
                self.image[x, y] = result[x * self.width + y]

class LayerShader(BaseShader):
    def __init__(self, width, height):
        self.subShaders = {}
        return super().__init__(width, height)

    def addSubShader(self, shaderID, shader, shaderProgram):
        shader.runShader(shaderProgram)
        self.subShaders[shaderID] = shader

    def putShader(self, shaderID, shader):
        self.subShaders[shaderID] = shader

    def runShader(self, masterShader):
        for x in range(self.width):
            for y in range(self.height):
                u = x / self.width
                v = y / self.height
                
                self.image[x, y] = masterShader(u, v, self.subShaders)

class NumExprLayerShader(BaseShader):
    def __init__(self, height, width):
        return super().__init__(width, height)

    def runShader(self, masterShader):
        self.image = numexpr.evaluate(masterShader, global_dict=vars(self)).astype('uint8')
        