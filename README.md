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
    
    Sphere(rootNode, name="sphere", withTranslation=[-5.0, 0.0, 0.0])
    Cube(rootNode, name="cube", withTranslation=[5.0,0.0,0.0])

    ElasticMaterialObject(rootNode, name="dragon",
                          fromVolumeMesh="mesh/liver.msh",
                          withSurfaceMesh="mesh/dragon.stl"
                          withTranslation=[0.0,0.0,0.0])

    Floor(rootNode, name="plane", withTranslation=[0.0, -1.0, 0.0])
```

The API documentation is available at [readthedocs](http://stlib.readthedocs.io/en/latest/index.html)

