# -*- coding: utf-8 -*-
from rigidobject import RigidObject

def Cube(node, **kwargs):
    return RigidObject(node, shapeFromFile="mesh/cube.obj", **kwargs)

def Sphere(node, **kwargs):
    return RigidObject(node, shapeFromFile="mesh/ball.obj", **kwargs)

def Floor(node, **kwargs):
    return RigidObject(node, shapeFromFile="mesh/floor.obj", **kwargs)

def createScene(rootNode):
    from stlib.scene import STLIBHeader
    from stlib.solver import DefaultSolver

    STLIBHeader(rootNode)
    DefaultSolver(rootNode)
    Cube(rootNode, translation=[5.0,0.0,0.0])
    Sphere(rootNode, translation=[-5.0,0.0,0.0])
    Floor(rootNode, translation=[0.0,-1.0,0.0])
