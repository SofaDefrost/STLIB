#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 16:34:41 2019

@author: stefan
"""

import splib.geometric.gmesh

def ParametricMeshLoader(Node, MeshFile, OutputDir='autogen/',Type='Surface', **kwargs):
    if Type == 'Surface':
        SurfaceMeshPath = meshFromParametricGeometry(MeshFile, outputdir=OutputDir, meshtype=Type, **kwargs)
        Node.createObject("MeshSTLLoader", name="loader", filename=SurfaceMeshPath)
    elif Type == 'Tetra':
        TetraMesh = meshFromParametricGeometry(MeshFile, outputdir=OutputDir, meshtype=Type, **kwargs)
        Node.createObject('MeshVTKLoader', name='loader', filename=TetraMesh)
     