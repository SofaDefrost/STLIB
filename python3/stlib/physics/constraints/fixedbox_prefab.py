#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:09:31 2020

@author: stefan
"""

"""type: SofaContent"""
import Sofa.Core
from stlib import types
class FixedBox(Sofa.Prefab):
    """  """
    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)
    """ Prefab parameters: """
    def createParams(self, *args, **kwargs):
        self.addPrefabParameter(name='BoxCoords', type=types.Vec6d, help=' Coordinates expressed as follows: [minX, minY, minZ, maxX, maxY, maxZ]', default=kwargs.get('BoxCoords', [0,0,0,1,1,1], ))
        self.addPrefabParameter(name='ShowBox', type=types.Bool, help='Visualize box', default=kwargs.get('ShowBox',None))
        #self.somePythonAttr = kwargs.get("test", 42)
        #self.addPrefabParameter(name='nModels', type='int', help='number of OglModels to create', default=kwargs.get('nModels', None))
        #self.addPrefabParameter(name='loader', type='Link', help='', default=kwargs.get('loader', None))
    def doReInit(self):
        #for i in range(0, self.somePythonAttr):
        #    print("kikoo")
        self.addObject('BoxROI', name='BoxROI', box=self.BoxCoords, drawBoxes=self.ShowBox)
        self.addObject('RestShapeSpringsForceField', points='@BoxROI.indices', stiffness='1e12')
        print('blupsi prefab')
    
