# -*- coding: utf-8 -*-
import Sofa


def loaderFor(name):
    if name.endswith(".obj"):
        return "MeshObjLoader"
    elif name.endswith(".stl"):
        return "MeshSTLLoader"
    elif name.endswith(".vtk"):
        return "MeshVTKLoader"


def CollisionMesh(attachedTo=None,
                  surfaceMeshFileName=None,
                  name="collision",
                  rotation=[0.0, 0.0, 0.0],
                  translation=[0.0, 0.0, 0.0],
                  collisionGroup=None,
                  mappingType='BarycentricMapping'):
    '''

    '''

    if attachedTo is None:
        Sofa.msg_error("Cannot create a CollisionMesh that is not attached to node.")
        return None

    collisionmodel = attachedTo.addChild(name)

    if surfaceMeshFileName is None:
        Sofa.msg_error(collisionmodel, "Unable to create a CollisionMesh without a surface mesh")
        return None

    collisionmodel.addObject(loaderFor(surfaceMeshFileName), name="loader", filename=surfaceMeshFileName,
                                rotation=rotation, translation=translation)
    collisionmodel.addObject('MeshTopology', src="@loader")
    collisionmodel.addObject('MechanicalObject')
    if collisionGroup:
        collisionmodel.addObject('TPointModel', group=collisionGroup)
        collisionmodel.addObject('TLineModel', group=collisionGroup)
        collisionmodel.addObject('TTriangleModel', group=collisionGroup)
    else:
        collisionmodel.addObject('TPointModel')
        collisionmodel.addObject('TLineModel')
        collisionmodel.addObject('TTriangleModel')

    if mappingType is not None:
        collisionmodel.addObject(mappingType)

    return collisionmodel


def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.physics.deformable import ElasticMaterialObject
    from stlib.physics.constraints import FixedBox

    MainHeader(rootNode)
    target = ElasticMaterialObject(volumeMeshFileName="mesh/liver.msh",
                                   totalMass=0.5,
                                   attachedTo=rootNode)

    FixedBox(atPositions=[-4, 0, 0, 5, 5, 4], applyTo=target,
             doVisualization=True)

    CollisionMesh(surfaceMeshFileName="mesh/liver.obj", attachedTo=target)
