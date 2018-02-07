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
                  fromSurfaceMesh=None,
                  withName="collision",
                  withRotation=[0.0,0.0,0.0],
                  withTranslation=[0.0,0.0,0.0],
                  withACollisionGroup=None):

    if attachedTo == None:
        Sofa.msg_error("Cannot create a CollisionMesh that is not attached to node.")
        return None

    collisionmodel = attachedTo.createChild(withName)

    if fromSurfaceMesh == None:
        Sofa.msg_error(collisionmodel, "Unable to create a CollisionMesh without a surface mesh")
        return None

    collisionmodel.createObject(loaderFor(fromSurfaceMesh), name="loader", filename=fromSurfaceMesh,
                                rotation=withRotation, translation=withTranslation)
    collisionmodel.createObject('Mesh', src="@loader")
    collisionmodel.createObject('MechanicalObject')
    if withACollisionGroup:
        collisionmodel.createObject('Point', group=withACollisionGroup)
        collisionmodel.createObject('Line', group=withACollisionGroup)
        collisionmodel.createObject('Triangle', group=withACollisionGroup)
    else:    
        collisionmodel.createObject('Point')
        collisionmodel.createObject('Line')
        collisionmodel.createObject('Triangle')
    
    collisionmodel.createObject('BarycentricMapping', mapForces=False, mapMasses=False)

    return collisionmodel
    

def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.physics.deformable import ElasticMaterialObject
    from stlib.physics.constraints import FixedBox

    MainHeader(rootNode)
    target = ElasticMaterialObject(fromVolumeMesh="mesh/liver.msh",
                                   withTotalMass=0.5,
                                   attachedTo=rootNode)

    FixedBox(atPositions=[-4, 0, 0, 5, 5, 4], applyTo=target,
             withVisualization=True)

    CollisionMesh(fromSurfaceMesh="mesh/liver.obj", attachedTo=target)
