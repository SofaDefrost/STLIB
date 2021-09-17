# -*- coding: utf-8 -*-
"""
Templates for most of the common scene setups.

**Content:**

.. _sphinx_hyperlinks:

.. autosummary::

    Scene
    MainHeader
    ContactHeader
    Node
    Wrapper

|

stlib.scene.Scene
*****************

.. autoclass:: Scene
   :members:
   :undoc-members:

stlib.scene.Interaction
***********************

.. autoclass:: Interaction
   :members:
   :undoc-members:

stlib.scene.MainHeader
**********************

.. autofunction:: MainHeader

stlib.scene.ContactHeader
*************************

.. autofunction:: ContactHeader

stlib.scene.Node
****************

.. autofunction:: Node

stlib.scene.Wrapper
*******************

.. autoclass:: Wrapper
   :members:
   :undoc-members:
   :special-members: __getattr__

"""
__all__=["scene", "interaction", "contactheader", "mainheader", "wrapper"]

def Node(parentNode, name):
    """Create a new node in the graph and attach it to a parent node."""
    return parentNode.addChild(name)

from splib.objectmodel import SofaPrefab, SofaObject
from splib.scenegraph import get

from stlib.scene.scene import Scene
from stlib.scene.mainheader import MainHeader
from stlib.scene.contactheader import ContactHeader
from stlib.scene.interaction import Interaction
from stlib.scene.wrapper import Wrapper
from stlib.solver import DefaultSolver



