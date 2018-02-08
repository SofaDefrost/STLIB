# -*- coding: utf-8 -*-
import Sofa

def ElasticMaterialObject(
                  attachedTo=None,
                  fromVolumeMesh=None,
                  withName="elasticelasticobject",
                  withRotation=[0.0, 0.0, 0.0],
                  withTranslation=[0.0, 0.0, 0.0],
                  withSurfaceMesh=None,
                  withCollisionMesh=None,
                  withSurfaceColor=[1.0, 1.0, 1.0],
                  withPoissonRatio=0.3,
                  withYoungModulus=18000,
                  withTotalMass=1.0):
    """
    Object with an elastic deformation law.

    Args:
        fromVolumeMesh (str): Filepath to a volumetric mesh (VTK,VTU, GMESH)

        withYoungModulus (float):  The young modulus.

        withPoissonRatio (float):  The poisson parameter.

        withTotalMass (float):   The mass is distributed according to the geometry of the object.

        withSurfaceMesh (str): Filepath to a surface mesh (STL, OBJ). If missing there is no visual properties to this object.

        withCollisionMesh (str): Filepath to a surface mesh (STL, OBJ). If missing there is no collision properties to this object.

        withSurfaceColor (vec3f):  The default color used for the rendering of the object.

        withTranslation (vec3f):   Apply a 3D translation to the object.

        withRotation (vec3f):   Apply a 3D rotation to the object in Euler angles.

        attachedTo (Sofa.Node): Where the node is created;

    Structure:
        .. sourcecode:: qml

            Node : {
                name : "elasticobject"
                MeshGmsgLoader or MeshVTKLoader,
                MechanicalObject,
                TetrahedronSetTopologyContainer,
                UniformMass,
                TetrahedronFEMForceField,
                EulerImplicit,
                SparseLDLSolver
                LinearSolverConstraintCorrection
                Node : {
                   name : "Collision"
                }
                Node : {
                   name : "Visual"
                   OglModel,
                   BarycentricMapping
                }
            }
    """

    if attachedTo == None:
        Sofa.msg_error("Unable to create an elastic object because there is no volume mesh provided.")
        return None

    if fromVolumeMesh == None:
        Sofa.msg_error(attachedTo, "Unable to create an elastic object because there is no volume mesh provided.")
        return None
    	
    elasticobject = attachedTo.createChild(withName)

    if fromVolumeMesh.endswith(".msh"):
        elasticobject.createObject('MeshGmshLoader', name='MeshLoader', filename=fromVolumeMesh, rotation=withRotation, translation=withTranslation)
    else:
        elasticobject.createObject('MeshVTKLoader', name='MeshLoader', filename=fromVolumeMesh, rotation=withRotation, translation=withTranslation)
    
    elasticobject.createObject('EulerImplicit')
    solver = elasticobject.createObject('SparseLDLSolver', name="Solver")

    elasticobject.createObject('TetrahedronSetTopologyContainer', src='@MeshLoader', name='container')
    elasticobject.createObject('MechanicalObject', template='Vec3d')

    ## To be properly simulated and to interact with gravity or inertia forces, an elasticobject
    ## also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
    ## by adding a UniformMass component to the elasticobject node
    elasticobject.createObject('UniformMass', totalmass=withTotalMass)

    ## The next component to add is a FEM forcefield which defines how the elasticobject reacts
    ## to a loading (i.e. which deformations are created from forces applied onto it).
    ## Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
    ## This behavior is available via the TetrahedronFEMForceField component.
    elasticobject.createObject('TetrahedronFEMForceField', template='Vec3d',
                         	method='large',
                                poissonRatio=withPoissonRatio,  youngModulus=withYoungModulus)


    elasticobject.createObject('LinearSolverConstraintCorrection', solverName=solver.name)
   
    #################################################################################
    ## Collision
    if withCollisionMesh:
        collisionNode = elasticobject.createChild('Collision')
        collisionNode.createObject('MeshSTLLoader', name='MeshLoader', filename=withCollisionMesh, rotation=withRotation, translation=withTranslation)
        collisionNode.createObject('TriangleSetTopologyContainer', src='@MeshLoader', name='container')
        collisionNode.createObject('MechanicalObject', name='MechanicalObject', template='Vec3d')
        collisionNode.createObject('Triangle')
        collisionNode.createObject('Line')
        collisionNode.createObject('Point')
        collisionNode.createObject('BarycentricMapping')


    #################################################################################
    ## Visualization
    if withSurfaceMesh:
	    elasticobjectVisu = elasticobject.createChild('Visual')

	    ## Add to this empty node a rendering model made of triangles and loaded from an stl file.
	    elasticobjectVisu.createObject('OglModel', filename=withSurfaceMesh,
	                            template='ExtVec3f', color=withSurfaceColor, rotation=withRotation, translation=withTranslation)

	    ## Add a BarycentricMapping to deform the rendering model to follow the ones of the
	    ## mechanical model.
	    elasticobjectVisu.createObject('BarycentricMapping')
       
    return elasticobject
    
def createScene(rootNode):
    from stlib.scene import MainHeader

    MainHeader(rootNode)
    ElasticMaterialObject(rootNode, "ShouldFail")
    ElasticMaterialObject(rootNode, "NoVisual", fromVolumeMesh="mesh/liver.msh", translation=[3.0, 0.0, 0.0])
    ElasticMaterialObject(rootNode, "WithVisual", withSurfaceMesh="mesh/liver.obj", surfacecolor=[1.0, 0.0, 0.0], fromVolumeMesh="mesh/liver.msh", translation=[-3, 0, 0])

