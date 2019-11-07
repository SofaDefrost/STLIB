# -*- coding: utf-8 -*-
import Sofa
from splib.objectmodel import SofaPrefab, SofaObject
from stlib.scene import Node
from stlib.visuals import VisualModel
from stlib.solver import DefaultSolver

from math import sqrt

# ENUM ANISOTROPY TYPES
ISOTROPIC=1
TRANSVERSE_ISOTROPIC=2
ORTHOTROPIC=3
CUBIC=4

@SofaPrefab
class HighOrderShape(SofaObject):
    """Creates an object composed of an elastic material."""

    def __init__(self,
                attachedTo=None,
                poissonRatio=0.45,youngModulus=200,totalMass=1.0,name="highOrderCube",translation=[0,0,0],rotation=[0,0,0],scale=[1.0, 1.0, 1.0],
                volumeMeshFileName=None,
                numericalIntegrationMethod='Tetrahedron Gauss',
                forceAffineAssemblyForAffineElements= False, # if true affine tetrahedra are always assembled with the closed form formula, Otherwise use the method defined in integrationMethod
                integrationMethod='analytical', # analytical # numerical # standard !! if degree ==  1 --> force to AFFINE_ELEMENT_INTEGRATION
                method="qr", # linear # qr # polar # polar2 # none
                integrationOrder=1, # The order of integration for numerical integration
                orderDegree=1,      # Degree of High Order Tetrahedra
                oneRotationPerIntegrationPoint= False,
                withAnysotropy=True,
                elasticitySymmetry='transverseIsotropic', # \"isotropic\"  or \"transverseIsotropic\" or \"orthotropic\" or \"cubic\
                youngModulusLongitudinal = None,
                anisotropyParameters=[1000,0.45,300], # [youngModulusLongitudinal, poissonRatioTransverseLongitudinal, shearModulusTransverse]
                anisotropyDirections = [[1,1,0]], # vector<Coord>
                surfaceMeshFileName=None,
                collisionMesh=None,
                withConstrain=True,
                surfaceColor=[1.0, 1.0, 1.0],
                solver=None,
                color=[1,0,0]):

        self.node = Node(attachedTo, name)

        HighOrderShape.createPrefab(self,poissonRatio,youngModulus,totalMass,name,translation,rotation,scale,
                                    volumeMeshFileName,numericalIntegrationMethod,forceAffineAssemblyForAffineElements,
                                    integrationMethod,method,integrationOrder,orderDegree,
                                    oneRotationPerIntegrationPoint,withAnysotropy,elasticitySymmetry,
                                    youngModulusLongitudinal,anisotropyParameters,anisotropyDirections,
                                    surfaceMeshFileName,collisionMesh,withConstrain,surfaceColor,solver,color)

    @staticmethod
    def createPrefab(self,poissonRatio,youngModulus,totalMass,name="highOrderCube",translation=[0,0,0],rotation=[0,0,0],scale=[1.0, 1.0, 1.0],
        volumeMeshFileName=None,
        numericalIntegrationMethod='Tetrahedron Gauss',
        forceAffineAssemblyForAffineElements= False, # if true affine tetrahedra are always assembled with the closed form formula, Otherwise use the method defined in integrationMethod
        integrationMethod='analytical', # analytical # numerical # standard !! if degree ==  1 --> force to AFFINE_ELEMENT_INTEGRATION
        method="qr", # linear # qr # polar # polar2 # none
        integrationOrder=1, # The order of integration for numerical integration
        orderDegree=1,      # Degree of High Order Tetrahedra
        oneRotationPerIntegrationPoint= False,
        withAnysotropy=True,
        elasticitySymmetry='transverseIsotropic', # \"isotropic\"  or \"transverseIsotropic\" or \"orthotropic\" or \"cubic\
        youngModulusLongitudinal = None,
        anisotropyParameters=[1000,0.45,300], # [youngModulusLongitudinal, poissonRatioTransverseLongitudinal, shearModulusTransverse]
        anisotropyDirections = [[1,1,0]], # vector<Coord>
        surfaceMeshFileName=None,
        collisionMesh=None,
        withConstrain=True,
        surfaceColor=[1.0, 1.0, 1.0],
        solver=None,
        color=[1,0,0]):

        # print("highOrderCube : "+name)
        # print("    - youngModulus : " + str(youngModulus))
        # print("    - youngModulusLongitudinal : " + str(youngModulusLongitudinal))
        # print("    - poissonRatio : " + str(poissonRatio))
        
        if youngModulusLongitudinal != None: 
            # http://solidmechanics.org/text/Chapter3_2/Chapter3_2.htm
            # 3.2.14 Stress-strain relations for linear elastic Transversely Isotropic Material
            poissonRatioTransverseLongitudinal = (poissonRatio*youngModulusLongitudinal)/youngModulus
            shearModulusTransverse = youngModulusLongitudinal/(2*(1+poissonRatioTransverseLongitudinal))

            anisotropyParameters = [youngModulusLongitudinal,poissonRatioTransverseLongitudinal,shearModulusTransverse]

            print("    - poissonRatioTransverseLongitudinal : " + str(poissonRatioTransverseLongitudinal))
            print("    - shearModulusTransverse : " + str(shearModulusTransverse))


        # MESH TOPO
        if volumeMeshFileName.endswith(".msh"):
            loader = self.node.createObject('MeshGmshLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation, scale3d=scale)
        elif volumeMeshFileName.endswith(".gidmsh"):
            loader = self.node.createObject('GIDMeshLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation, scale3d=scale)
        else:
            loader = self.node.createObject('MeshVTKLoader', name='loader', filename=volumeMeshFileName, rotation=rotation, translation=translation, scale3d=scale)


        # The next component to add is a FEM forcefield which defines how the elasticobject reacts
        # to a loading (i.e. which deformations are created from forces applied onto it).
        # Here, because the elasticobject is made of silicone, its mechanical behavior is assumed elastic.
        # This behavior is available via the TetrahedronFEMForceField component.
        tetstc = self.node.createObject('TetrahedronSetTopologyContainer',name="Container1",tetrahedra="@loader.tetrahedra",position="@loader.position")
        tetsga = self.node.createObject('TetrahedronSetGeometryAlgorithms',name="GeomAlgo")    

        dofs = self.node.createObject('MechanicalObject', template='Vec3d', name='dofs',rotation=rotation,translation=translation)


        highOrder_node = Node(self.node, "highOrder_node")

        DefaultSolver(highOrder_node)
        highOrder_node.LinearSolver.iterations = 600
        highOrder_node.LinearSolver.tolerance = 1.0e-12
        highOrder_node.LinearSolver.threshold=1e-12

        highOrder_node.createObject('HighOrderTetrahedronSetTopologyContainer',name="container") # ContainerBezier
        highOrder_node.createObject('Mesh2HighOrderTopologicalMapping',name="topoMapping",input="@"+name+"/Container1",output="@container",
                                                bezierTetrahedronDegree=orderDegree)

        highOrder_node.createObject('MechanicalObject',name="dofs")
        highOrder_node.createObject('UniformMass', totalMass=totalMass)

        highOrder_node.createObject('LagrangeTetrahedronSetGeometryAlgorithms',name="GeomAlgo",
                                                drawControlPoints=0,
                                                drawEdges=1,
                                                drawColorEdges=color)

        # ortho_scalar = [138.76684753783957, 3141.4129587985185, 1644.9974911863344, 523.0648, 37.606, 35.3856]
        # ortho_matrix = [1.0316984366734514e-19, -3.2754811645233607e-21, -2.5808419992050925e-21, 1.9372577089388137e-18, 3.0950201251587604e-17, 3.81618765376334e-17, 6.670970008072477e-18, 5.828336408780264e-16, -4.730307706866279e-16]
        ortho_scalar = [2387.129297021417, 1342.7480845151795, 98.63192673343927, 37.606, 35.3856, 523.0648]
        ortho_matrix =[1.0178227947727454e-14, 9.082503750624732e-15, 5.027047230737284e-16, -7.032065245677738e-16, 7.878519879935228e-16, 3.436740122338369e-18, 1.0479307885140909e-15, 1.1158385634747292e-15, -4.137754316210274e-14]


        high_fem = highOrder_node.createObject('HighOrderTetrahedralCorotationalFEMForceField',
                                                name="Elasticity",  printLog=1,  poissonRatio=poissonRatio,  youngModulus=youngModulus,
                                                integrationMethod=integrationMethod,
                                                method=method,
                                                forceAffineAssemblyForAffineElements=forceAffineAssemblyForAffineElements,
                                                oneRotationPerIntegrationPoint= oneRotationPerIntegrationPoint,
                                                numericalIntegrationMethod=numericalIntegrationMethod,
                                                integrationOrder=integrationOrder,ortho_scalar=ortho_scalar,ortho_matrix=ortho_matrix)

        if withAnysotropy :
            high_fem.elasticitySymmetry   = elasticitySymmetry
            high_fem.anisotropyParameters = anisotropyParameters
            high_fem.anisotropyDirections = anisotropyDirections

        highOrder_node.createObject("LinearSolverConstraintCorrection")

        # if withConstrain:
        #     node.createObject('LinearSolverConstraintCorrection', solverName=solver.name)

        # if collisionMesh:
        #     addCollisionModel(collisionMesh, rotation, translation, scale)

        if surfaceMeshFileName:
                addVisualModel(surfaceMeshFileName, surfaceColor, rotation, translation, scale)


    def addCollisionModel(self, collisionMesh, rotation=[0.0, 0.0, 0.0], translation=[0.0, 0.0, 0.0], scale=[1., 1., 1.]):
        self.collisionmodel = self.node.createChild('CollisionModel')
        self.collisionmodel.createObject('MeshSTLLoader', name='loader', filename=collisionMesh, rotation=rotation, translation=translation, scale=scale)
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

def generateAnisotropicParam(anisotropyType,**kwargs):
    
    if anisotropyType == TRANSVERSE_ISOTROPIC: # 2
        nu = getPoissonRatio(kwargs["poissonRatioLongitudinal"],kwargs["youngModulusLongitudinal"],kwargs["youngModulusTransversal"])
        mu = getShear((kwargs["youngModulusTransversal"]+kwargs["youngModulusLongitudinal"])/2.0,kwargs["poissonRatioLongitudinal"])
        return [anisotropyType,kwargs["youngModulusTransversal"],nu,mu]
    
    elif anisotropyType == CUBIC: # 4
        return [anisotropyType,kwargs["anisotropyRatio"]]

def getPoissonRatio(poissonRatioLongitudinal,youngModulusLongitudinal,youngModulusTransversal):
    return poissonRatioLongitudinal * sqrt(youngModulusLongitudinal/youngModulusTransversal)

def getShear(youngModulus,poissonRatio):
    return youngModulus/(2.0*(1.0+poissonRatio))