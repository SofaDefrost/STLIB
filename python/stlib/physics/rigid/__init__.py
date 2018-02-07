# -*- coding: utf-8 -*-
"""

This package is focused on implementing a standard rigid object for sofa. The object is
made described by its surface mesh.

Content:
********
.. autosummary::

    RigidObject
    Cube
    Sphere
    Floor

|

.. autofunction:: RigidObject
.. autofunction:: Cube
.. autofunction:: Sphere
.. autofunction:: Floor


"""

from rigidobject import RigidObject

def Cube(node, **kwargs):
    """Create a rigid cube of unit dimension"""
    return RigidObject(node, shapeFromFile="mesh/cube.obj", **kwargs)

def Sphere(node, **kwargs):
    """Create a rigid sphere of unit dimension"""
    return RigidObject(node, shapeFromFile="mesh/ball.obj", **kwargs)

def Floor(node, **kwargs):
    """Create a rigid floor of unit dimension"""
    return RigidObject(node, shapeFromFile="mesh/floor.obj", **kwargs)

def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.solver import DefaultSolver

    MainHeader(rootNode)
    DefaultSolver(rootNode)
    Cube(rootNode, translation=[5.0,0.0,0.0])
    Sphere(rootNode, translation=[-5.0,0.0,0.0])
    Floor(rootNode, translation=[0.0,-1.0,0.0])
