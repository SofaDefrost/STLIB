# -*- coding: utf-8 -*-
"""
Python templates for all sofa components.

Content:
********

.. autosummary::
    :toctree: _autosummary

.. automodule:: stlib3.components.all
    :members:


"""
__all__ = ["all"]

from splib3.numerics import getOrientedBoxFromTransform


def addOrientedBoxRoi(parentNode, position, name="BoxROI", translation=[0., 0., 0.], eulerRotation=[0., 0., 0.], scale=[1., 1., 1.], drawBoxes=True):
    orientedBox = getOrientedBoxFromTransform(translation=translation, eulerRotation=eulerRotation, scale=scale)
    return parentNode.addObject("BoxROI", name=name, position=position, orientedBox=orientedBox, drawBoxes=drawBoxes)


def OrientedBoxFromTransform(translation=[0., 0., 0.], eulerRotation=[0., 0., 0.], scale=[1., 1., 1.]):
    raise Exception("This function is now deprecated and replaced with splib3.numerics.getOrientedBoxFromTransform. Please update your code.")


def createScene(rootNode):
    from stlib3.scene import MainHeader
    from stlib3.physics.rigid import Floor

    MainHeader(rootNode, plugins=["SofaPython"],
               dt=1.,
               gravity=[0., -9810., 0.])

    rootNode.VisualStyle.displayFlags = "showVisual showBehavior"

    floor = Floor(rootNode,
                  name="Plane",
                  color=[1., 0., 1.],
                  isAStaticObject=True,
                  uniformScale=10)

    addOrientedBoxRoi(floor, name="MyBoxRoi", position=[[50, 0, 0], [15, 15, 0], [60, 70, 25]], scale=[100, 100, 100])

    myOrientedBox = getOrientedBoxFromTransform(translation=[400, 100, 100], eulerRotation=[0, 65, 0], scale=[400, 400, 800])
    floor.addObject("BoxROI", orientedBox=myOrientedBox, drawBoxes=True)
