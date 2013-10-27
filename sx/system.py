# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import platform
import sys

UNAME_KEYS = [
    'system',
    'node',
    'release',
    'version',
    'machine',
    'processor'
]

class System(object):

    def __init__(self):
        self.platform = sys.platform

        uname_data = platform.uname()
        for index, elem in enumerate(UNAME_KEYS):
            setattr(self, elem, uname_data[index])

        if self.is_linux():
            self.__determine_linux_platform()

    def __repr__(self):
        result = "System: {system}\nRelease: {release}\n" \
               "Version: {version}\nMachine: {machine}\n" \
               "Proccessor: {processor}".format(**self.__dict__)
        if self.is_linux():
            result = "{result}\nDistribution:{distro}" \
                     " {distro_version} ({distro_abr})"\
                .format(result=result,**self.__dict__)
        return result

    def __determine_linux_platform(self):
        self.distro, self.distro_version, self.distro_abr = \
            platform.linux_distribution()

    def is_linux(self):
        return self.platform.startswith('linux')

    def is_64bit(self):
        return self.machine == 'x86_64'

    def is_32bit(self):
        return self.machine in ['i386', 'i586', 'i686',]
