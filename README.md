# Pseudo shaders in Python

The file `ShaderLib.py` can be imported - It contains the following classes
- `BaseShader`
- `MultiThreadedShader` \- Inherits from `BaseShader`
- `LayerShader` \- Inherits from `BaseShader`

## `BaseShader`
The `BaseShader` has little function and should not be used.

However its methods are used throughout.
#### Construction
Arguments:
- Width
- Height
#### ``saveImage(filename)``
Method to save a shader's image to file locally.
Arguments:
- Filename: A string relating to the where the file will be saved. Uses PIL.
#### ``getPixel(u, v)``
Method to get the colour information of an individual pixel. Returns an ``numpy.ndarray``.<br>
Arguments:
- u: Float relating to X position in image (0 to 1)
- v: Float relating to Y position in image (0 to 1)

### `MultiThreadedShader`
#### Construction
*See base shader*
Arguments:
- Threads: The total number of threads used when executing this shader.

### `runShader(shaderProgram)`
Runs the specified program on the shader's image.

Example:
```Python
def shader(arguments):
    u, v = arguments
    # u, v: the relative position of the pixel (x/width, y/height) in the image. Float between 0 and 1.
    e = np.uint8(v * 255)
    # Output must be a np.array consisting of np.uint8 - 0 to 255. RGBA format.
    return np.array([e, e, e, 255])
```
This method is multithreaded.

### _LayerShader_
#### Construction
*See base shader*

#### `addSubShader(shaderID, shader, shaderProgram)`
Used to add layers to a ``LayerShader``.
The shader will be run when added - There is no need to run it first.
Arguments:
- shaderID: A string identifying this layer.
- shader: A class descended from ``BaseShader``
- shaderProgram: The program to be run on the layer.
### runShader(masterShader)
Used to run a shader which has access to the layers added to the shader.
Arguments:
- masterShader: A shader which has access to all layers of the current ``LayerShader``
An example of a *"master program"*:

```Python
def masterShader(u, v, ls):
    # Currently collapsed arguments are not needed.
    # u, v: Same as base ShaderProcess
    # ls: A dictionary relating ShaderID with sub shaders
    e = ls["sh1"].getPixel(u, v)[0] * (1-u) * v ** 2
    # ls["sh1"] retrieves the subProcess with ID "sh1"
    return np.array([e, e, e, 255])
```

### Planned features:
- Loading images from disk
- Blending shaders - so multiple processes can be run on the same image.
- Parallel processing of the *"master shader"* in order to improve performance.
- NumExpr type shaders for very efficient, strict shaders.
