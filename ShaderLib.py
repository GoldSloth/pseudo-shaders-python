import numpy as np
from PIL import Image

class ShaderProcess:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self._img = np.ndarray((height, width, 4), dtype=np.uint8)
        self._img.fill(0)
    
    def runAdditiveShader(self, shader):
        for x in range(self._img.shape[0]):
            for y in range(self._img.shape[1]):
                self._img[x, y] = shader(x, y, self.width, self.height)
    
    def toImage(self, file):
        im = Image.fromarray(self._img)
        im.save(file, "PNG")