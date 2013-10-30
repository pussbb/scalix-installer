# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

import os


from sx.package.base import PackageBase, PackageBaseFile

__all__ = ["RPM"]

try:
    import rpm
except ImportError as exception:
    __AVAILABLE = False

_ts = rpm.ts()

class RpmFile(PackageBaseFile):

    def __init__(self, rpm_file):
        self.file = rpm_file
        self.header = None
        fdno = os.open(rpm_file, os.O_RDONLY)
        try:
            _ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
            self.header = _ts.hdrFromFdno(fdno)
        except rpm.error as exception:
            pass
        finally:
            os.close(fdno)

    @property
    def name(self):
        return self.header[rpm.RPMTAG_NAME]

    @property
    def version(self):
        return self.header[rpm.RPMTAG_VERSION]

    @property
    def description(self):
        return self.header[rpm.RPMTAG_DESCRIPTION]

    @property
    def arch(self):
        return self.header[rpm.RPMTAG_ARCH]

    @property
    def platform(self):
        platform_ = self.header[rpm.RPMTAG_PLATFORM]
        if platform_ and platform_.find('-') == -1:
            return platform_
        return self.release.split('.')[-1]

    def is_source(self):
        return self.header.isSource()

    @property
    def license(self):
        return self.header[rpm.RPMTAG_LICENSE]

    @property
    def release(self):
        return self.header[rpm.RPMTAG_RELEASE]

    @property
    def summary(self):
        return self.header[rpm.RPMTAG_SUMMARY]

    @property
    def provides(self):
        return self.header[rpm.RPMTAG_PROVIDENEVRS]

    @property
    def confilts(self):
        return self.header[rpm.RPMTAG_CONFLICTS]

    @property
    def requires(self):
        return self.header[rpm.RPMTAG_REQUIRENEVRS]

class RpmPackage(PackageBase):
    def package(self, *args, **kwargs):
        return RpmFile(*args, **kwargs)


RPM = RpmPackage(__AVAILABLE, 'rpm')
