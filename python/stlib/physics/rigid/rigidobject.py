# -*- coding: utf-8 -*-

def RigidObject(node, name="rigidobject", shapeFromFile=None,
                translation=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0], scale=1.0,
                totalmass=1.0,
                color=[1.0, 1.0, 0.0]):
    """Creates a rigid body from a surface mesh.
       The mass is distributed according to the geometry of the object.
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
