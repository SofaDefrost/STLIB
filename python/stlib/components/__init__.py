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

def OrientedBoxRoi(parentNode, position, name="BoxRoi", translation=[0.0,0.0,0.0], eulerRotation=[0.0,0.0,0.0], scale=[1.0,1.0,1.0]):
    
    orientedBox = OrientedBoxFromTransform(translation,eulerRotation,scale)
    parentNode.createObject("BoxROI", position=position, orientedBox=orientedBox, drawBoxes=True )
    
    return parentNode

def OrientedBoxFromTransform(translation=[0.0,0.0,0.0], eulerRotation=[0.0,0.0,0.0], scale=[1.0,1.0,1.0]):
    from stlib.numerics import *
    # BoxROI unitaire
    pos = [[-0.5, 0.0,-0.5],
           [-0.5, 0.0, 0.5],
           [ 0.5, 0.0, 0.5]]

    depth = [scale[2]]

    return transformPosition(position=pos, translation=translation, eulerRotation=eulerRotation, scale=scale) + depth

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

    OrientedBoxRoi(floor, name="MyBoxRoi",position=[[50,0,0],[15,15,0],[60,70,25]],scale=[100,100,100])

    myOrientedBox = OrientedBoxFromTransform(translation=[400,100,100],eulerRotation=[0,65,0],scale=[400,400,800])
    floor.createObject("BoxROI", orientedBox=myOrientedBox, drawBoxes=True )