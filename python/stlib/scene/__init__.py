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

def Node(parentNode, Name):
    """Create a new node and attach it to the provided node"""
    return parentNode.createChild(Name)
