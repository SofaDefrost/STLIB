
# -*- coding: utf-8 -*-

def RigidObject(node, name="RigidObject", surfaceMeshFileName=None,
                translation=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0], uniformScale=1.0,
                totalMass=1.0, volume=1.0, inertiaMatrix=[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
                color=[1.0, 1.0, 0.0], isAStaticObject=False):
    """Creates and adds rigid body from a surface mesh.

    Args:
        surfaceMeshFileName (str):  The path or filename pointing to surface mesh file.

        totalMass (float):   The mass is distributed according to the geometry of the object.

        color (vec3f):  The default color used for the rendering of the object.

        translation (vec3f):   Apply a 3D translation to the object.

        rotation (vec3f):   Apply a 3D rotation to the object in Euler angles.

        uniformScale (vec3f):   Apply a uniform scaling to the object.

        isAStaticObject (bool): The object does not move in the scene (e.g. floor, wall) but react to collision.

    Structure:
            .. sourcecode:: qml

                Node : {
                    name : "rigidobject"
                    MechanicalObject,
                    UniformMass,
                    UncoupledConstraintCorrection,
                    *EulerImplicit,
                    *SparseLDLSolver,

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

    if not isAStaticObject:
        cube.createObject('EulerImplicit', name='odesolver')
        cube.createObject('CGLinearSolver', name='Solver')

    cube.createObject('MechanicalObject', name="mstate", template="Rigid",
                      translation=translation, rotation=rotation)

    cube.createObject('UniformMass', name="mass", mass=[totalMass, volume, inertiaMatrix[:]])

    if not isAStaticObject:
        cube.createObject('UncoupledConstraintCorrection')

    #### collision
    cubeCollis = cube.createChild('collision')
    cubeCollis.createObject('MeshObjLoader', name="loader", filename=surfaceMeshFileName, triangulate="true",
                            translation=translation, rotation=rotation,scale=uniformScale)

    cubeCollis.createObject('Mesh', src="@loader")
    cubeCollis.createObject('MechanicalObject')

    if isAStaticObject:
        cubeCollis.createObject('Triangle', moving=False, simulated=False)
        cubeCollis.createObject('Line', moving=False, simulated=False)
        cubeCollis.createObject('Point', moving=False, simulated=False)
    else:
        cubeCollis.createObject('Triangle')
        cubeCollis.createObject('Line')
        cubeCollis.createObject('Point')

    cubeCollis.createObject('RigidMapping')

    #### visualization
    cubeVisu = cube.createChild('visual')
    cubeVisu.createObject('OglModel', name="visual",
                          fileMesh=surfaceMeshFileName, color=color,
                          translation=translation, rotation=rotation,scale=uniformScale)
    cubeVisu.createObject('RigidMapping')

    return cube

def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.solver import DefaultSolver

    MainHeader(rootNode)
    DefaultSolver(rootNode)
    RigidObject(rootNode, surfaceMeshFileName="mesh/smCube27.obj", translation=[-20.0,0.0,0.0])
    RigidObject(rootNode, surfaceMeshFileName="mesh/dragon.obj", translation=[ 0.0,0.0,0.0])
    RigidObject(rootNode, surfaceMeshFileName="mesh/smCube27.obj", translation=[ 20.0,0.0,0.0])
