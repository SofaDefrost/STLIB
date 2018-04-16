# -*- coding: utf-8 -*-
"""
Utilitary function to ease the writing of scenes.

Functions:
**********
.. autosummary::

    stlib.tools.loadPointListFromFile

.. autofunction:: stlib.tools.loadPointListFromFile

"""
__all__=[]


def loadPointListFromFile(s):
    import json

    """Load a set of 3D point from a json file"""
    return json.load(open(s))
