#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:09:31 2020

@author: stefan
"""

"""type: SofaContent"""
import Sofa.Core
from stlib3 import types

class FixedBox(Sofa.Prefab):
    """  """

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)
    """ Prefab parameters: """

    def createParams(self, *args, **kwargs):
        self.addPrefabParameter(name='BoxCoords', type=types.Vec6, help=' Coordinates expressed as follows: [minX, minY, minZ, maxX, maxY, maxZ]', default=kwargs.get('BoxCoords', [0,0,0,1,1,1], ))
        self.addPrefabParameter(name='ShowBox', type=types.Bool, help='Visualize box', default=kwargs.get('ShowBox',None))

    def doReInit(self):
        self.addObject('BoxROI', name='BoxROI', box=self.BoxCoords, drawBoxes=self.ShowBox)
        self.addObject('RestShapeSpringsForceField', points='@BoxROI.indices', stiffness=1e12)
