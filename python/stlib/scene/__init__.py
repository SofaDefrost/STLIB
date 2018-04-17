# -*- coding: utf-8 -*-
"""
Templates for most of the common scene setups.

Content:
********
.. autosummary::

    MainHeader
    ContactHeader
    Node

|

.. autofunction:: MainHeader
.. autofunction:: ContactHeader
.. autofunction:: Node

"""
from splib.objectmodel import SofaPrefab, SofaObject
from splib.scenegraph import get

from mainheader import MainHeader
from contactheader import ContactHeader
from stlib.solver import DefaultSolver

def Node(parentNode, name):
    """Create a new node in the graph and attach it to a parent node."""
    return parentNode.createChild(name)


@SofaPrefab
class Scene(SofaObject):
    def __init__(self, node):
        self.node = node
        MainHeader(node)
        self.visualstyle = get(node, "VisualStyle")

    def addSolver(self):
        self.solver = DefaultSolver(self.node)


