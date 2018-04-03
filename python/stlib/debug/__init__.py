# -*- coding: utf-8 -*-
"""
Scene debuging facilities.

"""
import Sofa
import SofaPython
import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


SofaPython.__SofaPythonEnvironment_modulesExcludedFromReload.append("OpenGL.GL")
SofaPython.__SofaPythonEnvironment_modulesExcludedFromReload.append("OpenGL.GLU")
SofaPython.__SofaPythonEnvironment_modulesExcludedFromReload.append("OpenGL.GLUT")

debugManager=None
def DebugManager(parentNode):
    global debugManager
    ImmediateRenderer(parentNode)
    return parentNode

currentImmediateRenderer = None
def drawText(text, x, y):
    global currentImmediateRenderer
    if currentImmediateRenderer == None:
        return
    currentImmediateRenderer.addText(text,x,y)

def drawLine(p0,p1):
    global currentImmediateRenderer
    if currentImmediateRenderer == None:
        return
    currentImmediateRenderer.addEdge(p0, p1)

def worldToScreenPoint(p):
    return gluProject(p[0],p[1],p[2], currentImmediateRenderer.mvm,
                      currentImmediateRenderer.pm, currentImmediateRenderer.viewport)


def BluePrint(parentNode, name="BluePrint"):
    class BluePrintController(Sofa.PythonScriptController):
        def __init__(self, node):
            self.name = "Controller"
            self.rules

        def addRule(self, origin=[0.0,0.0,0.0], direction=[1.0,0.0,0.0], spacing=1.0, length=10, text="cm"):
            pass

        def addCircle(self, origin, radius):
            pass

        def drawRule(self, o,d,s,t):
            step = length / spacing
            for i in range(0, int(step)):
                drawLine()

        def draw(self):
            for rule in self.rules:
                print("HEllow")

    c = parentNode.createChild(name)
    BluePrintController(c)
    return c

class ImmediateRenderer(Sofa.PythonScriptController):
    def __init__(self, rootNode):
        global currentImmediateRenderer
        self.name = "DebugManager"
        self.edges = []
        self.textes = []
        currentImmediateRenderer = self
        glutInit()
        self.mvm = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.pm = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport = glGetInteger( GL_VIEWPORT )


    def addText(self, text, x, y):
        self.textes.append([text,int(x),int(y)])

    def addEdge(self, p0, p1):
        self.edges.append([p0,p1])

    def addRenderable(self, r):
        self.renderable.append(r)

    def drawAll2D(self):
        viewport = glGetInteger( GL_VIEWPORT );

        glDepthMask(GL_FALSE)

        glPushAttrib( GL_LIGHTING_BIT )
        glPushAttrib( GL_ENABLE_BIT )
        glEnable( GL_COLOR_MATERIAL )
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glEnable( GL_LINE_SMOOTH )
        glEnable( GL_POLYGON_SMOOTH )
        glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, viewport[2], 0, viewport[3] )

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glLineWidth(1.0)
        glBegin(GL_LINES)
        glColor(1.0,1.0,1.0)
        glVertex3d(-100,480,0)
        glVertex3d(1000,480,0)
        glEnd()

        self.drawAllText()

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glPopAttrib()
        glPopAttrib()

        glDepthMask(GL_TRUE)

    def drawAllText(self):
        for text in self.textes:
            glRasterPos2i( text[1], text[2] )
            glColor(1.0,0.0,0.0)
            for c in text[0]:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

    def onBeginAnimationStep(self, dt):
        self.textes = []
        self.edges = []

    def draw(self):
        self.mvm = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.pm = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport = glGetInteger( GL_VIEWPORT )

        self.drawAll2D()

        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor3f(1.0,0.0,0.0)
        for e in self.edges:
            glVertex3dv(e[0])
            glVertex3dv(e[1])
        glEnd()


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
