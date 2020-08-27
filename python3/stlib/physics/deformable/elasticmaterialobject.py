# -*- coding: utf-8 -*-
import Sofa
from splib import SofaPrefab
from splib.objectmodel import SofaPrefab, SofaObject
from stlib.scene import Node
from stlib.visuals import VisualModel

class ElasticMaterialObject(Sofa.Prefab):
    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

    def createParams(self, *args, **kwargs):
        self.addPrefabParameter(name="volumeMeshFileName", type="string", help="The volume topology of this elastic material object", default=kwargs.get("volumeMeshFileName", ''))
        self.addPrefabParameter(name="surfaceMeshFileName", type="string", help="The surface topology of this elastic material object", default=kwargs.get("surfaceMeshFileName", ''))
        self.addPrefabParameter(name="rotation", type="Vec3d", help="Initial Rotation of this elastic material object", default=kwargs.get("rotation", [0,0,0]))
        self.addPrefabParameter(name="translation", type="Vec3d", help="Initial Translation of this elastic material object", default=kwargs.get("translation", [0,0,0]))
        self.addPrefabParameter(name="scale", type="Vec3d", help="Initial Scaling of this elastic material object", default=kwargs.get("scale", [1.0,1.0,1.0]))

        self.addPrefabParameter(name="collisionMesh", type="Link", help="The mesh file to use for collision", default=kwargs.get("collisionMesh", ''))
        self.addPrefabParameter(name="withConstraints", type="bool", help="Enables the use of constraints on this prefab (provided that you have a compatible solver and animation loop in your scene)", default=kwargs.get("withConstraints", True))
        
        self.addPrefabParameter(name="surfaceColor", type="Vec3d", help="The material color for the mesh visualization", default=kwargs.get("surfaceColor", [1.0, 1.0, 1.0]))
        
        self.addPrefabParameter(name="poissonRatio", type="double", help="Poisson ratio for the object", default=kwargs.get("poissonRatio", 0.3))
        self.addPrefabParameter(name="youngModulus", type="double", help="Young's modulus of this object", default=kwargs.get("youngModulus", 18000))
        self.addPrefabParameter(name="totalMass", type="double", help="the mass of the object, distributed evenly on the volume's nodes", default=kwargs.get("totalMass", 1.0))
        self.addPrefabParameter(name="solverName", type="Link", help="the name of the solver", default=kwargs.get("solveName", "no_solver"))


    def doReInit(self):
        if "SofaSparseSolver" not in SofaRuntime.PluginManager.loadedPlugins:
            Sofa.msg_info("Missing plugin SofaSparseSolver, adding it to the root node.")
            self.getRoot().createObject("RequiredPlugin", pluginName="SofaSparseSolver")

        if volumeMeshFileName.value == '':
            Sofa.msg_error(self, "Unable to create an elastic object: no volume mesh was provided.")
            return

        if volumeMeshFileName.endswith(".msh"):
            self.createObject('MeshGmshLoader', name='loader', filename=volumeMeshFileName.value, rotation=rotation.value, translation=translation.value, scale3d=scale.value)
        elif volumeMeshFileName.endswith(".gidmsh"):
            self.createObject('GIDMeshLoader', name='loader', filename=volumeMeshFileName.value, rotation=rotation.value, translation=translation.value, scale3d=scale.value)
        else:
            self.createObject('MeshVTKLoader', name='loader', filename=volumeMeshFileName.value, rotation=rotation.value, translation=translation.value, scale3d=scale.value)

        if solver == "no_solver":
            Sofa.msg_info(self, "No solver was passed to this prefab: embedding a solver & integration scheme")
            self.createObject('EulerImplicitSolver', name='integration')
            self.solverName.value = "solver"
            self.createObject('SparseLDLSolver', name=self.solverName.value)

        self.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
        self.createObject('MechanicalObject', template='Vec3d', name='dofs')

        # To be properly simulated and to interact with gravity or inertia forces, an elasticobject
        # also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
        # by adding a UniformMass component to the elasticobject node
        self.createObject('UniformMass', totalMass=totalMass.value, name='mass')

        # The next component to add is a FEM forcefield which defines how the elasticobject reacts
        # to a loading (i.e. which deformations are created from forces applied onto it).
        # Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
        # This behavior is available via the TetrahedronFEMForceField component.
        self.createObject('TetrahedronFEMForceField', template='Vec3d',
                          method='large', name='forcefield',
                          poissonRatio=poissonRatio.value,  youngModulus=youngModulus.value)
        
        if withConstrain:
            self.createObject('LinearSolverConstraintCorrection', solverName=self.solver.name)

        if collisionMesh:
            self.addCollisionModel(collisionMesh, rotation, translation, scale)

        if surfaceMeshFileName:
            self.addVisualModel(surfaceMeshFileName, surfaceColor, rotation, translation, scale)

    def addCollisionModel(self, collisionMesh, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], scale=[1., 1., 1.]):
        self.createChild('CollisionModel')
        self.Collisionmodel.createObject('MeshSTLLoader', name='loader', filename=collisionMesh.value, rotation=rotation.value, translation=translation.value, scale3d=scale.value)
        self.Collisionmodel.createObject('TriangleSetTopologyContainer', src='@loader', name='container')
        self.Collisionmodel.createObject('MechanicalObject', template='Vec3d', name='dofs')
        self.Collisionmodel.createObject('Triangle')
        self.Collisionmodel.createObject('Line')
        self.Collisionmodel.createObject('Point')
        self.Collisionmodel.createObject('BarycentricMapping')

    def addVisualModel(self, filename, color, rotation, translation, scale=[1., 1., 1.]):
        VisualModel(self, name="visualmodel", surfaceMeshFileName=filename, color=color, rotation=rotation, translation=translation)

        # Add a BarycentricMapping to deform the rendering model to follow the ones of the
        # mechanical model.
        self.visualmodel.createObject('BarycentricMapping', name='mapping')

