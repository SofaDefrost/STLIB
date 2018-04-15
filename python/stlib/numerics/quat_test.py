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

    def test_norm(self):
        q = Quat()
        self.assertEqual(q.norm(), 1.)

    def test_normalize(self):
        q = Quat(1.,0.,2.,2.)
        q.normalize()
        self.assertEqual(q, [1./3.,0.,2./3.,2./3.])

    def test_createQuatFromAxis(self):
        q = createQuatFromAxis([1.,0.,0.],pi/2.)
        self.assertEqual(q, [sin(pi/4.),0.,0.,cos(pi/4.)])



if __name__ == '__main__':
    unittest.main()
