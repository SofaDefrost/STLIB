# -*- coding: utf-8 -*-
"""
Scene debuging facilities.

"""
import Sofa
import SofaPython
from stlib.scene import Node
from OpenGL.GL import *

SofaPython.__SofaPythonEnvironment_modulesExcludedFromReload.append("OpenGL.GL")

debugManager=None
def DebugManager(parentNode):
    global debugManager
    debugManager = Node(parentNode, "DebugManager")
    ImmediateRenderer(debugManager)
    return debugManager

currentImmediateRenderer = None

def drawLine(p0,p1):
    if currentImmediateRenderer == None:
        return
    currentImmediateRenderer.addEdge(p0, p1)

class ImmediateRenderer(Sofa.PythonScriptController):
    def __init__(self, rootNode):
        global currentImmediateRenderer
        self.edges = []
        currentImmediateRenderer = self

    def addEdge(self, p0, p1):
        self.edges.append([p0,p1])

    def draw(self):
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glBegin(GL_LINES)
        glColor3f(1.0,0.0,0.0)
        for e in self.edges:
            glVertex3dv(e[0])
            glVertex3dv(e[1])
        glEnd
        self.edges = []

class TracerLog(object):
    def __init__(self, filename):
        self.outfile = open(filename, "wt")

    def writeln(self, s):
        self.outfile.write(s+"\n")

    def close(self):
        self.outfile.close()


def kwargs2str(kwargs):
    s=""
    for k in kwargs:
        s+=", "+k+"="+repr(kwargs[k])
    return s

class Tracer(object):

    def __init__(self, node, backlog, depth, context):
        self.node = node
        self.backlog = backlog
        self.depth = depth
        self.context = context

    def createObject(self, type, **kwargs):
        self.backlog.writeln(self.depth+self.node.name+".createObject('"+type+"' "+kwargs2str(kwargs)+")")
        n = self.node.createObject(type, **kwargs)
        return n

    def createChild(self, name, **kwargs):
        self.backlog.writeln("")
        self.backlog.writeln(self.depth+"#========================= "+name+" ====================== ")
        self.backlog.writeln(self.depth+name+" = "+self.node.name+".createChild('"+name+"' "+kwargs2str(kwargs)+")")
        n = Tracer(self.node.createChild(name, **kwargs), self.backlog, self.depth, name)
        return n

    def getObject(self, name):
        n = self.node.getObject(name)
        return n

    def addObject(self, tgt):
        self.backlog.writeln(self.depth+self.node.name+".addObject('"+tgt.name+"')")
        if isinstance(tgt, type(Tracer)):
            return self.node.addObject(tgt.node)
        return self.node.addObject(tgt)

    def __getattr__(self, value):
        return self.node.__getattribute__(value)
