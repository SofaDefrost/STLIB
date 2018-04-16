# -*- coding: utf-8 -*-
import Sofa
from splib.objectmodel import SofaPrefab, SofaObject
from stlib.scene import Node

@SofaPrefab
class ElasticMaterialObject(SofaObject):
    def __init__(self,
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
                 totalMass=1.0, solver=None):

        self.node = Node(attachedTo, name)
        ElasticMaterialObject.createPrefab(self,
                                           volumeMeshFileName, name, rotation, translation, surfaceMeshFileName,
                                           collisionMesh, withConstrain, surfaceColor, poissonRatio, youngModulus, totalMass, solver)

    @staticmethod
    def createPrefab(self, volumeMeshFileName=None,
                 name="ElasticMaterialObject",
                 rotation=[0.0, 0.0, 0.0],
                 translation=[0.0, 0.0, 0.0],
                 surfaceMeshFileName=None,
                 collisionMesh=None,
                 withConstrain=True,
                 surfaceColor=[1.0, 1.0, 1.0],
                 poissonRatio=0.3,
                 youngModulus=18000,
                 totalMass=1.0, solver=None):
        if self.node == None:
            Sofa.msg_error("Unable to create the elastic object because it is not attached to any node. Please fill the attachedTo parameter")
            return None

        if volumeMeshFileName == None:
            Sofa.msg_error(self.node, "Unable to create an elastic object because there is no volume mesh provided.")
            return None

        if volumeMeshFileName.endswith(".msh"):
            self.loader = self.node.createObject('MeshGmshLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation)
        elif volumeMeshFileName.endswith(".gidmsh"):
            self.loader = self.node.createObject('GIDMeshLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation)
        else:
            self.loader = self.node.createObject('MeshVTKLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation)

        if solver == None:
            self.integration = self.node.createObject('EulerImplicit', name='integration')
            self.solver = self.node.createObject('SparseLDLSolver', name="solver")

        self.container = self.node.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
        self.dofs = self.node.createObject('MechanicalObject', template='Vec3d', name='dofs')

        ## To be properly simulated and to interact with gravity or inertia forces, an elasticobject
        ## also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
        ## by adding a UniformMass component to the elasticobject node
        self.mass = self.node.createObject('UniformMass', totalmass=totalMass, name='mass')

        ## The next component to add is a FEM forcefield which defines how the elasticobject reacts
        ## to a loading (i.e. which deformations are created from forces applied onto it).
        ## Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
        ## This behavior is available via the TetrahedronFEMForceField component.
        self.forcefield = self.node.createObject('TetrahedronFEMForceField', template='Vec3d',
                         	        method='large', name='forcefield',
                                    poissonRatio=poissonRatio,  youngModulus=youngModulus)

        if withConstrain:
            self.node.createObject('LinearSolverConstraintCorrection', solverName=self.solver.name)

        if collisionMesh:
            self.addCollisionModel(collisionMesh, rotation, translation)

        if surfaceMeshFileName:
	        self.addVisualModel(surfaceMeshFileName, surfaceColor, rotation, translation)

    def addCollisionModel(self, collisionMesh):
        self.collisionmodel = self.node.createChild('CollisionModel')
        self.collisionmodel.createObject('MeshSTLLoader', name='loader', filename=collisionMesh, rotation=rotation, translation=translation)
        self.collisionmodel.createObject('TriangleSetTopologyContainer', src='@loader', name='container')
        self.collisionmodel.createObject('MechanicalObject', template='Vec3d', name='dofs')
        self.collisionmodel.createObject('Triangle')
        self.collisionmodel.createObject('Line')
        self.collisionmodel.createObject('Point')
        self.collisionmodel.createObject('BarycentricMapping')

    def addVisualModel(self, filename, color, rotation, translation):
        self.visualmodel = SofaObject(self.node, "VisualModel")

	    ## Add to this empty node a rendering model made of triangles and loaded from an stl file.
        self.visualmodel.model = self.visualmodel.node.createObject('OglModel', filename=filename,
	                                                           template='ExtVec3f', color=color, rotation=rotation, translation=translation)

	    ## Add a BarycentricMapping to deform the rendering model to follow the ones of the
	    ## mechanical model.
        self.visualmodel.mapping = self.visualmodel.node.createObject('BarycentricMapping', name='mapping')


def createScene(rootNode):
    from stlib.scene import MainHeader

    MainHeader(rootNode, gravity=" 0 0 0")
    ElasticMaterialObject(rootNode, "mesh/liver.msh", "NoVisual" , translation=[3.0, 0.0, 0.0])
    ElasticMaterialObject(rootNode, "mesh/liver.msh", "WithVisual", translation=[-3, 0, 0], surfaceMeshFileName="mesh/liver.obj", surfaceColor=[1.0, 0.0, 0.0])
