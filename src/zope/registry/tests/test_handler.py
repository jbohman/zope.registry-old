import unittest

from zope.interface import implementedBy

class Test(unittest.TestCase):

    def setUp(self):
        from zope import registry
        self.components = registry.Components('comps')
        self.tests = registry.tests

    def test_register_handler(self):
        from zope import registry

        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)

        @registry.adapter(self.tests.I1)
        def handle1(x):
            self.assertEqual(x, test_object1)

        self.components.registerHandler(handle1, info=u'First handler')
        self.components.handle(test_object1)

        @registry.adapter(self.tests.I1, self.tests.I2)
        def handle12(x, y):
            self.assertEqual(x, test_object1)
            self.assertEqual(y, test_object2)

        self.components.registerHandler(handle12)
        self.components.handle(test_object1, test_object2)

    def test_register_noncompliant_handler(self):
        handle_calls = []
        def handle(*objects):
            handle_calls.append(objects)

        self.assertRaises(TypeError, self.components.registerHandler, handle)
        self.components.registerHandler(handle, required=[self.tests.I1], info=u'a comment')
        self.components.registerHandler(handle, required=[self.tests.U], info=u'handle a class')

        test_object = self.tests.U1(1)
        self.components.handle(test_object)
        self.assertEqual(len(handle_calls), 2)
        map(self.assertEqual, handle_calls, [(test_object,), (test_object,)])

    def test_list_handlers(self):
        from zope import registry

        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)

        @registry.adapter(self.tests.I1)
        def handle1(x):
            self.assertEqual(x, test_object1)

        @registry.adapter(self.tests.I1, self.tests.I2)
        def handle12(x, y):
            self.assertEqual(x, test_object1)
            self.assertEqual(y, test_object2)

        handle_calls = []
        def handle(*objects):
            handle_calls.append(objects)

        self.components.registerHandler(handle1, info=u'First handler')
        self.components.registerHandler(handle12)
        self.components.registerHandler(handle, required=[self.tests.I1], info=u'a comment')
        self.components.registerHandler(handle, required=[self.tests.U], info=u'handle a class')

        handlers = list(self.components.registeredHandlers())
        handlers_required = map(lambda x: getattr(x, 'required'), handlers)
        handlers_handler = map(lambda x: getattr(x, 'handler'), handlers)
        handlers_info = map(lambda x: getattr(x, 'info'), handlers)

        self.assertEqual(len(handlers), 4)
        self.assertEqual(handlers_required, [(self.tests.I1,), (self.tests.I1, self.tests.I2), (self.tests.I1,), (implementedBy(self.tests.U),)])
        self.assertEqual(handlers_handler, [handle1, handle12, handle, handle])
        self.assertEqual(handlers_info, [u'First handler', u'', u'a comment', u'handle a class'])

    def test_unregister_handler(self):
        from zope import registry

        test_object1 = self.tests.U1(1)
        test_object2 = self.tests.U12(2)

        @registry.adapter(self.tests.I1)
        def handle1(x):
            self.assertEqual(x, test_object1)

        @registry.adapter(self.tests.I1, self.tests.I2)
        def handle12(x, y):
            self.assertEqual(x, test_object1)
            self.assertEqual(y, test_object2)

        handle_calls = []
        def handle(*objects):
            handle_calls.append(objects)

        self.components.registerHandler(handle1, info=u'First handler')
        self.components.registerHandler(handle12)
        self.components.registerHandler(handle, required=[self.tests.I1], info=u'a comment')
        self.components.registerHandler(handle, required=[self.tests.U], info=u'handle a class')

        self.assertEqual(len(list(self.components.registeredHandlers())), 4)
        self.assertTrue(self.components.unregisterHandler(handle12))
        self.assertEqual(len(list(self.components.registeredHandlers())), 3)
        self.assertFalse(self.components.unregisterHandler(handle12))
        self.assertEqual(len(list(self.components.registeredHandlers())), 3)
        self.assertRaises(TypeError, self.components.unregisterHandler)
        self.assertEqual(len(list(self.components.registeredHandlers())), 3)
        self.assertTrue(self.components.unregisterHandler(handle, required=[self.tests.I1]))
        self.assertEqual(len(list(self.components.registeredHandlers())), 2)
        self.assertTrue(self.components.unregisterHandler(handle, required=[self.tests.U]))
        self.assertEqual(len(list(self.components.registeredHandlers())), 1)

    def test_multi_handler_unregistration(self):
        """
        There was a bug where multiple handlers for the same required
        specification would all be removed when one of them was
        unregistered.

        """
        from zope import interface

        calls = []

        class I(interface.Interface):
            pass

        def factory1(event):
            calls.append(2)

        def factory2(event):
            calls.append(3)

        class Event(object):
            interface.implements(I)

        self.components.registerHandler(factory1, [I,])
        self.components.registerHandler(factory2, [I,])
        self.components.handle(Event())
        self.assertEqual(sum(calls), 5)
        self.assertTrue(self.components.unregisterHandler(factory1, [I,]))
        calls = []
        self.components.handle(Event())
        self.assertEqual(sum(calls), 3)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(Test),))

if __name__ == '__main__':
    main(defaultTest='test_suite')    
