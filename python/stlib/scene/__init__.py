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

from mainheader import MainHeader
from contactheader import ContactHeader
from stlib.algorithms import get

def Node(parentNode, name):
    """Create a new node in the graph and attach it to a parent node."""
    return parentNode.createChild(name)

