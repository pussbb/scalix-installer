# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

import os


from sx.package.base import PackageBase, PackageBaseFile
from sx.exceptions import ScalixUnresolvedDependencies

__all__ = ["RPM"]

try:
    import rpm
except ImportError as exception:
    __AVAILABLE = False

_ts = rpm.ts()
_ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
#_ts.initDB()

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
        versions = self.header[rpm.RPMTAG_PROVIDEVERSION]
        packages = self.header[rpm.RPMTAG_PROVIDES]
        result = []
        for index, name in enumerate(packages):
            result.append((name, versions[index]))
        return result


    @property
    def confilts(self):
        return self.header[rpm.RPMTAG_CONFLICTS]

    @property
    def requires(self):
        versions = self.header[rpm.RPMTAG_REQUIREVERSION]
        packages =  self.header[rpm.RPMTAG_REQUIRES]
        result = []
        for index, name in enumerate(packages):
            result.append((name, None, versions[index]))
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

rpmtsCallback_fd = None

class RpmPackage(PackageBase):

    def package(self, *args, **kwargs):
        return RpmFile(*args, **kwargs)

    def uninstall(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        for package in args:
            _ts.addErase(package.header)

    def __package_instalation_data(self, package):
        key = 'i'
        if package.installed or package.upgradable:
            key = 'u'
        return [package.header, package.file, key]

    def add(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        for package in args:
            _ts.addInstall(*self.__package_instalation_data(package))

    @staticmethod
    def parse_need_flag(mask):
        result = ''
        if mask & rpm.RPMSENSE_EQUAL:
            result = '='
        if mask & rpm.RPMSENSE_GREATER:
            result =  '>' + result
        if mask & rpm.RPMSENSE_LESS:
            result = '<' + result

        return result

    def __parse_dependencies(self, dependecies):
        result = {}
        #'require': [],
        #'conflict': [],
        for dep in dependecies:
            package, unresolved, needs_flags, suggested_package, sense = dep
            if package[0] not in result:
                result[package[0]] = {
                    'require': [],
                    'conflict': [],
                }
            data = (
                unresolved[0],
                RpmPackage.parse_need_flag(needs_flags),
                unresolved[1]
            )
            if sense is rpm.RPMDEP_SENSE_CONFLICTS:
                result[package[0]]['conflicts'].append(data)
            else:
                result[package[0]]['require'].append(data)
        return result

    def check(self):
        dependecies = _ts.check()
        if dependecies:
            raise ScalixUnresolvedDependencies(self.__parse_dependencies(dependecies))
        return True

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


    def run(self):
        #TODO write exceptions

        self.check()
        _ts.order()
        _ts.run()
        #_ts.test(self.runCallback, 1)


RPM = RpmPackage(__AVAILABLE, 'rpm')
