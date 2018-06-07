# -*- coding: utf-8 -*-
"""
Utilitary function to ease the writing of scenes.

.. autosummary::

    loadPointListFromFile

splib.loaders.loadPointListFromFile
***********************************
.. autofunction:: loadPointListFromFile

"""
__all__=[]


def loadPointListFromFile(s):
    import json

    """Load a set of 3D point from a json file"""
    return json.load(open(s))
