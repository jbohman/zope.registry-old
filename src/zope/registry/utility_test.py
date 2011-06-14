import unittest

class Test_utility(unittest.TestCase):

    def setUp(self):
        from zope import registry
        self.components = registry.Components('comps')

        from zope.event import subscribers
        self._old_subscribers = subscribers[:]
        subscribers[:] = []
        self.dummy = []
        subscribers.append(self.log_event)

    def log_event(self, event):
        self.dummy.append(event)

    def tearDown(self):
        from zope.event import subscribers
        subscribers[:] = self._old_subscribers

    def test_register_utility(self):
        from zope.registry import tests
        self.components.registerUtility(tests.U1(1))
        self.assertEqual(self.dummy[0].__class__.__name__, 'Registered')
        self.assertEqual(repr(self.dummy[0].object), "UtilityRegistration(<Components comps>, I1, u'', 1, None, u'')")
        self.assertEqual(repr(self.components.getUtility(tests.I1)), repr(tests.U1(1)))

        def factory():
           return tests.U1(1)
        self.components.registerUtility(factory=factory)

        self.assertEqual(self.dummy[1].__class__.__name__, 'Unregistered')
        self.assertEqual(repr(self.dummy[1].object), "UtilityRegistration(<Components comps>, I1, u'', 1, None, u'')")
        self.assertEqual(self.dummy[2].__class__.__name__, 'Registered')
        self.assertRegexpMatches(repr(self.dummy[2].object), r"UtilityRegistration\(<Components comps>, I1, u'', 1, <function factory at .+>, u''\)")
