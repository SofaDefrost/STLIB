import numpy
import math

def createQuatFromAxis(axis, angle):
    """ Function createQuatFromAxis from quat expects two arguments. Quat has the Sofa format i.e (x,y,z,w).
    Examples:
    createQuatFromAxis([1.,0.,0.],pi/2.) returns [0.707,0.,0.,0.707]
    Note that the angle should be in radian.
    """
    from quat import Quat
    q = Quat()
    q[0]=axis[0]*math.sin(angle/2.)
    q[1]=axis[1]*math.sin(angle/2.)
    q[2]=axis[2]*math.sin(angle/2.)
    q[3]=math.cos(angle/2.)

    q.normalize()
    return q

#combinaison of rotation: q.apply(q2) or something like that
#eulerToQuat
#quatToEuler

class Quat(numpy.ndarray):

    def __new__(cls, *args):
        """ Quat constructor expects zero or four arguments. Quat has the Sofa format i.e (x,y,z,w).
        Examples:
        Quat(0.,0.,0.,1.) will return [0.,0.,0.,1.]
        Quat([0.,0.,0.,1.]) will return [0.,0.,0.,1.]
        Default Quat() will return [0.,0.,0.,1.]
        """
        if len(args)==0:
            return super(Quat,cls).__new__(cls, shape=(4,), dtype=float, buffer=numpy.array([0.,0.,0.,1.]))
        elif hasattr(args[0],"__len__") and len(args[0])==4:
            return super(Quat,cls).__new__(cls, shape=(4,), dtype=float, buffer=numpy.array([args[0][0],args[0][1],args[0][2],args[0][3]]))
        elif len(args)==4:
            return super(Quat,cls).__new__(cls, shape=(4,), dtype=float, buffer=numpy.array([args[0],args[1],args[2],args[3]]))

        print(cls.__new__.__doc__)
        return super(Quat,cls).__new__(cls, shape=(4,), dtype=float, buffer=numpy.array([0.,0.,0.,1.]))


    def __eq__(self, other):
        """ Quat overriding of __eq__ so that it returns a boolean."""
        results = (super(Quat,self).__eq__(other))
        for result in results:
            if result == False:
                return False
        return True


    def __ne__(self, other):
        """ Quat overriding of __ne__ so that it returns a boolean."""
        return not (self == other)


    def norm(self, *args):
        """ Function norm of class Quat returns the norm of the vector. The function expects no argument.
        """
        return math.sqrt(self.dot(self))


    def normalize(self, *args):
        """ Function normalize of class Quat normalize the vector. The function expects no argument.
        """
        self /= self.norm()
