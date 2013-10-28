# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

import os

try:
    import rpm
except ImportError as exception:
    __AVAILABLE = False

def is_available():
    return __AVAILABLE

def file_extention():
    return "rpm"

__PRMTAGS = [
    'RPMTAG_NAME',
    'RPMTAG_VERSION',
    'RPMTAG_RELEASE',
    'RPMTAG_SUMMARY',
    'RPMTAG_DESCRIPTION',
    'RPMTAG_BUILDTIME',
    'RPMTAG_BUILDHOST',
    'RPMTAG_SIZE',
    'RPMTAG_LICENSE',
    'RPMTAG_GROUP',
    'RPMTAG_OS',
    'RPMTAG_ARCH',
    'RPMTAG_SOURCERPM',
    'RPMTAG_FILEVERIFYFLAGS',
    'RPMTAG_ARCHIVESIZE',
    'RPMTAG_RPMVERSION',
    'RPMTAG_CHANGELOGTIME',
    'RPMTAG_CHANGELOGNAME',
    'RPMTAG_CHANGELOGTEXT',
    'RPMTAG_COOKIE',
    'RPMTAG_OPTFLAGS',
    'RPMTAG_PAYLOADFORMAT',
    'RPMTAG_PAYLOADCOMPRESSOR',
    'RPMTAG_PAYLOADFLAGS',
    'RPMTAG_RHNPLATFORM',
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
        __PRMTAGS = [
            'RPMTAG_NAME',
            'RPMTAG_VERSION',
            'RPMTAG_RELEASE',
            'RPMTAG_SUMMARY',
            'RPMTAG_DESCRIPTION',
            'RPMTAG_BUILDTIME',
            'RPMTAG_BUILDHOST',
            'RPMTAG_SIZE',
            'RPMTAG_LICENSE',
            'RPMTAG_GROUP',
            'RPMTAG_OS',
            'RPMTAG_ARCH',
            #'RPMTAG_SOURCERPM',
            #'RPMTAG_FILEVERIFYFLAGS',
            #'RPMTAG_ARCHIVESIZE',
            'RPMTAG_RPMVERSION',
            #'RPMTAG_CHANGELOGTIME',
            #'RPMTAG_CHANGELOGNAME',
            #'RPMTAG_CHANGELOGTEXT',
            #'RPMTAG_COOKIE',
            'RPMTAG_OPTFLAGS',
            #'RPMTAG_PAYLOADFORMAT',
            #'RPMTAG_PAYLOADCOMPRESSOR',
            #'RPMTAG_PAYLOADFLAGS',
            #'RPMTAG_RHNPLATFORM',
            'RPMTAG_PLATFORM',
        ]
        res = []
        for i in __PRMTAGS:
            res.append(self.header[getattr(rpm, i)])
        print(res)
        #print(self.header[rpm.RPMTAG_NAME], self.header[rpm.RPMTAG_ARCH])
