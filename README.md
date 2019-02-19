# Pseudo shaders in Python

The file `ShaderLib.py` can be imported - It contains two classes
- `ShaderProcess`
- `MultiShader` \- Inherits from `ShaderProcess`

### _Shader Process_
The `ShaderProcess` class has two optional arguments, **width** and **height**.<br>
You can run the shader by passing in a function to the ``runShader(shader)`` method.

Example:
```Python
def shader(arguments):
    x, y, u, v = arguments
    # x, y: the position of the pixel: should not be used commonly. Instead use u and v.
    # u, v: the relative position of the pixel (x/width, y/height) in the image. Float between 0 and 1.
    e = np.uint8(v * 255)
    # Output must be a np.array consisting of np.uint8 - 0 to 255. RGBA format.
    return np.array([e, e, e, 255])
```

The ``runShader`` method is multithreaded - by default it will use 4 threads. The performance roughly follows an exponential between square size of image and time. A higher number of threads may be specified with the optional argument `threads`.

The contents of the shader can be saved to an image using the ``toImage(file)`` method. The ``file`` argument refers to filename.

The `getPixel(x, y)` method is used in a ``MultiShader`` in order to retrieve the colour data for an individual pixel of a `ShaderProcess`.

### _MultiShader_

The methods `runShader` and `toImage` are to be used in exactly the same way as in `ShaderProcess`.

The class adds the method ``addSubShader`` - which can be used to add an existing image of the ``ShaderProcess`` type. When the image is added, it will run the shader provided and add it to the `MultiShader`'s group of sub shaders. The image will be stored paired with the ``ShaderID`` provided.

When all the sub shaders are loaded as desired, a *"master shader"* can be applied to produce a final image.

In theory a `MultiShader` can be used as a sub shader - I have not experimented too far into this, however.

The `MultiShader` does not currently run the *"master shader"* in a parallel fasion, but that is planned.

An example of a *"master program"*:

```Python
def masterShader(x, y, u, v, ls):
    # Currently collapsed arguments are not needed.
    # x, y: Somewhat useful now in getPixel(x, y)
    # u, v: Same as base ShaderProcess
    # ls: A dictionary relating ShaderID with sub shaders
    e = ls["sh1"].getPixel(x, y)[0] * (1-u) * v ** 2
    # ls["sh1"] retrieves the subProcess with ID "sh1"
    return np.array([e, e, e, 255])
```

### Planned features:
- Loading images from disk for use in a `MultiShader`.
- Blending shaders - so multiple processes can be run on the same image.
- Parallel processing of the *"master shader"* in order to improve performance.
- Unit square bilerp for uv of a `subShader`