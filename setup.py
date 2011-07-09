##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.registry package
"""
import sys
import os
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['setup_requires'] = ['zope.fixers']
    extra['use_2to3'] = True
    extra['use_2to3_fixers'] = ['zope.fixers']

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='zope.registry',
    version='0.1dev',
    url='http://pypi.python.org/pypi/zope.registry',
    license='ZPL 2.1',
    description='Zope Component Architecture',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(
        read('README.txt')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('REGISTRY.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    packages=['zope', 'zope.registry', 'zope.registry.tests'],
    package_dir={'': 'src'},
    namespace_packages=['zope'],
    install_requires=['setuptools', 'zope.interface', 'zope.event'],
    tests_require=['setuptools', 'zope.interface', 'zope.event'],
    test_suite='zope.registry.tests',
    zip_safe=False,
    **extra
    )
