import numpy
import math

class Vec3(numpy.ndarray):

    def __new__(cls, *args):
        """ Vec3 constructor expects zero, one or three arguments.

        Example:
        vec3(1.) will return [1.,1.,1.]
        vec3(1,2,3) will return [1,2,3]
        vec3([1,2,3]) will return [1,2,3]

        Default vec3() will return [0.,0.,0]
        """
        if len(args)==0:
            return super(Vec3,cls).__new__(cls, shape=(3,), dtype=float, buffer=numpy.array([0.,0.,0.]))
        if len(args) == 1:
            if hasattr(args[0],"__len__") and len(args[0])==3:
                return super(Vec3,cls).__new__(cls, shape=(3,), dtype=type(args[0][0]), buffer=numpy.array([args[0][0],args[0][1],args[0]][2]))
            else:
                return super(Vec3,cls).__new__(cls, shape=(3,), dtype=type(args[0]), buffer=numpy.array([args[0],args[0],args[0]]))
        elif len(args)==3:
            return super(Vec3,cls).__new__(cls, shape=(3,), dtype=type(args[0]), buffer=numpy.array([args[0],args[1],args[2]]))

        print(cls.__new__.__doc__)
        return super(Vec3,cls).__new__(cls, shape=(3,), dtype=float, buffer=numpy.array([args[0],args[0],args[0]]))


    def __eq__(self, other):
        """ Vec3 overriding of __eq__ so that (v1==v2) returns a boolean.
        """
        results = (super(Vec3,self).__eq__(other))
        for result in results:
            if result == False:
                return False
        return True


    def __ne__(self, other):
        """ Vec3 overriding of __ne__ so that (v1!=v2) returns a boolean.
        """
        return not (self == other)


    def norm(self, *args):
        """ Function norm of class Vec3 returns the norm of the vector. The function expects no argument.
        """
        return math.sqrt(self.dot(self))


    def normalize(self, *args):
        """ Function normalize of class Vec3 normalize the vector. The function expects no argument.
        """
        self /= self.norm()


    def translate(self, *args):
        """ Function translate of class Vec3 expects one or three arguments. Note that you can also use the '+' and '-' operators.

        Example: if v = Vec3([0.,0.,0.])
        v.translate(1.) will set v = [1.,1.,1.]
        v.translate(1.,2.,3.) will set v = [1.,2.,3.]
        v.translate([1.,2.,3.]) will set v = [1.,2.,3.]
        """
        if len(args) == 1:
            if hasattr(args[0],"__len__") and len(args[0])==3:
                for i in range(0,3):
                    self.put(i,self.take(i)+args[0][i])
            else:
                for i in range(0,3):
                    self.put(i,self.take(i)+args[0])
        elif len(args) == 3:
            for i in range(0,3):
                self.put(i,self.take(i)+args[i])
        else:
            print(self.translate.__doc__)


    #def rotate(self, *args):
    #   from quat import Quat
    #   if len(args) == 1 and type(args[0]) == Quat:
    #       self.rotateFromQuat(args[0])
    #   elif ...


    #def rotateFromQuat():
    #   from quat import Quat

    #def rotateFromEuler():


    #def rotateFromAxisAndAngle(self, axis, angle):
    #   import quat.createQuatFromAxis
    #   q = createQuatFromAxis(axis, angle)
    #   self.rotateFromQuat(q)


    def scale(self, *args):
        """ Function scale of class Vec3 expects one or three arguments. Note that you can also use the '*' and '/' operators.

        Example: if v = Vec3([1.,2.,3.])
        v.scale(2.) will set v = [2.,4.,6.]
        v.scale(1.,2.,3.) will set v = [1.,4.,9.]
        v.scale([1.,2.,3.]) will set v = [1.,4.,9.]
        """
        if len(args) == 1:
            if hasattr(args[0],"__len__") and len(args[0])==3:
                for i in range(0,3):
                    self.put(i,self.take(i)*args[0][i])
            else:
                for i in range(0,3):
                    self.put(i,self.take(i)*args[0])
        elif len(args) == 3:
            for i in range(0,3):
                self.put(i,self.take(i)*args[i])
        else:
            print(self.scale.__doc__)


    def dot(self, *args):
        """ Function dot of class Vec3 returns the scalar product with the given vector. The function expects one or three arguments.

        Example: if v = Vec3([1.,1.,1.])
        v.dot(1.,2.,3.) will return 6.
        v.dot([1.,2.,3.]) will return 6.
        """
        s = 0
        if len(args) == 1 and hasattr(args[0],"__len__") and len(args[0])==3:
            for i in range(0,3):
                s += self.take(i)*args[0][i]
            return s
        elif len(args) == 3:
            for i in range(0,3):
                s += self.take(i)*args[i]
            return s
        else:
            print(self.dot.__doc__)


    def cross(self, *args):
        """ Function cross of class Vec3 returns the cross product with the given vector. The function expects one or three arguments.

        Example: if v = Vec3([1.,1.,1.])
        v.cross(1.,2.,3.) will return [1.,-2.,1.]
        v.cross([1.,2.,3.]) will return [1.,-2.,1.]
        """
        v = Vec3()
        u = Vec3()
        if len(args) == 1 and hasattr(args[0],"__len__") and len(args[0])==3:
            u = args[0]
        elif len(args) == 3:
            u = args
        else:
            print(self.cross.__doc__)

        v[0]=self.take(1)*u[2]-self.take(2)*u[1]
        v[1]=self.take(2)*u[0]-self.take(0)*u[2]
        v[2]=self.take(0)*u[1]-self.take(1)*u[0]
        return v
