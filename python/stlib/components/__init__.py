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

def OrientedBoxRoi(parentNode, position, translation=[0.0,0.0,0.0], eulerRotation=[0.0,0.0,0.0], scale=[1.0,1.0,1.0], name="BoxRoi"):
    from stlib.numerics import *
    pos = [[-0.5, 0.0,-0.5, 1],
           [-0.5, 0.0, 0.5, 1],
           [ 0.5, 0.0, 0.5, 1]]

    trs = TRS_to_matrix(translation=translation, eulerRotation=eulerRotation, scale=scale)
    tp = []
    for p in pos:
        np = numpy.matmul( trs, numpy.array( p[0:3]+[1.0] ) )
        tp.append( np[0:3].tolist() )

    depth = [1.0]
    return parentNode.createObject("BoxROI", position=position, orientedBox=tp+depth, drawBoxes=True )
