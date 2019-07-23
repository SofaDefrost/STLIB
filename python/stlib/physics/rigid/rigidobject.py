# -*- coding: utf-8 -*-
from stlib.visuals import VisualModel


def RigidObject(node, name="RigidObject",
                surfaceMeshFileName=None,
                translation=[0., 0., 0.],
                rotation=[0., 0., 0.],
                uniformScale=1.,
                totalMass=1.,
                volume=1.,
                inertiaMatrix=[1., 0., 0., 0., 1., 0., 0., 0., 1.],
                color=[1., 1., 0.],
                collisionMeshFileName=None,
                isAStaticObject=False,
                noSolver=False,
                collisionGroup=None):
    """Creates and adds rigid body from a surface mesh.

    Args:
        surfaceMeshFileName (str):  The path or filename pointing to surface mesh file.

        totalMass (float):   The mass is distributed according to the geometry of the object.

        color (vec3f):  The default color used for the rendering of the object.

        translation (vec3f):   Apply a 3D translation to the object.

        rotation (vec3f):   Apply a 3D rotation to the object in Euler angles.

        uniformScale (vec3f):   Apply a uniform scaling to the object.

        collisionMeshFileName (str):  The path or filename pointing to surface mesh file use for collision.

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
    object = node.createChild(name)

    if not isAStaticObject and not noSolver:
        object.createObject("EulerImplicitSolver", name='odesolver')
        object.createObject('CGLinearSolver', name='Solver')

    object.createObject('MechanicalObject', position=[0.,0.,0.,0.,0.,0.,1.],
                      name="dofs", template="Rigid3",
                      translation2=translation, rotation2=rotation, showObjectScale=uniformScale)

    object.createObject('UniformMass', name="mass", vertexMass=[totalMass, volume, inertiaMatrix[:]])

    if not isAStaticObject and not noSolver:
        object.createObject('UncoupledConstraintCorrection')

    #### collision
    objectCollis = object.createChild('CollisionModel')
    if collisionMeshFileName is None:
        collisionMeshFileName = surfaceMeshFileName

    if collisionMeshFileName.endswith(".stl"):
        objectCollis.createObject('MeshSTLLoader',
                                 name="loader",
                                 filename=collisionMeshFileName, scale3d=[uniformScale]*3)
    elif collisionMeshFileName.endswith(".obj"):
        objectCollis.createObject('MeshObjLoader',
                                 name="loader",
                                 filename=collisionMeshFileName, scale3d=[uniformScale]*3)
    else:
        print("Extension not handled in STLIB/python/stlib/visuals for file: "+str(collisionMeshFileName))


    objectCollis.createObject('MeshTopology', src="@loader")
    objectCollis.createObject('MechanicalObject', name="dofs")

    objectCollis.createObject('TriangleCollisionModel', name="Triangle", group=collisionGroup if collisionGroup is not None else " ")
    objectCollis.createObject('LineCollisionModel', name="Line", group=collisionGroup if collisionGroup is not None else " ")
    objectCollis.createObject('PointCollisionModel', name="Point", group=collisionGroup if collisionGroup is not None else " ")
    if isAStaticObject:
        objectCollis.Triangle.moving=False
        objectCollis.Line.moving=False
        objectCollis.Point.moving=False
        objectCollis.Triangle.simulated=False
        objectCollis.Line.simulated=False
        objectCollis.Point.simulated=False

    objectCollis.createObject('RigidMapping')

    #### visualization
    objectVisu = VisualModel(parent=object, surfaceMeshFileName=surfaceMeshFileName, color=color, scale=[uniformScale]*3)
    objectVisu.createObject('RigidMapping')

    return object

def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.solver import DefaultSolver

    MainHeader(rootNode)
    DefaultSolver(rootNode)
    RigidObject(rootNode, surfaceMeshFileName="mesh/smCube27.obj", name="Left", translation=[-20., 0., 0.])
    RigidObject(rootNode, surfaceMeshFileName="mesh/dragon.obj", translation=[0., 0., 0.])
    RigidObject(rootNode, surfaceMeshFileName="mesh/smCube27.obj", name="Right", translation=[20., 0., 0.])
