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

       Content:
           Node
           {
                name : 'Visual'
                MeshLoader : 'loader'
                OglModel : "model'
           }
    """
    def __init__(self, parent, surfaceMeshFileName, color=[1.0,1.0,1.0]):
        self.node  = Node(parent, "VisualModel")

        self.loader = self.node.createObject('MeshSTLLoader',
                                        name="loader",
                                        filename=surfaceMeshFileName)

        self.model = self.node.createObject('OglModel',
                                        name="model",
                                        position='@loader.position',
                                        triangles='@loader.triangles',
                                        color=color)
