import unittest

from zope.interface import implementedBy
from zope.registry import ComponentLookupError

class Test(unittest.TestCase):

    def setUp(self):
        from zope import registry
        self.components = registry.Components('comps')
        self.tests = registry.tests

    def test_register_and_unregister_adapter(self):
        self.components.registerAdapter(self.tests.A12_1)

        multi_adapter = self.components.getMultiAdapter((self.tests.U1(1), self.tests.U12(2)), self.tests.IA1)
        self.assertEqual(multi_adapter.__class__, self.tests.A12_1)
        self.assertEqual(repr(multi_adapter), 'A12_1(U1(1), U12(2))')

        self.assertTrue(self.components.unregisterAdapter(self.tests.A12_1))
        self.assertRaises(ComponentLookupError, self.components.getMultiAdapter, (self.tests.U1(1), self.tests.U12(2)), self.tests.IA1)

    def test_register_and_unregister_adapter_with_two_interfaces(self):
        self.assertRaises(TypeError, self.components.registerAdapter, self.tests.A1_12)
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2)

        test_object = self.tests.U1(1)
        multi_adapter = self.components.getMultiAdapter((self.tests.U1(1),), self.tests.IA2)
        self.assertEqual(multi_adapter.__class__, self.tests.A1_12)
        self.assertEqual(repr(multi_adapter), 'A1_12(U1(1))')

        self.assertRaises(TypeError, self.components.unregisterAdapter, self.tests.A1_12)
        self.assertTrue(self.components.unregisterAdapter(self.tests.A1_12, provided=self.tests.IA2))
        self.assertRaises(ComponentLookupError, self.components.getMultiAdapter, (self.tests.U1(1),), self.tests.IA2)

    def test_register_and_unregister_adapter_with_no_interfaces(self):
        self.assertRaises(TypeError, self.components.registerAdapter, self.tests.A12_)

        self.components.registerAdapter(self.tests.A12_, provided=self.tests.IA2)
        multi_adapter = self.components.getMultiAdapter((self.tests.U1(1), self.tests.U12(2)), self.tests.IA2)
        self.assertEqual(multi_adapter.__class__, self.tests.A12_)
        self.assertEqual(repr(multi_adapter), 'A12_(U1(1), U12(2))')

        self.assertRaises(TypeError, self.components.unregisterAdapter, self.tests.A12_)
        self.assertTrue(self.components.unregisterAdapter(self.tests.A12_, provided=self.tests.IA2))
        self.assertRaises(ComponentLookupError, self.components.getMultiAdapter, (self.tests.U1(1), self.tests.U12(2)), self.tests.IA2)

    def test_register_and_unregister_adapter_with_no___component_adapts___attribute(self):
        self.assertRaises(TypeError, self.components.registerAdapter, self.tests.A_2)
        self.components.registerAdapter(self.tests.A_2, required=[self.tests.I3])
        self.assertTrue(self.components.unregisterAdapter(self.tests.A_2, required=[self.tests.I3]))

    def test_register_and_unregister_class_specific(self):
        self.components.registerAdapter(self.tests.A_3, required=[self.tests.U], info=u'Really class specific')
        self.assertTrue(self.components.unregisterAdapter(required=[self.tests.U], provided=self.tests.IA3))
      
    def test_registered_adapters_and_sorting(self):
        self.components.registerAdapter(self.tests.A12_1)
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerAdapter(self.tests.A12_, provided=self.tests.IA2)
        self.components.registerAdapter(self.tests.A_2, required=[self.tests.I3])
        self.components.registerAdapter(self.tests.A_3, required=[self.tests.U], info=u'Really class specific')

        sorted_adapters = sorted(self.components.registeredAdapters())
        sorted_adapters_name = map(lambda x: getattr(x, 'name'), sorted_adapters)
        sorted_adapters_provided = map(lambda x: getattr(x, 'provided'), sorted_adapters) 
        sorted_adapters_required = map(lambda x: getattr(x, 'required'), sorted_adapters)
        sorted_adapters_info = map(lambda x: getattr(x, 'info'), sorted_adapters)

        self.assertEqual(len(sorted_adapters), 5)
        self.assertEqual(sorted_adapters_name, [u'', u'', u'', u'', u''])
        self.assertEqual(sorted_adapters_provided, [self.tests.IA1,
                                                    self.tests.IA2,
                                                    self.tests.IA2,
                                                    self.tests.IA2,
                                                    self.tests.IA3])

        self.assertEqual(sorted_adapters_required, [(self.tests.I1, self.tests.I2),
                                                    (self.tests.I1, self.tests.I2),
                                                    (self.tests.I1,),
                                                    (self.tests.I3,),
                                                    (implementedBy(self.tests.U),)])
        self.assertEqual(sorted_adapters_info, [u'', u'', u'', u'', u'Really class specific'])

    def test_get_none_existing_adapter(self):
        self.assertRaises(ComponentLookupError, self.components.getMultiAdapter, (self.tests.U(1),), self.tests.IA1)

    def test_query_none_existing_adapter(self):
        self.assertTrue(self.components.queryMultiAdapter((self.tests.U(1),), self.tests.IA1) is None)
        self.assertEqual(self.components.queryMultiAdapter((self.tests.U(1),), self.tests.IA1, default=42), 42)

    def test_unregister_none_existing_adapter(self):
        self.assertFalse(self.components.unregisterAdapter(self.tests.A_2, required=[self.tests.I3]))
        self.assertFalse(self.components.unregisterAdapter(self.tests.A12_1, required=[self.tests.U]))

    def test_unregister_adapter(self):
        self.components.registerAdapter(self.tests.A12_1)
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerAdapter(self.tests.A12_, provided=self.tests.IA2)
        self.components.registerAdapter(self.tests.A_2, required=[self.tests.I3])
        self.components.registerAdapter(self.tests.A_3, required=[self.tests.U], info=u'Really class specific')

        self.assertTrue(self.components.unregisterAdapter(self.tests.A12_1))
        self.assertTrue(self.components.unregisterAdapter(required=[self.tests.U], provided=self.tests.IA3))

        sorted_adapters = sorted(self.components.registeredAdapters())
        sorted_adapters_name = map(lambda x: getattr(x, 'name'), sorted_adapters)
        sorted_adapters_provided = map(lambda x: getattr(x, 'provided'), sorted_adapters) 
        sorted_adapters_required = map(lambda x: getattr(x, 'required'), sorted_adapters)
        sorted_adapters_info = map(lambda x: getattr(x, 'info'), sorted_adapters)

        self.assertEqual(len(sorted_adapters), 3)
        self.assertEqual(sorted_adapters_name, [u'', u'', u''])
        self.assertEqual(sorted_adapters_provided, [self.tests.IA2,
                                                    self.tests.IA2,
                                                    self.tests.IA2])
        self.assertEqual(sorted_adapters_required, [(self.tests.I1, self.tests.I2),
                                                    (self.tests.I1,),
                                                    (self.tests.I3,)])
        self.assertEqual(sorted_adapters_info, [u'', u'', u''])

    def test_register_named_adapter(self):
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2, name=u'test')
        self.assertTrue(self.components.queryMultiAdapter((self.tests.U1(1),), self.tests.IA2) is None)
        self.assertEqual(repr(self.components.queryMultiAdapter((self.tests.U1(1),), self.tests.IA2, name=u'test')), 'A1_12(U1(1))')

        self.assertTrue(self.components.queryAdapter(self.tests.U1(1), self.tests.IA2) is None)
        self.assertEqual(repr(self.components.queryAdapter(self.tests.U1(1), self.tests.IA2, name=u'test')), 'A1_12(U1(1))')
        self.assertEqual(repr(self.components.getAdapter(self.tests.U1(1), self.tests.IA2, name=u'test')), 'A1_12(U1(1))')

    def test_get_adapters(self):
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA1, name=u'test 1')
        self.components.registerAdapter(self.tests.A1_23, provided=self.tests.IA2, name=u'test 2')
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2)

        adapters = list(self.components.getAdapters((self.tests.U1(1),), self.tests.IA2))
        self.assertEqual(len(adapters), 2)
        self.assertEqual(adapters[0][0], u'test 2')
        self.assertEqual(adapters[1][0], u'')
        self.assertEqual(repr(adapters[0][1]), 'A1_23(U1(1))')
        self.assertEqual(repr(adapters[1][1]), 'A1_12(U1(1))')

    def test_register_no_factory(self):
        self.components.registerAdapter(self.tests.A1_12, provided=self.tests.IA2)
        self.components.registerAdapter(self.tests.noop, 
                                        required=[self.tests.IA1], provided=self.tests.IA2, 
                                        name=u'test noop')

        self.assertTrue(self.components.queryAdapter(self.tests.U1(9), self.tests.IA2, name=u'test noop') is None)
        adapters = list(self.components.getAdapters((self.tests.U1(1),), self.tests.IA2))
        self.assertEqual(len(adapters), 1)
        self.assertEqual(adapters[0][0], u'')
        self.assertEqual(repr(adapters[0][1]), 'A1_12(U1(1))')

        self.assertTrue(self.components.unregisterAdapter(self.tests.A1_12, provided=self.tests.IA2))

        sorted_adapters = sorted(self.components.registeredAdapters())
        sorted_adapters_name = map(lambda x: getattr(x, 'name'), sorted_adapters)
        sorted_adapters_provided = map(lambda x: getattr(x, 'provided'), sorted_adapters) 
        sorted_adapters_required = map(lambda x: getattr(x, 'required'), sorted_adapters)
        sorted_adapters_info = map(lambda x: getattr(x, 'info'), sorted_adapters)

        self.assertEqual(len(sorted_adapters), 1)
        self.assertEqual(sorted_adapters_name, [u'test noop'])
        self.assertEqual(sorted_adapters_provided, [self.tests.IA2])
        self.assertEqual(sorted_adapters_required, [(self.tests.IA1,)])
        self.assertEqual(sorted_adapters_info, [u''])


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(Test),))

if __name__ == '__main__':
    main(defaultTest='test_suite')
