# -*- coding: utf-8 -*-
"""
Python templates for all sofa components.

Content:
********

.. autosummary::
    :toctree: _autosummary

.. automodule:: stlib.components.all
    :members:


"""

__all__=["all"]

def OrientedBoxRoi(parentNode, positions, name="BoxRoi", translation=[0.0,0.0,0.0], eulerRotation=[0.0,0.0,0.0], scale=[1.0,1.0,1.0], depth = [1.0]):
    from stlib.numerics import *
    if len(positions) != 3:
        raise Exception('An orientedBox is defined by 3 points, number of points given : %i' % len(positions))


    positionTRS = positionsTRS(positions=positions, translation=translation, eulerRotation=eulerRotation, scale=scale)

    parentNode.createObject("BoxROI", name=name, position=positions, orientedBox=positionTRS+depth, drawBoxes=True )

    return parentNode


def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.physics.rigid import Floor

    MainHeader(rootNode,plugins=["SofaPython","SoftRobots","ModelOrderReduction"],
                        dt=1,
                        gravity=[0.0,-9810,0.0])

    floor =Floor(rootNode,
            name = "Plane",
            color = [1.0, 0.0, 1.0],
            isAStaticObject = True,
            uniformScale = 10)

    OrientedBoxRoi(floor,[[0.0, 0.0, 0], [150.0, 0, 0], [150.0, -100.0, 0]],translation=[0,100,0],eulerRotation=[650,0,0],depth=[50])