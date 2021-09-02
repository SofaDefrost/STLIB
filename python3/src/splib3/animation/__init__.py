# -*- coding: utf-8 -*-
"""
Animation framework focusing in ease of use.

**********
Functions:
**********

.. autosummary::

    animate
    AnimationManager
    AnimationManagerController


splib3.animation.animate
***********************
.. autofunction:: animate

splib3.animation.AnimationManager
********************************
.. autofunction:: AnimationManager

splib3.animation.AnimationManagerController
******************************************
.. autoclass:: AnimationManagerController(Sofa.PythonScriptController)
   :members: addAnimation

********
Modules:
********

.. autosummary::
    :toctree: _autosummary

    splib3.animation.easing

"""
__all__=["animate", "easing"]

from splib3.animation.animate import AnimationManager, AnimationManagerController, animate
