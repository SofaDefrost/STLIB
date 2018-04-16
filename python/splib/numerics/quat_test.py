import unittest
from math import sin, cos, pi
from quat import *

class Quat_test(unittest.TestCase):


    def test_equal(self):
        q1 = Quat()
        q2 = Quat(0.707,0.,0.,0.707)
        self.assertEqual(q1,q1)
        self.assertNotEqual(q1,q2)

        self.assertEqual(q1,[0.,0.,0.,1.])
        self.assertNotEqual(q1,[0.707,0.,0.,0.707])


    def test_constructors(self):
        q = Quat()
        self.assertEqual(q,[0.,0.,0.,1.])

        q = Quat(0.707,0.,0.,0.707)
        self.assertEqual(q,[0.707,0.,0.,0.707])

        q = Quat([0.707,0.,0.,0.707])
        self.assertEqual(q,[0.707,0.,0.,0.707])


## PUBLICS METHODS


    def test_norm(self):
        q = Quat()
        self.assertEqual(q.norm(), 1.)


    def test_normalize(self):
        q = Quat(1.,0.,2.,2.)
        q.normalize()
        self.assertEqual(q, [1./3.,0.,2./3.,2./3.])


    def test_realPart(self):
        q = Quat()
        self.assertEqual(q.re(), 1.)


    def test_imaginaryPart(self):
        q = Quat()
        self.assertEqual(q.im(), [0.,0.,0.])


## STATIC METHODS


    def test_createFromAxisAngle(self):
        q = Quat.createFromAxisAngle([1.,0.,0.],pi/2.)
        self.assertEqual(q, [sin(pi/4.),0.,0.,cos(pi/4.)])


    def test_conjugate(self):
        q = Quat()
        self.assertEqual(Quat.conjugate(q), q)

        q = Quat(0.5,0.5,0.5,0.5)
        self.assertEqual(Quat.conjugate(q), [-0.5,-0.5,-0.5,0.5])


    def test_inverse(self):
        q = Quat()
        self.assertEqual(Quat.inverse(q), q)

        q = Quat(0.5,0.5,0.5,0.5)
        self.assertEqual(Quat.inverse(q), Quat.conjugate(q))

        q = Quat(1.,1.,1.,1.)
        self.assertEqual(Quat.inverse(q),[-0.25,-0.25,-0.25,0.25])


    def test_angle(self):
        q = Quat()
        self.assertEqual(Quat.angle(q), 0)

        q = Quat(sin(pi/4.),0.,0.,cos(pi/4.))
        self.assertEqual(Quat.angle(q), pi/2.)


if __name__ == '__main__':
    unittest.main()
