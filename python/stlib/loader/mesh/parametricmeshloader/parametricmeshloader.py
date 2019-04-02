#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 16:34:41 2019

@author: stefan
"""

from splib.geometric.gmesh import meshFromParametricGeometry

def ParametricMeshLoader(Node, MeshFile, OutputDir='autogen/',MeshType='Surface', **kwargs):
    if MeshType == 'Surface':        
        SurfaceMeshPath = meshFromParametricGeometry(MeshFile, outputdir=OutputDir, meshtype=MeshType, **kwargs)
        Node.createObject("MeshSTLLoader", name="loader", filename=SurfaceMeshPath)
    elif MeshType == 'Volumetric':
        TetraMesh = meshFromParametricGeometry(MeshFile, outputdir=OutputDir, meshtype=MeshType, **kwargs)
        Node.createObject('MeshVTKLoader', name='loader', filename=TetraMesh)
     