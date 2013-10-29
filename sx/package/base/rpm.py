# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

import os

from sx.package.base import PackageBase

try:
    import rpm
except ImportError as exception:
    __AVAILABLE = False

def is_available():
    return __AVAILABLE

def file_extention():
    return "rpm"

RPMTAGS = [
    'RPMTAG_NAME',
    'RPMTAG_VERSION',
    'RPMTAG_RELEASE',
    'RPMTAG_SUMMARY',
    'RPMTAG_DESCRIPTION',
    'RPMTAG_SIZE',
    'RPMTAG_LICENSE',
    'RPMTAG_OS',
    'RPMTAG_ARCH',
    'RPMTAG_PLATFORM',
]

class RpmFile(object):

    def __init__(self, rpm_file):
        ts = rpm.ts()
        self.header = None
        fdno = os.open(rpm_file, os.O_RDONLY)
        try:
            ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
            self.header = ts.hdrFromFdno(fdno)
        except rpm.error as exception:
            pass
        finally:
            os.close(fdno)

        for item in RPMTAGS:
            name = item.split('_')[1].lower()
            setattr(self, name, self.header[getattr(rpm, item)])
        print(self.__dict__)

class RpmPackage(PackageBase):

    def package(self, *args, **kwargs):
        return RpmFile(*args, **kwargs)

RPM = RpmPackage(__AVAILABLE, 'rpm')
