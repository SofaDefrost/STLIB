# -*- coding: utf-8 -*-
"""
Templates for rendering.
"""
from splib.objectmodel import SofaPrefab, SofaObject
from stlib.scene import Node

__all__=[]

def ShowGrid(node):
    node.createObject("OglGrid", nbSubdiv=10, size=1000)


@SofaPrefab
class VisualModel(SofaObject):
    """VisualModel Prefab

       This prefab is creating a VisualModel.

       Arguments:
            parent
            surfaceMeshFileName
            color
            rotation
            translation

       Content:
           Node
           {
                name : 'Visual'
                MeshLoader : 'loader'
                OglModel : "model'
           }
    """
    def __init__(self, parent, surfaceMeshFileName, color=[1.0,1.0,1.0], rotation=[0.0,0.0,0.0], translation=[0.0,0.0,0.0]):
        self.node  = Node(parent, "VisualModel")

        if surfaceMeshFileName.endswith(".stl"):
            self.loader = self.node.createObject('MeshSTLLoader',
                                            name="loader",
                                            filename=surfaceMeshFileName)
        elif surfaceMeshFileName.endswith(".obj"):
            self.loader = self.node.createObject('MeshObjLoader',
                                                 name="loader",
                                                 filename=surfaceMeshFileName)
        else:
            print("Extension not handled in STLIB/python/stlib/visuals for file: "+str(surfaceMeshFileName))

        self.model = self.node.createObject('OglModel',
                                        name="model",
                                        src="@loader",
                                        rotation=rotation,
                                        translation=translation,
                                        color=color, updateNormals=False)
