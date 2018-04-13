import numpy

class Vec3(numpy.ndarray):


    def __new__(cls, *args):
        """ Vec3 constructor expects zero, one or three arguments.
        Example:
        vec3(1.) will return [1.,1.,1.]
        vec3(1,2,3) will return [1,2,3]
        Default vec3() will return [0.,0.,0]
        """
        if len(args)==0:
            return super(Vec3,cls).__new__(cls, shape=(3,), dtype=float, buffer=numpy.array([0.,0.,0.]))
        elif len(args)==1:
            return super(Vec3,cls).__new__(cls, shape=(3,), dtype=float, buffer=numpy.array([args[0],args[0],args[0]]))
        elif len(args)==3:
            return super(Vec3,cls).__new__(cls, shape=(3,), dtype=float, buffer=numpy.array([args[0],args[1],args[2]]))

        print(cls.__new__.__doc__)
        return super(Vec3,cls).__new__(cls, shape=(3,), dtype=float, buffer=numpy.array([args[0],args[0],args[0]]))


    def __eq__(self, other):
        """ Vec3 overriding of __eq__ so that it returns a boolean."""
        results = (super(Vec3,self).__eq__(other))
        for result in results:
            if result == False:
                return False
        return True


    def __ne__(self, other):
        """ Vec3 overriding of __ne__ so that it returns a boolean."""
        results = (super(Vec3,self).__ne__(other))
        for result in results:
            if result == False:
                return False
        return True


    def translate(self, *args):
        """ Function translate of class Vec3 expects one or three arguments.
        Example: if v = [0.,0.,0.]
        v.translate(1.) will set v = [1.,1.,1.]
        v.translate(1,2,3) will set v = [1,2,3]
        v.translate([1,2,3]) will set v = [1,2,3]
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


    def scale(self, *args):
        """ Function scale of class Vec3 expects one or three arguments.
        Example: if v = [1.,2.,3.]
        v.scale(2.) will set v = [2.,4.,6.]
        v.scale(1,2,3) will set v = [1.,4.,9.]
        v.scale([1,2,3]) will set v = [1.,4.,9.]
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
        """ Function dot of class Vec3 computes the scalar product with the given vector. The function expects one or three arguments.
        Example: if v = [1.,1.,1.]
        v.scale(1,2,3) will return 6
        v.scale([1,2,3]) will return 6
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


    # def cross(self, *args):
    # def rotate(self, *args):
    # def norm(self, *args):
    # def normalize(self, *args):
