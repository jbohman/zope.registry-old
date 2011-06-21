import unittest

class Test(unittest.TestCase):

    def setUp(self):
        from zope import registry
        self.tests = registry.tests

    def test_extendning(self):
        from zope import registry

        c1 = registry.Components('1')
        self.assertEqual(c1.__bases__, ())

        c2 = registry.Components('2', (c1, ))
        self.assertTrue(c2.__bases__ == (c1, ))

        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U1(2)
        test_object3 = self.tests.U12(1)
        test_object4 = self.tests.U12(3)

        self.assertEqual(len(list(c1.registeredUtilities())), 0)
        self.assertEqual(len(list(c2.registeredUtilities())), 0)

        c1.registerUtility(test_object1)
        self.assertEqual(len(list(c1.registeredUtilities())), 1)
        self.assertEqual(len(list(c2.registeredUtilities())), 0)
        self.assertEqual(c1.queryUtility(self.tests.I1), test_object1)
        self.assertEqual(c2.queryUtility(self.tests.I1), test_object1)

        c1.registerUtility(test_object2)
        self.assertEqual(len(list(c1.registeredUtilities())), 1)
        self.assertEqual(len(list(c2.registeredUtilities())), 0)
        self.assertEqual(c1.queryUtility(self.tests.I1), test_object2)
        self.assertEqual(c2.queryUtility(self.tests.I1), test_object2)


        c3 = registry.Components('3', (c1, ))
        c4 = registry.Components('4', (c2, c3))
        self.assertEqual(c4.queryUtility(self.tests.I1), test_object2)
    
        c1.registerUtility(test_object3, self.tests.I2)
        self.assertEqual(c4.queryUtility(self.tests.I2), test_object3)

        c3.registerUtility(test_object4, self.tests.I2)
        self.assertEqual(c4.queryUtility(self.tests.I2), test_object4)

        @registry.adapter(self.tests.I1)
        def handle1(x):
            self.assertEqual(x, test_object1)

        def handle(*objects):
            self.assertEqual(objects, (test_object1,))

        @registry.adapter(self.tests.I1)
        def handle3(x):
            self.assertEqual(x, test_object1)

        @registry.adapter(self.tests.I1)
        def handle4(x):
            self.assertEqual(x, test_object1)

        c1.registerHandler(handle1, info=u'First handler')
        c2.registerHandler(handle, required=[self.tests.U])
        c3.registerHandler(handle3)
        c4.registerHandler(handle4)

        c4.handle(test_object1)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(Test),))

if __name__ == '__main__':
    main(defaultTest='test_suite')    
