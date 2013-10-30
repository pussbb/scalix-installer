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
_ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)

class RpmFile(PackageBaseFile):

    def __init__(self, rpm_file):
        self.file = rpm_file
        self.header = None
        fdno = os.open(rpm_file, os.O_RDONLY)
        try:
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
        requires_ = self.header[rpm.RPMTAG_REQUIRENEVRS]
        result = []
        for item in requires_:
            parts = item.split()
            if len(parts) == 1:
                result.append((item, None, None))
            else:
                result.append((parts[0], parts[1], parts[2]))
        return result

    @property
    def installed(self):
        return len(_ts.dbMatch('name', self.name)) > 0

    @property
    def upgradable(self):
        if not self.installed:
            return False
        inst_h = _ts.dbMatch('name', self.name)[0]
        return inst_h.dsOfHeader().EVR() > self.header.dsOfHeader().EVR()

class RpmPackage(PackageBase):

    def package(self, *args, **kwargs):
        return RpmFile(*args, **kwargs)

    def uninstall(self, package):
        _ts.addErase(package.header)

    def __package_instalation_data(self, package):
        key = 'i'
        if package.installed or package.upgradable:
            key = 'u'
        return (package.header, os.path.basename(package.file), key)

    def add(self, package):
        _ts.addInstall(*self.__package_instalation_data(package))

    def order(self, packages):
        ts = rpm.ts()
        for package in packages.values():
            ts.addInstall(*self.__package_instalation_data(package))

        ts.check()
        ts.order()
        result = []

        for te in ts:
            result.append(packages.get(te.N()))
        return result

    def runCallback(reason, amount, total, key, client_data):
        """
        http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch16s06s04.html
            if reason == rpm.RPMCALLBACK_INST_OPEN_FILE:
                print "Opening file. ", reason, amount, total, key, client_data
                rpmtsCallback_fd = os.open(client_data, os.O_RDONLY)
                return rpmtsCallback_fd
            elif reason == rpm.RPMCALLBACK_INST_START:
                print "Closing file. ", reason, amount, total, key, client_data
                os.close(rpmtsCallback_fd)
        """
        pass

    def run(self):
        #TODO write exceptions
        _ts.check()
        _ts.order()
        _ts.run()


RPM = RpmPackage(__AVAILABLE, 'rpm')
