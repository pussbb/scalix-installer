# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'


import sx.utils as utils

def version_file():
    """returns version file name with full path

    @rtype string

    """
    return utils.absolute_file_path('version.properties')

def version_properties():
    """get properties in version file

    @rtype dict
    @return dict

    """
    return utils.properties_from_file(version_file())

def get_version():
    """ returns current version of module

    @rtype string
    @return string in format major_v.minor_v.patch_v.build_N

    """
    properties = utils.properties_from_file(version_file(), replace_dots=True)
    return '{version_major}.{version_minor}.{version_patch}.{build_number}'\
        .format(**properties)

if __name__ == '__main__':
    print(get_version(), version_properties())

