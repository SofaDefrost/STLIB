# -*- coding: utf-8 -*-
import Sofa

def ElasticMaterialObject(
                  attachedTo=None,
                  volumeMeshFileName=None,
                  name="ElasticMaterialObject",
                  rotation=[0.0, 0.0, 0.0],
                  translation=[0.0, 0.0, 0.0],
                  surfaceMeshFileName=None,
                  collisionMesh=None,
                  withConstrain=True,
                  surfaceColor=[1.0, 1.0, 1.0],
                  poissonRatio=0.3,
                  youngModulus=18000,
                  totalMass=1.0):
    """
    Object with an elastic deformation law.

    Args:
        volumeMeshFileName (str): Filepath to a volumetric mesh (VTK,VTU, GMESH)

        youngModulus (float):  The young modulus.

        poissonRatio (float):  The poisson parameter.

        totalMass (float):   The mass is distributed according to the geometry of the object.

        surfaceMeshFileName(str): Filepath to a surface mesh (STL, OBJ). If missing there is no visual properties to this object.

        collisionMesh (str): Filepath to a surface mesh (STL, OBJ). If missing there is no collision properties to this object.

        withConstrain (bool): Add by default a default constraint correction component (ei:LinearSolverConstraintCorrection)

        surfaceColor (vec3f):  The default color used for the rendering of the object.

        translation (vec3f):   Apply a 3D translation to the object.

        rotation (vec3f):   Apply a 3D rotation to the object in Euler angles.

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
                LinearSolverConstraintCorrection,
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
        Sofa.msg_error("Unable to create the elastic object because it is not attached to any node. Please fill the attachedTo parameter")
        return None

    if volumeMeshFileName == None:
        Sofa.msg_error(attachedTo, "Unable to create an elastic object because there is no volume mesh provided.")
        return None
    	
    elasticobject = attachedTo.createChild(name)

    if volumeMeshFileName.endswith(".msh"):
        elasticobject.createObject('MeshGmshLoader', name='MeshLoader', filename=volumeMeshFileName, rotation=rotation, translation=translation)
    else:
        elasticobject.createObject('MeshVTKLoader', name='MeshLoader', filename=volumeMeshFileName, rotation=rotation, translation=translation)
    
    elasticobject.createObject('EulerImplicit')
    solver = elasticobject.createObject('SparseLDLSolver', name="Solver")

    elasticobject.createObject('TetrahedronSetTopologyContainer', src='@MeshLoader', name='container')
    elasticobject.createObject('MechanicalObject', template='Vec3d')

    ## To be properly simulated and to interact with gravity or inertia forces, an elasticobject
    ## also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
    ## by adding a UniformMass component to the elasticobject node
    elasticobject.createObject('UniformMass', totalmass=totalMass)

    ## The next component to add is a FEM forcefield which defines how the elasticobject reacts
    ## to a loading (i.e. which deformations are created from forces applied onto it).
    ## Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
    ## This behavior is available via the TetrahedronFEMForceField component.
    elasticobject.createObject('TetrahedronFEMForceField', template='Vec3d',
                         	method='large',
                                poissonRatio=poissonRatio,  youngModulus=youngModulus)


    if withConstrain:
        elasticobject.createObject('LinearSolverConstraintCorrection', solverName=solver.name)
   
    #################################################################################
    ## Collision
    if collisionMesh:
        collisionNode = elasticobject.createChild('Collision')
        collisionNode.createObject('MeshSTLLoader', name='MeshLoader', filename=collisionMesh, rotation=rotation, translation=translation)
        collisionNode.createObject('TriangleSetTopologyContainer', src='@MeshLoader', name='container')
        collisionNode.createObject('MechanicalObject', name='MechanicalObject', template='Vec3d')
        collisionNode.createObject('Triangle')
        collisionNode.createObject('Line')
        collisionNode.createObject('Point')
        collisionNode.createObject('BarycentricMapping')


    #################################################################################
    ## Visualization
    if surfaceMeshFileName:
	    elasticobjectVisu = elasticobject.createChild('Visual')

	    ## Add to this empty node a rendering model made of triangles and loaded from an stl file.
	    elasticobjectVisu.createObject('OglModel', filename=surfaceMeshFileName,
	                            template='ExtVec3f', color=surfaceColor, rotation=rotation, translation=translation)

	    ## Add a BarycentricMapping to deform the rendering model to follow the ones of the
	    ## mechanical model.
	    elasticobjectVisu.createObject('BarycentricMapping')
       
    return elasticobject
    
def createScene(rootNode):
    from stlib.scene import MainHeader

    MainHeader(rootNode, gravity=" 0 0 0")
    ElasticMaterialObject(rootNode, "mesh/liver.msh", "NoVisual" , translation=[3.0, 0.0, 0.0])
    ElasticMaterialObject(rootNode, "mesh/liver.msh", "WithVisual", translation=[-3, 0, 0], surfaceMeshFileName="mesh/liver.obj", surfaceColor=[1.0, 0.0, 0.0])

