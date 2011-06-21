import unittest

class Test(unittest.TestCase):

    def setUp(self):
        from zope import registry
        self.components = registry.Components('comps')
        self.tests = registry.tests

    def test_register_subscriber(self):
        self.components.registerSubscriptionAdapter(self.tests.A1_2)
        self.components.registerSubscriptionAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2, info='a sample comment')
        subscribers = self.components.subscribers((self.tests.U1(1),), self.tests.IA2)
        self.assertEqual(len(subscribers), 3)
        self.assertEqual(repr(subscribers[0]), 'A1_2(U1(1))')
        self.assertEqual(repr(subscribers[1]), 'A1_12(U1(1))')
        self.assertEqual(repr(subscribers[2]), 'A(U1(1),)') 

    def test_register_noncompliant_subscriber(self):
        self.assertRaises(TypeError, self.components.registerSubscriptionAdapter, self.tests.A1_12)
        self.assertRaises(TypeError, self.components.registerSubscriptionAdapter, self.tests.A)
        self.assertRaises(TypeError, self.components.registerSubscriptionAdapter, self.tests.A, required=[self.tests.IA1])

    def test_register_named_subscriber(self):
        self.components.registerSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2, u'', u'a sample comment')
        self.assertRaises(TypeError, self.components.registerSubscriptionAdapter, 
                          self.tests.A, [self.tests.I1], self.tests.IA2, u'oops', u'a sample comment')
        subscribers = self.components.subscribers((self.tests.U1(1),), self.tests.IA2)
        self.assertEqual(len(subscribers), 1)
        self.assertEqual(repr(subscribers[0]), 'A(U1(1),)')

    def test_register_no_factory(self):
        self.components.registerSubscriptionAdapter(self.tests.noop, [self.tests.I1], self.tests.IA2)
        subscribers = self.components.subscribers((self.tests.U1(1),), self.tests.IA2)
        self.assertEqual(len(subscribers), 0)

    def test_sorting_registered_subscription_adapters(self):
        self.components.registerSubscriptionAdapter(self.tests.A1_2)
        self.components.registerSubscriptionAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2, info=u'a sample comment')
        self.components.registerSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2, u'', u'a sample comment')
        self.components.registerSubscriptionAdapter(self.tests.noop, [self.tests.I1], self.tests.IA2)

        sorted_subscribers = sorted(self.components.registeredSubscriptionAdapters())
        sorted_subscribers_name = map(lambda x: getattr(x, 'name'), sorted_subscribers)
        sorted_subscribers_provided = map(lambda x: getattr(x, 'provided'), sorted_subscribers) 
        sorted_subscribers_required = map(lambda x: getattr(x, 'required'), sorted_subscribers)
        sorted_subscribers_factory = map(lambda x: getattr(x, 'factory'), sorted_subscribers)
        sorted_subscribers_info = map(lambda x: getattr(x, 'info'), sorted_subscribers)

        self.assertEqual(len(sorted_subscribers), 5)
        self.assertEqual(sorted_subscribers_name, [u'', u'', u'', u'', u''])
        self.assertEqual(sorted_subscribers_provided, [self.tests.IA2, self.tests.IA2, self.tests.IA2, self.tests.IA2, self.tests.IA2])
        self.assertEqual(sorted_subscribers_required, [(self.tests.I1,), (self.tests.I1,), (self.tests.I1,),(self.tests.I1,), (self.tests.I1,)])
        self.assertEqual(sorted_subscribers_factory, [self.tests.A, self.tests.A, self.tests.A1_12, self.tests.A1_2, self.tests.noop])
        self.assertEqual(sorted_subscribers_info, [u'a sample comment', u'a sample comment', u'', u'', u''])

    def test_unregister(self):
        self.components.registerSubscriptionAdapter(self.tests.A1_2)
        self.assertEqual(len(self.components.subscribers((self.tests.U1(1),), self.tests.IA2)), 1)
        self.assertTrue(self.components.unregisterSubscriptionAdapter(self.tests.A1_2))
        self.assertEqual(len(self.components.subscribers((self.tests.U1(1),), self.tests.IA2)), 0)

    def test_unregister_multiple(self):
        self.components.registerSubscriptionAdapter(self.tests.A1_2)
        self.components.registerSubscriptionAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2, info=u'a sample comment')
        self.components.registerSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2, u'', u'a sample comment')
        self.components.registerSubscriptionAdapter(self.tests.noop, [self.tests.I1], self.tests.IA2)
        self.assertEqual(len(self.components.subscribers((self.tests.U1(1),), self.tests.IA2)), 4)
        self.assertEqual(len(list(self.components.registeredSubscriptionAdapters())), 5)

        self.assertTrue(self.components.unregisterSubscriptionAdapter(self.tests.A, [self.tests.I1], self.tests.IA2))
        self.assertEqual(len(self.components.subscribers((self.tests.U1(1),), self.tests.IA2)), 2)
        self.assertEqual(len(list(self.components.registeredSubscriptionAdapters())), 3)

    def test_unregister_no_factory(self):
        self.components.registerSubscriptionAdapter(self.tests.A1_2)
        self.components.registerSubscriptionAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerSubscriptionAdapter(self.tests.noop, [self.tests.I1], self.tests.IA2)
        self.assertEqual(len(self.components.subscribers((self.tests.U1(1),), self.tests.IA2)), 2)
        self.assertEqual(len(list(self.components.registeredSubscriptionAdapters())), 3)

        self.assertRaises(TypeError, self.components.unregisterSubscriptionAdapter, required=[self.tests.I1])
        self.assertRaises(TypeError, self.components.unregisterSubscriptionAdapter, provided=self.tests.IA2)
        self.assertTrue(self.components.unregisterSubscriptionAdapter(required=[self.tests.I1], provided=self.tests.IA2))
        self.assertEqual(len(self.components.subscribers((self.tests.U1(1),), self.tests.IA2)), 0)
        self.assertEqual(len(list(self.components.registeredSubscriptionAdapters())), 0)

    def test_unregister_noncompliant_subscriber(self):
        self.assertRaises(TypeError, self.components.unregisterSubscriptionAdapter, self.tests.A1_12)
        self.assertRaises(TypeError, self.components.unregisterSubscriptionAdapter, self.tests.A)
        self.assertRaises(TypeError, self.components.unregisterSubscriptionAdapter, self.tests.A, required=[self.tests.IA1])

    def test_unregister_nonexistent_subscriber(self):
        self.assertFalse(self.components.unregisterSubscriptionAdapter(required=[self.tests.I1], provided=self.tests.IA2))


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(Test),))

if __name__ == '__main__':
    main(defaultTest='test_suite')       
