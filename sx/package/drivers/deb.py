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

def is_available():
    return __AVAILABLE

def file_extention():
    return "deb"

class DebFile(object):

    def __init__(self, deb_file):
        pass
