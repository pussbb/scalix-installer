# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

try:
    import debian
except ImportError as exception:
    __AVAILABLE = False

from sx.package.base import PackageBase

class DebFile(object):

    def __init__(self, deb_file):
        pass

class DebPackage(PackageBase):

    def package(self, *args, **kwargs):
        return DebFile(*args, **kwargs)

DEB = DebPackage(__AVAILABLE, 'deb')
