
# -*- coding: utf-8 -*-

def RigidObject(node, name="rigidobject", shapeFromFile=None,
                withTranslation=[0.0,0.0,0.0], withRotation=[0.0,0.0,0.0], withScale=1.0,
                withTotalMass=1.0, withVolume=1.0, withInertiaMatrix=[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
                withColor=[1.0, 1.0, 0.0], isAStaticObject=False):
    """Creates and adds rigid body from a surface mesh.

    Args:
        shapeFromFile (str):  The path or filename pointing to surface mesh file.

        withTotalMass (float):   The mass is distributed according to the geometry of the object.

        withColor (vec3f):  The default color used for the rendering of the object.

        withTranslation (vec3f):   Apply a 3D translation to the object.

        withRotation (vec3f):   Apply a 3D rotation to the object in Euler angles.

        withScale (vec3f):   Apply an uniform scaling to the object.

        isAStaticObject (bool): The object does not move in the scen but react to collision.

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
                        scale=withScale,
                        translation=withTranslation, rotation=withRotation)

    cube.createObject('UniformMass', name="mass", mass=[withTotalMass, withVolume, withInertiaMatrix[:]])

    if not isAStaticObject:
        cube.createObject('UncoupledConstraintCorrection')

    #### collision
    cubeCollis = cube.createChild('collision')
    cubeCollis.createObject('MeshObjLoader', name="loader", filename=shapeFromFile, triangulate="true",
                             scale=withScale)

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
                          fileMesh=shapeFromFile, color=withColor,
                          scale=withScale)
    cubeVisu.createObject('RigidMapping')

    return cube

def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.solver import DefaultSolver

    MainHeader(rootNode)
    DefaultSolver(rootNode)
    RigidObject(rootNode, shapeFromFile="mesh/smCube27.obj", withTranslation=[-5.0,0.0,0.0])
    RigidObject(rootNode, shapeFromFile="mesh/dragon.obj", withTranslation=[ 0.0,0.0,0.0])
    RigidObject(rootNode, shapeFromFile="mesh/smCube27.obj", withTranslation=[ 5.0,0.0,0.0])
