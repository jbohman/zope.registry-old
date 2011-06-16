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
from setuptools import setup, find_packages


tests_require = [
    'zope.testing',
    'zope.testrunner'
    ]

if sys.version_info < (3,):
    extra = {}
else:
    extra = dict(
      use_2to3=True,
      convert_2to3_doctests=['src/zope/registry/registry.txt', 'src/zope/registry/tests.py'],
    )


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
        read('src', 'zope', 'registry', 'registry.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data = {'': ['registry.txt']},

    namespace_packages=['zope',],
    tests_require = tests_require,
    install_requires=['setuptools',
                      'zope.interface',
                      'zope.event',
                      'six',
                      ],
    include_package_data = True,
    zip_safe = False,
    test_suite='zope.registry.tests.test_suite',
    **extra
    )
