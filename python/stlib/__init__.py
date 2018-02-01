# -*- coding: utf-8 -*-
"""
The Sofa Template Library.
==========================

Utility functions and scene templates for the real-time simulation framework SOFA.
The different templates are organized in types and abstract the complexity of object
creation with SOFA.

Example:
********

.. sourcecode:: python

    from stlib.scene import STLIBHeader
    from stlib.solver import DefaultSolver
    from stlib.physics.rigid import Cube, Sphere, Floor
    from stlib.physics.deformable import ElasticMaterialObject

    def createScene(rootNode):
        STLIBHeader(rootNode)
        DefaultSolver(rootNode)
        AnimationManager(rootNode)

        Sphere(rootNode, name="sphere", translation=[-5.0, 0.0, 0.0])
        Cube(rootNode, name="cube", translation=[5.0,0.0,0.0])

        ElasticMaterialObject(rootNode, name="dragon",
                              surface="mesh/dragon.obj", volume="mesh/liver.msh",
                              translation=[0.0,0.0,0.0])

        Floor(rootNode, name="plane", translation=[0.0, -1.0, 0.0])


Content of the library
**********************

.. autosummary::
    :toctree: _autosummary

    stlib.physics
    stlib.visuals
    stlib.solver
    stlib.scene
    stlib.tools


Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

"""
__all__=["physics", "visuals", "solver", "scene", "tools"]
