import unittest

class Test(unittest.TestCase):

    def setUp(self):
        from zope import registry
        self.components = registry.Components('comps')
        self.tests = registry.tests

    def test_register_utility(self):
        test_object = self.tests.U1(1)
        self.components.registerUtility(test_object)
        self.assertEqual(self.components.getUtility(self.tests.I1), test_object)

    def test_register_utility_with_factory(self):
        test_object = self.tests.U1(1)
        def factory():
           return test_object
        self.components.registerUtility(factory=factory)
        self.assertEqual(self.components.getUtility(self.tests.I1), test_object)
        self.assertTrue(self.components.unregisterUtility(factory=factory))

    def test_register_utility_with_component_and_factory(self):
        def factory():
            return self.tests.U1(1)
        self.assertRaises(TypeError, self.components.registerUtility, self.tests.U1(1), factory=factory)

    def test_unregister_utility_with_and_without_component_and_factory(self):
        def factory():
            return self.tests.U1(1)
        self.assertRaises(TypeError, self.components.unregisterUtility, self.tests.U1(1), factory=factory)
        self.assertRaises(TypeError, self.components.unregisterUtility)

    def test_register_utility_with_no_interfaces(self):
        self.assertRaises(TypeError, self.components.registerUtility, self.tests.A)

    def test_register_utility_with_two_interfaces(self):
        self.assertRaises(TypeError, self.components.registerUtility, self.tests.U12(1))

    def test_register_utility_with_arguments(self):
        test_object1 = self.tests.U12(1)
        test_object2 = self.tests.U12(2)
        self.components.registerUtility(test_object1, self.tests.I2)
        self.components.registerUtility(test_object2, self.tests.I2, 'name')
        self.assertEqual(self.components.getUtility(self.tests.I2), test_object1)
        self.assertEqual(self.components.getUtility(self.tests.I2, 'name'), test_object2)

    def test_get_none_existing_utility(self):
        from zope.registry import ComponentLookupError
        self.assertRaises(ComponentLookupError, self.components.getUtility, self.tests.I3)

    def test_query_none_existing_utility(self):
        self.assertTrue(self.components.queryUtility(self.tests.I3) is None)
        self.assertEqual(self.components.queryUtility(self.tests.I3, default=42), 42)

    def test_registered_utilities_and_sorting(self):
        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)
        test_object3 = self.tests.U12(3)
        self.components.registerUtility(test_object1)
        self.components.registerUtility(test_object3, self.tests.I2, u'name')
        self.components.registerUtility(test_object2, self.tests.I2)

        sorted_utilities = sorted(self.components.registeredUtilities())
        sorted_utilities_name = map(lambda x: getattr(x, 'name'), sorted_utilities)
        sorted_utilities_component = map(lambda x: getattr(x, 'component'), sorted_utilities)
        sorted_utilities_provided = map(lambda x: getattr(x, 'provided'), sorted_utilities)

        self.assertEqual(len(sorted_utilities), 3)
        self.assertEqual(sorted_utilities_name, [u'', u'', u'name'])
        self.assertEqual(sorted_utilities_component, [test_object1, test_object2, test_object3])
        self.assertEqual(sorted_utilities_provided, [self.tests.I1, self.tests.I2, self.tests.I2])

    def test_duplicate_utility(self):
        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)
        test_object3 = self.tests.U12(3)
        test_object4 = self.tests.U1(4)
        self.components.registerUtility(test_object1)
        self.components.registerUtility(test_object2, self.tests.I2)
        self.components.registerUtility(test_object3, self.tests.I2, u'name')
        self.assertEqual(self.components.getUtility(self.tests.I1), test_object1)

        self.components.registerUtility(test_object4, info=u'use 4 now')
        self.assertEqual(self.components.getUtility(self.tests.I1), test_object4)

    def test_unregister_utility(self):
        test_object = self.tests.U1(1)
        self.components.registerUtility(test_object)
        self.assertEqual(self.components.getUtility(self.tests.I1), test_object)
        self.assertTrue(self.components.unregisterUtility(provided=self.tests.I1))
        self.assertFalse(self.components.unregisterUtility(provided=self.tests.I1))

    def test_unregister_utility_extended(self):
        test_object = self.tests.U1(1)
        self.components.registerUtility(test_object)
        self.assertFalse(self.components.unregisterUtility(self.tests.U1(1)))
        self.assertEqual(self.components.queryUtility(self.tests.I1), test_object)
        self.assertTrue(self.components.unregisterUtility(test_object))
        self.assertTrue(self.components.queryUtility(self.tests.I1) is None)

    def test_get_utilities_for(self):
        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)
        test_object3 = self.tests.U12(3)
        self.components.registerUtility(test_object1)
        self.components.registerUtility(test_object2, self.tests.I2)
        self.components.registerUtility(test_object3, self.tests.I2, u'name')

        sorted_utilities = sorted(self.components.getUtilitiesFor(self.tests.I2))
        self.assertEqual(len(sorted_utilities), 2)
        self.assertEqual(sorted_utilities[0], (u'', test_object2))
        self.assertEqual(sorted_utilities[1], (u'name', test_object3))

    def test_get_all_utilities_registered_for(self):
        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)
        test_object3 = self.tests.U12(3)
        test_object4 = self.tests.U('ext')
        self.components.registerUtility(test_object1)
        self.components.registerUtility(test_object2, self.tests.I2)
        self.components.registerUtility(test_object3, self.tests.I2, u'name')
        self.components.registerUtility(test_object4, self.tests.I2e)

        sorted_utilities = sorted(self.components.getUtilitiesFor(self.tests.I2))
        self.assertEqual(len(sorted_utilities), 2)
        self.assertEqual(sorted_utilities[0], (u'', test_object2))
        self.assertEqual(sorted_utilities[1], (u'name', test_object3))

        all_utilities = self.components.getAllUtilitiesRegisteredFor(self.tests.I2)
        self.assertEqual(len(all_utilities), 3)
        self.assertTrue(test_object2 in all_utilities)
        self.assertTrue(test_object3 in all_utilities)
        self.assertTrue(test_object4 in all_utilities)

        self.assertTrue(self.components.unregisterUtility(test_object4, self.tests.I2e))
        self.assertEqual(self.components.getAllUtilitiesRegisteredFor(self.tests.I2e), [])

    def test_utility_events(self):
        from zope.event import subscribers
        old_subscribers = subscribers[:]
        subscribers[:] = []

        test_object = self.tests.U1(1)
        def log_event(event):
            self.assertEqual(event.object.component, test_object)
        subscribers.append(log_event)
        self.components.registerUtility(test_object)

        subscribers[:] = old_subscribers

    def test_dont_leak_utility_registrations_in__subscribers(self):
        """
        We've observed utilities getting left in _subscribers when they
        get unregistered.

        """
        class C:
            def __init__(self, name):
                self.name = name
            def __repr__(self):
                return "C(%s)" % self.name

        c1 = C(1)
        c2 = C(2)

        self.components.registerUtility(c1, self.tests.I1)
        self.components.registerUtility(c1, self.tests.I1)
        utilities = list(self.components.getAllUtilitiesRegisteredFor(self.tests.I1))
        self.assertEqual(len(utilities), 1)
        self.assertEqual(utilities[0], c1)

        self.assertTrue(self.components.unregisterUtility(provided=self.tests.I1))
        utilities = list(self.components.getAllUtilitiesRegisteredFor(self.tests.I1))
        self.assertEqual(len(utilities), 0)

        self.components.registerUtility(c1, self.tests.I1)
        self.components.registerUtility(c2, self.tests.I1)

        utilities = list(self.components.getAllUtilitiesRegisteredFor(self.tests.I1))
        self.assertEqual(len(utilities), 1)
        self.assertEqual(utilities[0], c2)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(Test),))

if __name__ == '__main__':
    main(defaultTest='test_suite')
