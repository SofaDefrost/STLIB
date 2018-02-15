# -*- coding: utf-8 -*-
"""
Templates for rendering.
"""
__all__=[]

def ShowGrid(node):
    node.createObject("OglGrid", nbSubdiv=10, size=1000)
