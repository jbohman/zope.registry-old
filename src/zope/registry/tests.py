##############################################################################
#
# Copyright (c) 2001, 2002, 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Component Architecture Tests
"""

import doctest
import re
import unittest

from zope import interface
from zope import registry
from zope.interface.verify import verifyObject
from zope.interface.interfaces import IInterface

class I1(interface.Interface):
    pass
class I2(interface.Interface):
    pass
class I2e(I2):
    pass
class I3(interface.Interface):
    pass
class IC(interface.Interface):
    pass

class ITestType(IInterface):
    pass

class U:

    def __init__(self, name):
        self.__name__ = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__name__)

class U1(U):
    interface.implements(I1)

class U12(U):
    interface.implements(I1, I2)

class IA1(interface.Interface):
    pass

class IA2(interface.Interface):
    pass

class IA3(interface.Interface):
    pass

class A:

    def __init__(self, *context):
        self.context = context

    def __repr__(self):
        return "%s%r" % (self.__class__.__name__, self.context)

class A12_1(A):
    registry.adapts(I1, I2)
    interface.implements(IA1)

class A12_(A):
    registry.adapts(I1, I2)

class A_2(A):
    interface.implements(IA2)

class A_3(A):
    interface.implements(IA3)

class A1_12(U):
    registry.adapts(I1)
    interface.implements(IA1, IA2)

class A1_2(U):
    registry.adapts(I1)
    interface.implements(IA2)

class A1_23(U):
    registry.adapts(I1)
    interface.implements(IA1, IA3)

def noop(*args):
    pass

def test_multi_handler_unregistration():
    """
    There was a bug where multiple handlers for the same required
    specification would all be removed when one of them was
    unregistered:

    >>> class I(interface.Interface):
    ...     pass
    >>> def factory1(event):
    ...     print "| Factory 1 is here"
    >>> def factory2(event):
    ...     print "| Factory 2 is here"
    >>> class Event(object):
    ...     interface.implements(I)
    >>> from zope.registry import Components
    >>> registry = Components()
    >>> registry.registerHandler(factory1, [I,])
    >>> registry.registerHandler(factory2, [I,])
    >>> registry.handle(Event())
    | Factory 1 is here
    | Factory 2 is here
    >>> registry.unregisterHandler(factory1, [I,])
    True
    >>> registry.handle(Event())
    | Factory 2 is here
    """

def dont_leak_utility_registrations_in__subscribers():
    """

    We've observed utilities getting left in _subscribers when they
    get unregistered.

    >>> import zope.registry
    >>> reg = zope.registry.Components()
    >>> class C:
    ...     def __init__(self, name):
    ...         self.name = name
    ...     def __repr__(self):
    ...         return "C(%s)" % self.name

    >>> c1 = C(1)
    >>> reg.registerUtility(c1, I1)
    >>> reg.registerUtility(c1, I1)
    >>> list(reg.getAllUtilitiesRegisteredFor(I1))
    [C(1)]

    >>> reg.unregisterUtility(provided=I1)
    True
    >>> list(reg.getAllUtilitiesRegisteredFor(I1))
    []

    >>> reg.registerUtility(c1, I1)
    >>> reg.registerUtility(C(2), I1)

    >>> list(reg.getAllUtilitiesRegisteredFor(I1))
    [C(2)]

    """

class Ob3(object):
    interface.implements(IC)

def setUp(tests):
    pass

def tearDown(tests):
    pass

def setUpRegistryTests(tests):
    setUp(tests)

def tearDownRegistryTests(tests):
    tearDown(tests)
    import zope.event
    zope.event.subscribers.pop()

def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp=setUp, tearDown=tearDown),
            doctest.DocFileSuite('registry.txt',
                                 globs={'__name__': '__main__'},
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 setUp=setUpRegistryTests,
                                 tearDown=tearDownRegistryTests),
        ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
