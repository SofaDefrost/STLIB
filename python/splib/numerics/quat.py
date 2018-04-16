import numpy
import math

class Quat(numpy.ndarray):

    def __new__(cls, *args):
        """ Quat constructor expects zero, one, or four arguments. Quat has the Sofa format i.e (x,y,z,w).

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
        """ Quat overriding of __eq__ so that (q1==q2) returns a boolean.
        """
        results = (super(Quat,self).__eq__(other))
        for result in results:
            if result == False:
                return False
        return True


    def __ne__(self, other):
        """ Quat overriding of __ne__ so that (q1!=q2) returns a boolean.
        """
        return not (self == other)


    def norm(self, *args):
        """ Function norm of class Quat returns the norm of the vector. The function expects no argument.
        """
        return numpy.linalg.norm(self)


    def normalize(self, *args):
        """ Function normalize of class Quat normalize the vector. The function expects no argument.
        """
        self /= self.norm()


    def re(self):
        """Returns the real part of the Quat

        Example:
        q = Quat(0.65,0.,0.,0.75)
        q.re() returns 0.75
        """
        return self.take(3)


    def im(self):
        """Returns the imaginary part of the Quat.

        Example:
        q = Quat(0.65,0.,0.,0.75)
        q.im() returns [0.65,0.,0.]
        """
        return self.take(range(3))


    def apply(self, qb):
        """Function apply of class Quat combine the current Quat with the given one.

        Examples:
        qa.apply(x,y,z,w),
        qa.apply([x,y,z,w]),
        qa.apply(qb),
        will apply qb=[x,y,z,w] to qa
        """

        if qb != type(Quat):
            print("In function apply of class Quat, it is expected that qb is of type Quat")
            return

        # Here is a readable version :
        # array([ qa[3]*qb[0] + qb[3]*qa[0] + qa[1]*qb[2] - qa[2]*qb[1],
        # qa[3]*qb[1] + qb[3]*qa[1] + qa[2]*qb[0] - qa[0]*qb[2],
        # qa[3]*qb[2] + qb[3]*qa[2] + qa[0]*qb[1] - qa[1]*qb[0],
        # qa[3]*qb[3] - qb[0]*qa[0] - qa[1]*qb[1] - qa[2]*qb[2] ])
        self = numpy.hstack( (self.re()*qb.im() + qb.re()*self.im() + numpy.cross( self.im(), qb.im() ), [self.re() * qb.re() - numpy.dot( self.im(), qb.im())] ))


    @staticmethod
    def createFromAxisAngle(axis, angle):
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


    #@staticmethod
    #def createFromEuler(ax,ay,az)


    @staticmethod
    def product(a, b):
        """Use this product to compose the rotations represented by two quaterions.

        Here is a readable version :
        array([ qa[3]*qb[0] + qb[3]*qa[0] + qa[1]*qb[2] - qa[2]*qb[1],
        qa[3]*qb[1] + qb[3]*qa[1] + qa[2]*qb[0] - qa[0]*qb[2],
        qa[3]*qb[2] + qb[3]*qa[2] + qa[0]*qb[1] - qa[1]*qb[0],
        qa[3]*qb[3] - qb[0]*qa[0] - qa[1]*qb[1] - qa[2]*qb[2] ])
        """
        return hstack( (re(a)*im(b) + re(b)*im(a) + numpy.cross( im(a), im(b) ), [re(a) * re(b) - dot( im(a), im(b))] ))


    @staticmethod
    def angle(q):
        """Returns the angle in radian of a given Quat.
        """
        return 2.0* math.acos(q.re())


    #@staticmethod
    #def eulerRotation(q)


    @staticmethod
    def conjugate(q):
        """Returns the conjugate of a given Quat.
        """
        return Quat(-q[0],-q[1],-q[2],q[3])


    @staticmethod
    def inverse(q):
        """Returns the inverse of a given Quat.

        If you are dealing with unit quaternions, use getConjugate() instead.
        """
        return  Quat.conjugate(q) / q.norm()**2
