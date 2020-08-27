# -*- coding: utf-8 -*-
"""
Templates for rendering.
"""

import Sofa.Core
from stlib import types
class VisualModel(Sofa.Prefab):
    """  """
    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)
    """ Prefab parameters: """
    def createParams(self, *args, **kwargs):
        self.addPrefabParameter(name='VisualMeshPath', type=types.String, help='Path to visual mesh file', default=kwargs.get('VisualMeshPath', None))
    def doReInit(self):
        #for i in range(0, self.somePythonAttr):
        #    print("kikoo")
        print(self.VisualMeshPath.value)
        Path = self.VisualMeshPath.value
        if Path.endswith('.stl'):
            self.addObject('MeshSTLLoader', name='loader',filename=Path)
        elif Path.endswith('.obj'):
            self.addObject('MeshOBJLoader', name='loader',filename=VisualMeshPath)
        else:
            print("Extension not handled in STLIB/python/stlib/visuals for file: "+str(Path))

        self.addObject('Mesh', src='@loader', name='topo')
        self.addObject('OglModel', name="OglModel", src="@loader", updateNormals=False)
        self.addObject('BarycentricMapping')
