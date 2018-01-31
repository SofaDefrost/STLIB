# STLIB
Sofa Template Library

This library should contains sofa scene template.
It shoul contains common scene template used regularly to make the writing of scene with Sofa easy. 
The templates should be compatible with .pyscn and PSL scenes. The library also contains cool
utilitary function we should always consider to use.

```python
from stlib.scenes import STLIBHeader
from stlib.physics.rigid.shapes import Cube, Sphere, Plane
from stlib.physics.deformable import ElasticMaterialObject

from stlib.animate import AnimationManager, Animation, animate

#def myAnimAction(target, factor):
#    target.

def createScene(rootNode):
    STLIBHeader(rootNode)
    AnimationManager(rootNode)

    #Sphere(rootNode, name="sphere", translation=[0.0, 1.0, 0.0])
    #Cube(rootNode, name="cube", translation=[0.0,1.0,0.0])

    ElasticMaterialObject(name="dragon", translation=[0.0,1.0,0.0])

    Plane(rootNode, name="plane", translation=[0.0, -1.0, 0.0])

    animate( ( myAction, { "target" :   } ) )
```
