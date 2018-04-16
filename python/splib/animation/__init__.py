# -*- coding: utf-8 -*-
"""
Animation framework focusing in ease of use.

Modules:
********
.. autosummary::
    :toctree: _autosummary

    stlib.animation.easing

Functions:
**********
.. autosummary::

    stlib.animation.AnimationManager
    stlib.animation.animate

.. autofunction:: stlib.animation.AnimationManager
.. autofunction:: stlib.animation.animate


"""
__all__=["animate", "easing"]
from animate import AnimationManager, animate
