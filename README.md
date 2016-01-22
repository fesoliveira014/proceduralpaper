# Procedural Modeling of Buildings
Implemetation of the paper "Procedural Modeling of Buildings", by Peter Wonka and Pascal Müller. 

## Dependencies
In order to use this application, you must have **Python 3.x** and the following modules:

- Vispy
- Numpy 1.09+

## Usage
Simply run ```python app.py```

Note that the ruleset filepath is hardcoded. That will be changed on future iterations.

## Observations
Note that this is an attempt on implementing the basic concepts of Wonka and Müller's paper. Some of the described rules and methods used to do more sophisticated generation operations have not been implemented, such as some scope rules, occlusion queries and snapping.

## Known Issues
- The visualizer is presenting a problem when rendering the models. When moving the camera backwards, the textures might go black at some steps.
- When rotating the model, the textures become overlapped in the front and back of the model. Might be due Phong shading not working properly or to Vispy texture engine.
- Models that are over 3000 vertices might take a while to render. The bottleneck is yet to be found.

## License
This code is free to use and modify, only being requested that the author is given credit for the original code.
