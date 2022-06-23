#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:09:31 2020

@author: stefan
"""

"""type: SofaContent"""
import Sofa.Core
from Sofa.Helper import msg_deprecated


class FixedBox(Sofa.Prefab):
    """  """

    prefabData = [
        {"name": "boxCoords", "type": "Vec6f",
         "help": "Coordinates expressed as follows: [minX, minY, minZ, maxX, maxY, maxZ]",
         "default": [0, 0, 0, 1, 1, 1]},

        {"name": "showBox", "type": "bool",
         "help": "Visualize box",
         "default": False},

        {"name": "BoxCoords", "help": "deprecated, use boxCoords instead", "type": "Vec6f", 'default' : [0,0,0,1,1,1] },
        {"name": "ShowBox", "help": "deprecated, use showBox instead", "type": "bool", 'default' : False}
    ]

    def __init__(self, *args, **kwargs):
        if "parent" not in kwargs:
            raise TypeError("Missing positional argument 'parent' (Sofa.Core.Node). FixingBox needs that the provided 'parent' contains a mechanical object.")
        Sofa.Prefab.__init__(self, *args, **kwargs)
        if kwargs.get('BoxCoords') is not None:
            kwargs['boxCoords'] = kwargs.get('BoxCoords')
            msg_deprecated('BoxCoords parameter is deprecated, use boxCoords instead')

        if kwargs.get('ShowBox') is not None:
            kwargs['showBox'] = kwargs.get('ShowBox')
            msg_deprecated('ShowBox parameter is deprecated, use showBox instead')

    def init(self):
        self.addObject('BoxROI', name='BoxROI', box=self.boxCoords, drawBoxes=self.showBox)
        self.addObject('RestShapeSpringsForceField', points='@BoxROI.indices', stiffness=1e12)


def createScene(rootnode):
    rootnode.addObject('RequiredPlugin', pluginName=[
        "Sofa.Component.Visual",  # Needed to use components VisualStyle
        "Sofa.GL.Component.Rendering3D",  # Needed to use components OglSceneFrame
        "Sofa.Component.StateContainer"
    ])

    rootnode.addObject("MechanicalObject", name="dofs", position=[[0.0,1.0,2.0],[2.0,3.0,4.0], [0.5,0.5,0.5]],
                        showObject=True, showObjectScale=10.0)
    FixedBox(boxCoords=[0, 0, 0, 1, 1, 1], showBox=True, parent=rootnode)