@SofaPrefab
class ElasticMaterialObject(SofaObject):
    """Creates an object composed of an elastic material."""

    def __init__(self,
                 attachedTo=None,
                 volumeMeshFileName=None,
                 name="ElasticMaterialObject",
                 rotation=[0.0, 0.0, 0.0],
                 translation=[0.0, 0.0, 0.0],
                 scale=[1.0, 1.0, 1.0],
                 surfaceMeshFileName=None,
                 collisionMesh=None,
                 withConstrain=True,
                 surfaceColor=[1.0, 1.0, 1.0],
                 poissonRatio=0.3,
                 youngModulus=18000,
                 totalMass=1.0, solver=None):

        self.node = attachedTo.createChild(name)
        self.createPrefab(volumeMeshFileName, name, rotation, translation, scale, surfaceMeshFileName,
                          collisionMesh, withConstrain, surfaceColor, poissonRatio, youngModulus, totalMass, solver)

    def createPrefab(self,
                     volumeMeshFileName=None,
                     name="ElasticMaterialObject",
                     rotation=[0.0, 0.0, 0.0],
                     translation=[0.0, 0.0, 0.0],
                     scale=[1.0, 1.0, 1.0],
                     surfaceMeshFileName=None,
                     collisionMesh=None,
                     withConstrain=True,
                     surfaceColor=[1.0, 1.0, 1.0],
                     poissonRatio=0.3,
                     youngModulus=18000,
                     totalMass=1.0, solver=None):

        if not self.getRoot().getObject("SofaSparseSolver", warning=False):
            if not self.getRoot().getObject("/Config/SofaSparseSolver", warning=False):
                    Sofa.msg_info("Missing RequiredPlugin SofaSparseSolver in the scene, add it from Prefab ElasticMaterialObject.")
                    self.getRoot().createObject("RequiredPlugin", name="SofaSparseSolver")

        if self.node is None:
            Sofa.msg_error("Unable to create the elastic object because it is not attached to any node. Please fill the attachedTo parameter")
            return None

        if volumeMeshFileName is None:
            Sofa.msg_error(self.node, "Unable to create an elastic object because there is no volume mesh provided.")
            return None

        if volumeMeshFileName.endswith(".msh"):
            self.loader = self.node.createObject('MeshGmshLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation, scale3d=scale)
        elif volumeMeshFileName.endswith(".gidmsh"):
            self.loader = self.node.createObject('GIDMeshLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation, scale3d=scale)
        else:
            self.loader = self.node.createObject('MeshVTKLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation, scale3d=scale)

        if solver is None:
            self.integration = self.node.createObject('EulerImplicitSolver', name='integration')
            self.solver = self.node.createObject('SparseLDLSolver', name="solver")

        self.container = self.node.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
        self.dofs = self.node.createObject('MechanicalObject', template='Vec3d', name='dofs')

        # To be properly simulated and to interact with gravity or inertia forces, an elasticobject
        # also needs a mass. You can add a given mass with a uniform distribution for an elasticobject
        # by adding a UniformMass component to the elasticobject node
        self.mass = self.node.createObject('UniformMass', totalMass=totalMass, name='mass')

        # The next component to add is a FEM forcefield which defines how the elasticobject reacts
        # to a loading (i.e. which deformations are created from forces applied onto it).
        # Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
        # This behavior is available via the TetrahedronFEMForceField component.
        self.forcefield = self.node.createObject('TetrahedronFEMForceField', template='Vec3d',
                                                 method='large', name='forcefield',
                                                 poissonRatio=poissonRatio,  youngModulus=youngModulus)

        if withConstrain:
            self.node.createObject('LinearSolverConstraintCorrection', solverName=self.solver.name)

        if collisionMesh:
            self.addCollisionModel(collisionMesh, rotation, translation, scale)

        if surfaceMeshFileName:
                self.addVisualModel(surfaceMeshFileName, surfaceColor, rotation, translation, scale)

    def addCollisionModel(self, collisionMesh, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], scale=[1., 1., 1.]):
        self.collisionmodel = self.node.createChild('CollisionModel')
        self.collisionmodel.createObject('MeshSTLLoader', name='loader', filename=collisionMesh, rotation=rotation, translation=translation, scale3d=scale)
        self.collisionmodel.createObject('TriangleSetTopologyContainer', src='@loader', name='container')
        self.collisionmodel.createObject('MechanicalObject', template='Vec3d', name='dofs')
        self.collisionmodel.createObject('Triangle')
        self.collisionmodel.createObject('Line')
        self.collisionmodel.createObject('Point')
        self.collisionmodel.createObject('BarycentricMapping')

    def addVisualModel(self, filename, color, rotation, translation, scale=[1., 1., 1.]):
        self.visualmodel = VisualModel(parent=self.node, surfaceMeshFileName=filename, color=color, rotation=rotation, translation=translation)

        # Add a BarycentricMapping to deform the rendering model to follow the ones of the
        # mechanical model.
        self.visualmodel.mapping = self.visualmodel.node.createObject('BarycentricMapping', name='mapping')


# def createScene(rootNode):
#     from stlib.scene import MainHeader

#     MainHeader(rootNode, gravity=" 0 0 0")
#     ElasticMaterialObject(rootNode, "mesh/liver.msh", "NoVisual", translation=[3.0, 0.0, 0.0])
#     ElasticMaterialObject(rootNode, "mesh/liver.msh", "WithVisual", translation=[-3, 0, 0], surfaceMeshFileName="mesh/liver.obj", surfaceColor=[1.0, 0.0, 0.0])
