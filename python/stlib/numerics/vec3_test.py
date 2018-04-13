import unittest
from vec3 import *

class Vec3_test(unittest.TestCase):

    def test_equal(self):
        v1 = Vec3(0.)
        v2 = Vec3(1.)
        self.assertEqual(v1,v1)
        self.assertNotEqual(v1,v2)

        self.assertEqual(v1,[0.,0.,0.])
        self.assertNotEqual(v1,[1.,1.,1.])

    def test_constructors(self):
        v = Vec3()
        self.assertTrue(len(v),3)
        self.assertEqual(v, [0.,0.,0.])
        v = Vec3(1.)
        self.assertEqual(v, [1.,1.,1.])
        v = Vec3(1.,2.,3.)
        self.assertEqual(v, [1.,2.,3.])
        v = Vec3([1.,2.,3.])
        self.assertEqual(v, [1.,2.,3.])
        v1 = Vec3(2,2,2)
        v = Vec3(v1)
        self.assertEqual(v, v1)

        # If args are not expected should print the doc
        # v = Vec3(1,2)

    def test_norm(self):
        v = Vec3(1.,2.,2.)
        self.assertEqual(v.norm(), 3.)

    def test_normalize(self):
        v = Vec3(1.,2.,2.)
        v.normalize()
        self.assertEqual(v, [1./3.,2./3.,2./3.])

    def test_translate(self):
        v = Vec3()
        v.translate(1.)
        self.assertEqual(v, [1.,1.,1.])
        v.translate(1.,2.,3.)
        self.assertEqual(v, [2.,3.,4.])
        v.translate([1.,2.,3.])
        self.assertEqual(v, [3.,5.,7.])

        # If args are not expected should print the doc
        # v.translate(1,2)

    def test_scale(self):
        v = Vec3(1.,1.,1.)
        v.scale(2.)
        self.assertEqual(v, [2.,2.,2.])
        v.scale(1.,2.,3.)
        self.assertEqual(v, [2.,4.,6.])
        v.scale([1.,2.,3.])
        self.assertEqual(v, [2.,8.,18.])

        # If args are not expected should print the doc
        # v.scale(2,1)

    def test_dot(self):
        v = Vec3(1.,1.,1.)
        s = v.dot(1.,2.,3.)
        self.assertEqual(s,6)
        s = v.dot([1.,2.,3.])
        self.assertEqual(s,6)

        # If args are not expected should print the doc
        # v.dot(2,1)

    def test_cross(self):
        v = Vec3(1.,1.,1.)
        u = Vec3(1.,2.,3.)
        self.assertEqual(v.cross(u),[1.,-2.,1.])
        self.assertEqual(u.cross(v),[-1.,2.,-1.])

        # If args are not expected should print the doc
        # v.cross(2,1)


if __name__ == '__main__':
    unittest.main()
