# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

import os
import sys
#from cStringIO import StringIO

if sys.version_info[0] < 3:
    import imp
    imp.reload(sys)
    sys.setdefaultencoding("UTF-8")

from sx.package.base import PackageBase, PackageBaseFile
from sx.exceptions import ScalixUnresolvedDependencies, ScalixPackageProblems
import sx.logger as logger
from sx.package import *

__all__ = ["RPM"]

try:
    import rpm
except ImportError as exception:
    __AVAILABLE = False

rpm.setVerbosity(0)
_TS = rpm.ts()
_TS.setVSFlags(rpm._RPMVSF_NOSIGNATURES)


class RpmFile(PackageBaseFile):

    def __init__(self, rpm_file):
        #super(PackageBaseFile, self).__init__()
        PackageBaseFile.__init__(self)
        self.file = rpm_file
        self.header = None
        fdno = os.open(rpm_file, os.O_RDONLY)
        try:
            self.header = _TS.hdrFromFdno(fdno)
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
        return len(_TS.dbMatch('name', self.name)) > 0

    @property
    def upgradable(self):
        if not self.installed:
            return False
        inst_h = _TS.dbMatch('name', self.name)[0]
        return inst_h.dsOfHeader().EVR() > self.header.dsOfHeader().EVR()


class RpmPackage(PackageBase):

    """ file descriptor for run runCallback
    """
    fd = None
    filename = None

    def package(self, *args, **kwargs):
        return RpmFile(*args, **kwargs)

    def uninstall(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        for package in args:
            mi = _TS.dbMatch('name', package.name)
            _TS.addErase(*mi)

    def __package_instalation_data(self, package):
        key = 'i'
        if package.installed or package.upgradable:
            key = 'u'
        return [package.header, package.file, key]

    def add(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        for package in args:
            _TS.addInstall(*self.__package_instalation_data(package))

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

        for dep in dependecies:
            package, unresolved, needs_flags, _, sense = dep
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

    @staticmethod
    def prob_flag_format(prob):
        result = ""
        if prob & rpm.RPMPROB_BADOS:
            result += " (Bad OS) "
        if prob & rpm.RPMPROB_BADRELOCATE:
            result += " (Bad relocation) "
        if prob & rpm.RPMPROB_CONFLICT:
            result += " (Conflict) "
        if prob & rpm.RPMPROB_BADARCH:
            result += " ( bad architecture ) "
        if prob & rpm.RPMPROB_DISKNODES:
            result += " ( disk nodes ) "
        if prob & rpm.RPMPROB_DISKSPACE:
            result += " (disk space) "
        if prob & rpm.RPMPROB_FILE_CONFLICT:
            result += " (file conflit)"
        if prob & rpm.RPMPROB_FILTER_DISKNODES:
            result += " (filter disk nodes) "
        if prob & rpm.RPMPROB_FILTER_DISKSPACE:
            result += " ( filter disk space ) "
        if prob & rpm.RPMPROB_FILTER_FORCERELOCATE:
            result += " ( filter force relocate) "
        if prob & rpm.RPMPROB_FILTER_IGNOREARCH:
            result += " ( filter ignore search ) "
        if prob & rpm.RPMPROB_FILTER_IGNOREOS:
            result += " ( filter ignore os) "
        if prob & rpm.RPMPROB_FILTER_OLDPACKAGE:
            result += " (filter old package) "
        if prob & rpm.RPMPROB_FILTER_REPLACENEWFILES:
            result += " (filter replace new files) "
        if prob & rpm.RPMPROB_FILTER_REPLACEOLDFILES:
            result += " (filter replace old files) "
        if prob & rpm.RPMPROB_FILTER_REPLACEPKG:
            result += " (filter replace package ) "
        if prob & rpm.RPMPROB_NEW_FILE_CONFLICT:
            result += " ( new file conflict) "
        if prob & rpm.RPMPROB_OLDPACKAGE:
            result += " ( old package) "
        if prob & rpm.RPMPROB_PKG_INSTALLED:
            result += " ( package installed ) "
        if prob & rpm.RPMPROB_REQUIRES:
            result += " (package requires) "
        return result

    def __parse_problems(self, problems):
        result = {}
        for problem in problems:
            if not result.get(problem.pkgNEVR):
                result[problem.pkgNEVR] = []
            item = " {0} {1}".format(RpmPackage.prob_flag_format(problem.type),
                                     problem.altNEVR )
            result[problem.pkgNEVR].append(item)
        return result

    def clear(self):
        _TS.clean()
        try:
            _TS.clear()
        except AttributeError as exception:
            pass

    def check(self):
        dependecies = _TS.check()

        if dependecies:
            raise ScalixUnresolvedDependencies(
                self.__parse_dependencies(dependecies))

        problems = _TS.problems()
        if problems:
            raise ScalixPackageProblems(self.__parse_problems(problems))

        return True

    def order(self, packages):
        ts = rpm.ts()
        for package in packages.values():
            ts.addInstall(*self.__package_instalation_data(package))

        ts.check()
        ts.order()
        return [te.N() for te in ts]

    def run_callback(self, reason, amount, total, key, callback):
        logger.debug("run call back data", reason, amount, total, key,
                     callback)
        if reason == rpm.RPMCALLBACK_INST_OPEN_FILE:
            basename = os.path.basename(key)
            RpmPackage.filename = '-'.join(basename.split('-')[:2])
            RpmPackage.fd = os.open(key, os.O_RDONLY)
            return RpmPackage.fd
        elif reason == rpm.RPMCALLBACK_INST_CLOSE_FILE:
            os.close(RpmPackage.fd)
        elif reason == rpm.RPMCALLBACK_INST_PROGRESS:
            complete_percents = amount*100//total
            callback(PKG_INST_PROGRESS, RpmPackage.filename, complete_percents)
            #hack on centos 6.4 rpm doesn't have RPMCALLBACK_INST_STOP
            if amount == total:
                callback(PKG_INST_STOP, RpmPackage.filename)
        #elif reason == rpm.RPMCALLBACK_INST_STOP:
        #    logger.degug("instaltion stop")
        elif reason == rpm.RPMCALLBACK_INST_START:
            callback(PKG_INST_START, RpmPackage.filename)
        elif reason == rpm.RPMCALLBACK_UNINST_START:
            callback(PKG_UNINST_START, key)
        elif reason == rpm.RPMCALLBACK_UNINST_PROGRESS:
            callback(PKG_INST_PROGRESS, key, amount*100//total)
        elif reason == rpm.RPMCALLBACK_UNINST_STOP:
            callback(PKG_UNINST_STOP, key)

    def run(self, callback):
        #TODO write exceptions

        self.check()
        _TS.order()
        rpm.setLogFile(logger.logger_stream())
        _TS.run(self.run_callback, callback)
        self.clear()
        #_TS.test(self.runCallback, 1)


RPM = RpmPackage(__AVAILABLE, 'rpm')

"""
RPMCALLBACK_INST_CLOSE_FILE = 8
RPMCALLBACK_INST_OPEN_FILE = 4
RPMCALLBACK_INST_PROGRESS = 1
RPMCALLBACK_INST_START = 2
RPMCALLBACK_REPACKAGE_PROGRESS = 1024
RPMCALLBACK_REPACKAGE_START = 2048
RPMCALLBACK_REPACKAGE_STOP = 4096
RPMCALLBACK_SCRIPT_ERROR = 32768
RPMCALLBACK_TRANS_PROGRESS = 16
RPMCALLBACK_TRANS_START = 32
RPMCALLBACK_TRANS_STOP = 64
RPMCALLBACK_UNINST_PROGRESS = 128
RPMCALLBACK_UNINST_START = 256
RPMCALLBACK_UNINST_STOP = 512
RPMCALLBACK_UNKNOWN = 0
RPMCALLBACK_UNPACK_ERROR = 8192
"""
