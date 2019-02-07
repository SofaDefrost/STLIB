# STLIB
Sofa Template Library

This library should contains sofa scene template.
It should contains common scene template used regularly to make the writing of scene with Sofa easy. 
The templates should be compatible with .pyscn and PSL scenes. The library also contains cool
utilitary function we should always consider to use.

```python
from stlib.scene import MainHeader
from stlib.solver import DefaultSolver
from stlib.physics.rigid import Cube, Sphere, Floor
from stlib.physics.deformable import ElasticMaterialObject

def createScene(rootNode):
    MainHeader(rootNode)
    DefaultSolver(rootNode)
    
    Sphere(rootNode, name="sphere", translation=[-5.0, 0.0, 0.0])
    Cube(rootNode, name="cube", translation=[5.0,0.0,0.0])

    ElasticMaterialObject(rootNode, name="dragon",
                          volumeMeshFileName="mesh/liver.msh",
                          surfaceMeshFileName="mesh/dragon.stl",
                          translation=[0.0,0.0,0.0])

    Floor(rootNode, name="plane", translation=[0.0, -1.0, 0.0])
```

The API documentation is available at [readthedocs](http://stlib.readthedocs.io/en/latest/index.html)

# To build STLIB 
First you need to have [SOFA](https://github.com/Sofa-framework/sofa) on your machine, since to build STLIB you will need to build it through SOFA.

`git clone https://github.com/sofa-framework/sofa.git`

Then clone STLIB

`git clone https://github.com/SofaDefrost/STLIB.git`

In the configurations of SOFA build settings, set `PLUGIN_SOFAPYTHON` to `ON` and `SOFA_EXTERNAL_DIRECTORIES` to the absolute path of STLIB `your_path/STLIB`

Then build SOFA

Now you should be able to use `import stlib` in python from inside SOFA (running the .py from runSofa)
