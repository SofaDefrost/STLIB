# -*- coding: utf-8 -*-
"""
Templates for rendering.
"""

import Sofa.Core


class VisualModel(Sofa.Prefab):
    """  """
    properties = [
        {'name':'visualMeshPath', 'type':'string', 'help':'Path to visual mesh file',  'default':''},
        {'name':'translation',    'type':'Vec3d',  'help':'translate visual model',    'default':[0.,0.,0.]},
        {'name':'rotation',       'type':'Vec3d',  'help':'rotate visual model',       'default':[0.,0.,0.]},
        {'name':'scale',          'type':'Vec3d',  'help':'scale visual model',        'default':[0.,0.,0.]},
        {'name':'color',          'type':'string',  'help':'color put to visual model', 'default':"1. 0. 1. 1."}]

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

    def doReInit(self):
        path = self.visualMeshPath.value
        if path.endswith('.stl'):
            self.addObject('MeshSTLLoader', name='loader',filename=path)
        elif path.endswith('.obj'):
            self.addObject('MeshObjLoader', name='loader',filename=path)
        else:
            print("Extension not handled in STLIB/python/stlib/visuals for file: "+str(path))

        self.addObject('MeshTopology', src='@loader', name='topo')
        self.addObject('OglModel', name="OglModel", src="@loader",
                                                    rotation=self.rotation.value,
                                                    translation=self.translation.value,
                                                    scale3d=self.scale.value,
                                                    color=self.color.value, updateNormals=False)

    def showGrid(self,nbSubdiv=10,size=1000):
        self.addObject("OglGrid", nbSubdiv=nbSubdiv, size=size)

def createScene(root):

    from stlib3.scene.Scene import Scene

    scene = Scene(root,plugins=["SofaOpenglVisual"])
    scene.addSettings()
    scene.addModelling()
    scene.addSimulation()

    visu = VisualModel(visualMeshPath="mesh/smCube27.obj")
    visu.showGrid()
    scene.Modelling.addChild(visu)