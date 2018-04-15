# -*- coding: utf-8 -*-
"""
Numerics components we often use.

Content:
********
.. autosummary::
    :toctree: _autosummary

.. automodule::
    stlib.numerics.vec3
    stlib.numerics.quat
    :members:


"""

import numpy.linalg
import SofaPython.Quaternion as Quaternion
from SofaPython.Quaternion import from_euler, to_matrix
from math import pi

def vadd(a,b):
    return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

def vvadd(a,b):
    return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

def vvsub(a,b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]

def vsadd(a,b):
    return [a[0]+b, a[1]+b, a[2]+b]

def vssub(a,b):
    return [a[0]-b, a[1]-b, a[2]-b]

def vsmul(a,b):
    return [a[0]*b, a[1]*b, a[2]*b]



def to_radians(v):
    if isinstance(v, list):
        p = []
        for tp in v:
            p.append( tp * pi * 2.0 / 360.0 )
        return p
    return v * pi * 2.0 / 360.0

def TRS_to_matrix(translation, rotation=None, scale=None, eulerRotation=None):
    t = numpy.identity(4)
    s = numpy.identity(4)
    if eulerRotation != None:
        rotation = from_euler( to_radians( eulerRotation ) )

    if scale == None:
        scale = [1.0,1.0,1.0]

    r = to_matrix( rotation )

    rr = numpy.identity(4)
    rr[0:3, 0:3] = r

    t[0,3]=translation[0]
    t[1,3]=translation[1]
    t[2,3]=translation[2]

    s[0,0]=scale[0]
    s[1,1]=scale[1]
    s[2,2]=scale[2]

    return numpy.matmul( numpy.matmul(t,rr), s )

def transformPositions(position, translation=[0.0,0.0,0.0], eulerRotation=[0.0,0.0,0.0], scale=[1.0,1.0,1.0]):

    trs = TRS_to_matrix(translation=translation, eulerRotation=eulerRotation, scale=scale)
    tp = []
    for point in position:
        tp.append(transformPosition(point, trs).tolist())

    return tp

def transformPosition(point, matrixTRS):

    if len(point) != 3:
        raise Exception('A Point is defined by 3 coordinates [X,Y,Z] , point given : '+str(point))

    elif all(isinstance(n, int) or isinstance(n, float) for n in point):
        np = numpy.matmul( matrixTRS, numpy.append(point,1.0) )
        tp = np[0:3]

    else :
        raise Exception('A Point is a list/array of int/float, point given : '+str(point))


    return tp

class Transform(object):
    def __init__(self, translation, orientation=None, eulerRotation=None):
        self.translation = translation

        if eulerRotation != None:
            self.orientation = from_euler( to_radians( eulerRotation ) )
        elif orientation != None:
            self.orientation = orientation
        else:
            self.orientation = [0,0,0,1]


    def toSofaRepr(self):
            return self.translation + list(self.orientation)

    def getForward(self):
        return numpy.matmul(TRS_to_matrix([0.0,0.0,0.0], self.orientation), numpy.array([5.0,0.0,0.0,1.0]))

    forward = property(getForward, None)

def axisToQuat(axis, angle):
    na  = numpy.zeros(3)
    na[0] = axis[0]
    na[1] = axis[1]
    na[2] = axis[2]
    return list(Quaternion.axisToQuat(na, angle))
