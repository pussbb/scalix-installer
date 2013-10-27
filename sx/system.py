# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import platform
import sys
import webbrowser

from sx.utils import execute
from sx.exceptions import ScalixExternalCommandFailed
import sx.logger as logger

UNAME_KEYS = [
    'system',
    'node',
    'release',
    'version',
    'machine',
    'processor'
]
"""
Supported platforms item's descripton
(
    'CentOS', # distro name
    '6', # version if needed specify concrete version just do it. e.g. 'Ubuntu'
    'Final', # distro abbreviation
    'x86_64', #platfrom architecture 32bit's or 64 bit's
    'rhel6' # packages release abbreviation
)
"""
SUPPORTED_PLATFORMS = (
    ('CentOS', '6', 'Final', 'x86_64', 'rhel6'),
    ('CentOS', '6', 'Final', 'x86', 'rhel6'),
    ('Ubuntu', '13.10', 'saucy', 'x86_64', '???'),
)
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

    def is_supported(self):
        current_platform = ()
        if self.is_linux():
            current_platform = (self.distro, self.distro_version, self.machine)

        for platform in SUPPORTED_PLATFORMS:
            if current_platform[0] != platform[0]:
                continue
            if not current_platform[1].startswith(platform[1]):
                continue
            if current_platform[2] != platform[3]:
                continue
            return True

        return False

    @staticmethod
    def run_level():
        try:
            result = execute("runlevel", "|","gawk '{print $2}'")
            return int(result[0])
        except ScalixExternalCommandFailed,e:
            logger.critical("Could not get run level", e)
            return -1

    @staticmethod
    def memory_total():
        try:
            #gawk '/MemTotal/ { print $2 }' /proc/meminfo
            return int(execute("gawk","'/MemTotal/ { print $2 }'",
                               "/proc/meminfo")[0])
        except ScalixExternalCommandFailed,e:
            logger.critical("Could not get total memory", e)
            return -1

    @staticmethod
    def memory_free():
        try:
            #"gawk '/MemFree/ { print $2 }' /proc/meminfo"
            return int(execute("gawk","'/MemFree/ { print $2 }'",
                               "/proc/meminfo")[0])
        except ScalixExternalCommandFailed,e:
            logger.critical("Could not get free memory", e)
            return -1

    @staticmethod
    def memory():
        return System.memory_total(), System.memory_free()

    @staticmethod
    def partition_size(folder):
        try:
            #"df -lP %s | gawk '{print $4}'"
            result = execute("df", "-lp", folder, "|", "gawk '{print $4}'")
            try:
                return int(result[1])
            except (UnicodeEncodeError, ValueError) as e:
                logger.critical("Could not get partition size", result)
                return -1
        except ScalixExternalCommandFailed,e:
            logger.critical("Could not get partition size", e)
            return -1

    @staticmethod
    def disk_space(*args):
        if not args:
            return System.partition_size('/')
        result = []
        for partition in args:
            result.append(System.partition_size(partition))
        return result

    @staticmethod
    def open_url(url):
        try:
            return webbrowser.open(url, 1)
        except webbrowser.Error, e:
            logger.critical("Couldn't open brouser", e, " url ", url)
            return False
