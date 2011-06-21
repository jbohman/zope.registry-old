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
"""Registry Tests"""

import doctest
import re
import unittest

from zope import interface
from zope import registry

from zope.registry.tests import test_utility
from zope.registry.tests import test_adapter
from zope.registry.tests import test_subscriber
from zope.registry.tests import test_handler
from zope.registry.tests import test_extending

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

class ITestType(interface.interfaces.IInterface):
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

def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(test_utility.Test),
            unittest.makeSuite(test_adapter.Test),
            unittest.makeSuite(test_subscriber.Test),
            unittest.makeSuite(test_handler.Test),
            unittest.makeSuite(test_extending.Test)
        ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
