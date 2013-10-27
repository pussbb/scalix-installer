# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'


from sx.utils import properties_from_file, absolute_file_path

def version_file():
    return absolute_file_path('version.properties')

def version_properties():
     return properties_from_file(version_file())

def get_version():
    properties = properties_from_file(version_file(), replace_dots=True)
    return '{version_major}.{version_minor}.{version_patch}.{build_number}'\
        .format(**properties)

if __name__ == '__main__':
    print(get_version(), version_properties())

