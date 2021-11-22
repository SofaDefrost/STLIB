# -*- coding: utf-8 -*-
"""
Templates for rendering.
"""
import Sofa
from splib.objectmodel import SofaPrefab, SofaObject
from stlib.scene import Node

def ShowGrid(node):
    node.addObject("OglGrid", nbSubdiv=10, size=1000)


@SofaPrefab
class VisualModel(SofaObject):
    """VisualModel Prefab

       This prefab is creating a VisualModel.

       Arguments:
            parent
            surfaceMeshFileName
            name
            color
            rotation
            translation
            scale

       Content:
           Node
           {
                name : 'Visual'
                MeshLoader : 'loader'
                OglModel : "model'
           }
    """

    def __init__(self, parent, surfaceMeshFileName, name="VisualModel", color=[1., 1., 1.], rotation=[0., 0., 0.], translation=[0., 0., 0.], scale=[1., 1., 1.]):
        self.node = Node(parent, name)

        if not self.getRoot().hasObject("SofaOpenglVisual"):
            if not self.getRoot().hasObject("/Config/SofaOpenglVisual"):
                    Sofa.msg_info(self.getRoot(), "Missing RequiredPlugin SofaOpenglVisual in the scene, add it from Prefab VisualModel.")
                    self.getRoot().addObject("RequiredPlugin", name="SofaOpenglVisual")

        if surfaceMeshFileName.endswith(".stl"):
            self.loader = self.node.addObject('MeshSTLLoader',
                                                 name="loader",
                                                 filename=surfaceMeshFileName)
        elif surfaceMeshFileName.endswith(".obj"):
            self.loader = self.node.addObject('MeshObjLoader',
                                                 name="loader",
                                                 filename=surfaceMeshFileName)
        else:
            print("Extension not handled in STLIB/python/stlib/visuals for file: "+str(surfaceMeshFileName))

        self.model = self.node.addObject('OglModel',
                                            name="model",
                                            src="@loader",
                                            rotation=rotation,
                                            translation=translation,
                                            scale3d=scale,
                                            color=color, updateNormals=False)
def createScene(root):
    from stlib.scene import Scene
    scene = Scene(root, plugins=["SofaLoader"])
    scene.addSettings()
    scene.addModelling()
    scene.addSimulation()

    visu = VisualModel(scene.Modelling, surfaceMeshFileName="mesh/smCube27.obj")

