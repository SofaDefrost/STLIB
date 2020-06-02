# -*- coding: utf-8 -*-
import Sofa
#from stlib.scene import Node
#from stlib.visuals import VisualModel


class ElasticMaterialObject(Sofa.Prefab):
    """Creates an object composed of an elastic material.
       WorkFlow to make it work:
           
           Sofa.Prefab.__init__ 
                prefab::init
                prefab::reinit
                prefab::doReInit
           
           --> Instanciate as a prefab but due to pybind problem
               we loose all the python parameters
           
           self.doReInit
               prefab::doReInit
               
           --> We re-do a doReInit to finally instanciate the python
               parameters and build the graph 
    """

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)
        self.doReInit( *args, **kwargs)

    def doReInit(self, *args, **kwargs):

        # Instanciate Kwargs to given value
        # enter during self.doReInit
        if (kwargs.__len__() != 0):

            self.volumeMeshFileName=kwargs.get("volumeMeshFileName", None)
            self.rotation=kwargs.get("rotation", [0.0, 0.0, 0.0])
            self.translation=kwargs.get("translation", [0.0, 0.0, 0.0])
            self.scale=kwargs.get("scale", [1.0, 1.0, 1.0])
            self.surfaceMeshFileName=kwargs.get("surfaceMeshFileName", None)
            self.collisionMesh=kwargs.get("collisionMesh", None)
            self.withConstrain=kwargs.get("withConstrain", True)
            self.surfaceColor=kwargs.get("surfaceColor", [1.0, 1.0, 1.0])
            self.poissonRatio=kwargs.get("poissonRatio", 0.3)
            self.youngModulus=kwargs.get("youngModulus", 18000)
            self.totalMass=kwargs.get("totalMass", 1.0)
            self.solver=kwargs.get("solver", None)
        
        # Take a random python attribute and test if it exist
        # If it doesn't exist it mean that we are in the doReInit of Sofa.Prefab.__init__ 
        if ("rotation" not in self.__dict__):
            print("dic empty")
            return
        
        # Building graph ####################
        if not self.getRoot()["SofaSparseSolver"]:
            if not self.getRoot()["Config.SofaSparseSolver"]:
                    Sofa.msg_info("Missing RequiredPlugin SofaSparseSolver in the scene, add it from Prefab ElasticMaterialObject.")
                    self.getRoot().addObject("RequiredPlugin", name="SofaSparseSolver")

        if self.volumeMeshFileName is None:
            Sofa.msg_error(self, "Unable to create an elastic object because there is no volume mesh provided.")
            return None

        if self.volumeMeshFileName.endswith(".msh"):
            self.loader = self.addObject('MeshGmshLoader', name='loader', filename=self.volumeMeshFileName, rotation=self.rotation, translation=self.translation, scale3d=self.scale)
        elif self.volumeMeshFileName.endswith(".gidmsh"):
            self.loader = self.addObject('GIDMeshLoader', name='loader', filename=self.volumeMeshFileName, rotation=self.rotation, translation=self.translation, scale3d=self.scale)
        else:
            self.loader = self.addObject('MeshVTKLoader', name='loader', filename=self.volumeMeshFileName, rotation=self.rotation, translation=self.translation, scale3d=self.scale)

        if self.solver is None:
            self.integration = self.addObject('EulerImplicitSolver', name='integration')
            self.solver = self.addObject('SparseLDLSolver', name="solver")

        self.container = self.addObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
        self.dofs = self.addObject('MechanicalObject', template='Vec3d', name='dofs')

        # To be properly simulated and to interact with gravity or inertia forces, an elasticobject
        # also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
        # by adding a UniformMass component to the elasticobject node
        self.mass = self.addObject('UniformMass', totalMass=self.totalMass, name='mass')

        # The next component to add is a FEM forcefield which defines how the elasticobject reacts
        # to a loading (i.e. which deformations are created from forces applied onto it).
        # Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
        # This behavior is available via the TetrahedronFEMForceField component.
        self.forcefield = self.addObject('TetrahedronFEMForceField', template='Vec3d',
                                                 method='large', name='forcefield',
                                                 poissonRatio=self.poissonRatio,  youngModulus=self.youngModulus)

def createScene(root):

    root.addChild(ElasticMaterialObject("ElasticMaterialObject",name="ElasticMaterialObject",
                                        volumeMeshFileName="mesh/liver.msh",
                                        translation=[3.0, 0.0, 0.0]))
    root.ElasticMaterialObject.reinit()
#    from stlib.scene import MainHeader
#
#    MainHeader(rootNode, gravity=" 0 0 0")
#    rootNode.addObject('MeshSTLLoader', name='test')
#    ElasticMaterialObject(rootNode, "mesh/liver.msh", "NoVisual", translation=[3.0, 0.0, 0.0])
#    ElasticMaterialObject(rootNode, "mesh/liver.msh", "WithVisual", translation=[-3, 0, 0], surfaceMeshFileName="mesh/liver.obj", surfaceColor=[1.0, 0.0, 0.0])


#        if withConstrain:
#            self.node.addObject('LinearSolverConstraintCorrection', solverName=self.solver.name)
#
#        if collisionMesh:
#            self.addCollisionModel(collisionMesh, rotation, translation, scale)
#
#        if surfaceMeshFileName:
#                self.addVisualModel(surfaceMeshFileName, surfaceColor, rotation, translation, scale)
#
#    def addCollisionModel(self, collisionMesh, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], scale=[1., 1., 1.]):
#        self.collisionmodel = self.node.addChild('CollisionModel')
#        self.collisionmodel.addObject('MeshSTLLoader', name='loader', filename=collisionMesh, rotation=rotation, translation=translation, scale=scale)
#        self.collisionmodel.addObject('TriangleSetTopologyContainer', src='@loader', name='container')
#        self.collisionmodel.addObject('MechanicalObject', template='Vec3d', name='dofs')
#        self.collisionmodel.addObject('Triangle')
#        self.collisionmodel.addObject('Line')
#        self.collisionmodel.addObject('Point')
#        self.collisionmodel.addObject('BarycentricMapping')
#
#    def addVisualModel(self, filename, color, rotation, translation, scale=[1., 1., 1.]):
#        print("================================================> "+str(color))
#        self.visualmodel = VisualModel(parent=self.node, surfaceMeshFileName=filename, color=color, rotation=rotation, translation=translation)
#
#        # Add a BarycentricMapping to deform the rendering model to follow the ones of the
#        # mechanical model.
#        self.visualmodel.mapping = self.visualmodel.node.addObject('BarycentricMapping', name='mapping')