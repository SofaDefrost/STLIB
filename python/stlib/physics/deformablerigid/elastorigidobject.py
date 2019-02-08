# -*- coding: utf-8 -*-
from splib.numerics import Vec3, Quat, sdiv
from stlib.scene import MainHeader
from stlib.physics.deformable import ElasticMaterialObject
from stlib.components import addOrientedBoxRoi


# TODO List
# Crash when root contains MechanicalObject
# TODO(dmarchal) Add gather the Rigid DOF-mapping inside rigidified part.
# TODO(dmarchal) Instead of boxframe
def ElastoRigidObject(targetObject, sourceObject, frameOrientation, indicesLists, pointsLists):
        """
            :param targetObject: parent node where to attach the final object.
            :param sourceObject: node containing the deformable object.
            :param framesOrientation: array of orientation. The length of the array should be equal to the number
                                    of rigid component. The orientation are given in eulerAngles (in degree) by passing
                                    three values or using a quaternion by passing four values.
                                    [[0,10,20], [0.1,0.5,0.3,0.4]]
            :param indicesLists: array of indices to rigidify. The length of the array should be equal to the number
                                of rigid component.
            :param pointsLists: array of points to rigidify. The length of the array should be equal to the number
                                of rigid component.

        """
        sourceObject.init()
        elastoRigidObject = targetObject.createChild("ElastoRigidObject")

        allPositions = sourceObject.container.position
        allIndices = map(lambda x: x[0], sourceObject.container.points)

        centers = []
        selectedIndices = []
        indicesMap = []
        for index in range(len(indicesLists)):
            boxFrame = frameOrientation[index]
            orientation = Quat.createFromEuler(boxFrame)
            center = sdiv(sum(map(Vec3, pointsLists[index])), float(len(pointsLists[index]))) + list(orientation)
            centers.append(center)
            selectedIndices += map(lambda x: x[0], indicesLists[index])
            indicesMap += [index] * len(indicesLists[index])

        otherIndices = filter(lambda x: x not in selectedIndices, allIndices)
        Kd = {v: None for k, v in enumerate(allIndices)}
        Kd.update({v: [0, k] for k, v in enumerate(otherIndices)})
        Kd.update({v: [1, k] for k, v in enumerate(selectedIndices)})
        indexPairs = [v for kv in Kd.values() for v in kv]
        freeParticules = elastoRigidObject.createChild("DeformableParts")
        freeParticules.createObject("MechanicalObject", template="Vec3", name="freedofs",
                                    position=[allPositions[i] for i in otherIndices],
                                    showObject=True, showObjectScale=2, showColor=[1.0, 0.0, 1.0, 1.0])

        rigidParts = elastoRigidObject.createChild("RigidParts")
        rigidParts.createObject("MechanicalObject", template="Rigid", name="dofs", reserve=len(centers),
                                showObject=True, showObjectScale=15, position=centers)

        rigidifiedParticules = rigidParts.createChild("RigidifiedParticules")
        rigidifiedParticules.createObject("MechanicalObject", template="Vec3", name="dofs",
                                          position=[allPositions[i] for i in selectedIndices],
                                          showObject=True, showObjectScale=2, showColor=[1.0, 1.0, 0.0, 1.0])
        rigidifiedParticules.createObject("RigidMapping", globalToLocalCoords='true', rigidIndexPerPoint=indicesMap)

        interactions = elastoRigidObject.createChild("MaterialCoupling")
        c = sourceObject.container
        sourceObject.removeObject(sourceObject.solver)
        sourceObject.removeObject(sourceObject.integration)
        sourceObject.removeObject(sourceObject.LinearSolverConstraintCorrection)


        interactions.createObject("MechanicalObject",
                                  template="Vec3", name="dofs",
                                  position=sourceObject.container.position)

        interactions.createObject("SubsetMultiMapping", template="Vec3,Vec3",
                                  input=freeParticules.freedofs.getLinkPath()+" "+rigidifiedParticules.dofs.getLinkPath(),
                                  output='@.',
                                  indexPairs=indexPairs)

        interactions.addObject(c)
        interactions.createObject("TetrahedronFEMForceField", youngModulus=sourceObject.forcefield.youngModulus, poissonRatio=sourceObject.forcefield.poissonRatio)
        interactions.createObject("UniformMass", name="mass", vertexMass=sourceObject.mass.vertexMass)


        rigidifiedParticules.addChild(interactions)
        freeParticules.addChild(interactions)
        elastoRigidObject.removeChild(interactions)
        sourceObject.node.activated = False

        return elastoRigidObject


def createScene(rootNode):

        MainHeader(rootNode, plugins=["SofaSparseSolver"])
        rootNode.VisualStyle.displayFlags = "showBehavior"
        rootNode.createObject("DefaultAnimationLoop")
        rootNode.createObject("DefaultVisualManagerLoop")
        rootNode.gravity = "0 -9810 0"

        elasticobject = ElasticMaterialObject(rootNode,
                                              volumeMeshFileName="mesh/liver2.msh",
                                              youngModulus=100, poissonRatio=0.3, scale=[100, 100, 100], translation=[30, -20, 20], totalMass=3.5)

        simulation = rootNode.createChild("Simulation")
        simulation.createObject("EulerImplicit")
        simulation.createObject("CGLinearSolver")

        elasticobject.init()
        box1 = addOrientedBoxRoi(elasticobject, elasticobject.loader.position,
                                 translation=[20, 0, 10],
                                 eulerRotation=[0., 0., 90],
                                 scale=[50.0, 50.0, 50.0],
                                 name='filters1')
        box1.init()
        box2 = addOrientedBoxRoi(elasticobject, elasticobject.loader.position,
                                 translation=[100, -10, 50],
                                 eulerRotation=[0., 0., 90],
                                 scale=[40.0, 40.0, 40.0],
                                 name='filters2')
        box2.init()
        indices = [box1.indices, box2.indices]
        points = [box1.pointsInROI, box2.pointsInROI]

        o = ElastoRigidObject(simulation, elasticobject,
                              frameOrientation=[[0, 0, 0], [0, 0, 0]],
                              indicesLists=indices, pointsLists=points)

        o.RigidParts.createObject("FixedConstraint", indices=0)
