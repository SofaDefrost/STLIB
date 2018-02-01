# -*- coding: utf-8 -*-

def RigidObject(node, name="rigidobject", shapeFromFile=None,
                translation=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0], scale=1.0,
                totalmass=1.0,
                color=[1.0, 1.0, 0.0]):
    """Creates and adds rigid body from a surface mesh.

    Args:
        shapeFromFile (str):  The path or filename pointing to surface mesh file.

        totalmass (float):   The mass is distributed according to the geometry of the object.

        color (vec3f):  The default color used for the rendering of the object.

        translation (vec3f):   Apply a 3D translation to the object.

        rotation (vec3f):   Apply a 3D rotation to the object in Euler angles.

        scale (vec3f):   Apply an uniform scaling to the object.

    Structure:
            .. sourcecode:: qml

                Node : {
                    name : "rigidobject"
                    MechanicalObject,
                    UniformMass,
                    UncoupledConstraintCorrection,

                    Node : {
                        name : "collision",
                        Mesh,
                        MechanicalObject,
                        Triangle,
                        Line,
                        Point,
                        RigidMapping
                    }
                    Node : {
                       name : "visual"
                       OglModel,
                       RigidMapping
                    }
                }
    """
    #### mechanics
    cube =node.createChild(name)

    cube.createObject('MechanicalObject', name="mstate", template="Rigid", scale=scale, translation=translation, rotation=rotation)
    cube.createObject('UniformMass', name="mass", totalmass=totalmass)
    cube.createObject('UncoupledConstraintCorrection')

    #### collision
    cubeCollis = cube.createChild('collision')
    cubeCollis.createObject('MeshObjLoader', name="loader", filename=shapeFromFile, triangulate="true",
                             scale=scale, translation=translation, rotation=rotation )

    cubeCollis.createObject('Mesh', src="@loader")
    cubeCollis.createObject('MechanicalObject')
    cubeCollis.createObject('Triangle')
    cubeCollis.createObject('Line')
    cubeCollis.createObject('Point')
    cubeCollis.createObject('RigidMapping')

    #### visualization
    cubeVisu = cube.createChild('visual')
    cubeVisu.createObject('OglModel', name="visual",
                          fileMesh=shapeFromFile, color=color,
                          scale=scale, translation=translation, rotation=rotation)
    cubeVisu.createObject('RigidMapping')

    return cube

def createScene(rootNode):
    from stlib.scene import STLIBHeader
    from stlib.solver import DefaultSolver

    STLIBHeader(rootNode)
    DefaultSolver(rootNode)
    RigidObject(rootNode, shapeFromFile="mesh/smCube27.obj", translation=[-5.0,0.0,0.0])
    RigidObject(rootNode, shapeFromFile="mesh/dragon.obj", translation=[ 0.0,0.0,0.0])
    RigidObject(rootNode, shapeFromFile="mesh/smCube27.obj", translation=[ 5.0,0.0,0.0])
