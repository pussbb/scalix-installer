# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

try:
    import apt
    from apt.debfile import DebPackage
    CACHE = apt.Cache()
except ImportError as exception:
    __AVAILABLE = False

from sx.package.base import AbstractPackagerBase, AbstractPackageFile
from sx.exceptions import ScalixUnresolvedDependencies
class DebFile(AbstractPackageFile):

    def __init__(self, deb_file):
        super(AbstractPackageFile, self).__init__()
        self.file = deb_file
        self.package = DebPackage(deb_file, CACHE)
        self.package.check()

    def is_source(self):
        try:
            self.package['Source']
        except KeyError as exception:
            if self.arch == 'source':
                return True
            else:
                return False
        return True

    @property
    def requires(self):
        return self.package.depends

    @property
    def arch(self):
        return self.package['Architecture']

    @property
    def name(self):
        return self.package.pkgname

    @property
    def license(self):
        try:
            return self.package['License']
        except KeyError as exception:
            pass

    @property
    def conflicts(self):
        return self.package.conflicts

    @property
    def version(self):
        return self.package['Version']

    @property
    def summary(self):
        return self.description

    @property
    def upgradable(self):
        return super(DebFile, self).upgradable()

    @property
    def provides(self):
        return self.package.provides

    @property
    def platform(self):
        return None

    @property
    def description(self):
        return self.package['Description']

    @property
    def installed(self):
        return self.package.compare_to_version_in_cache() \
               != DebPackage.VERSION_NONE


    @property
    def release(self):
        try:
            return self.package['Distribution']
        except KeyError as exception:
            return 'unstable'


class DebPackager(AbstractPackagerBase):

    def __init__(self, available, file_extention):
        super(DebPackager, self).__init__(available, file_extention)
        self.__packages = {}

    def add(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        for pkg in args:
            self.__packages[pkg.name] = pkg

    def check(self):
        dependencies = {}
        for name, item in self.__packages.items():
            pkg_data = { 'require': [], 'conflict': [],}
            if item.requires:
                for dependency in item.requires[0]:
                    dep_name = dependency[0]
                    if dep_name not in self.__packages.keys():
                        pkg = CACHE[dep_name]
                        #pkg.installedVersion
                        if not pkg.installed:
                            pkg_data['require'].append((dependency[0],
                                                       dependency[2],
                                                       dependency[1]))
            if item.conflicts:
                for conflict in item.conflicts[0]:
                    if CACHE[conflict[0]].installed:
                        pkg_data['conflict'].append(conflict)

            if pkg_data['require'] or pkg_data['conflict']:
                dependencies[name] = pkg_data

        if dependencies:
            raise ScalixUnresolvedDependencies(dependencies)

        return True

    def order(self, packages):
        return packages#return super(DebPackager, self).order(packages)

    def uninstall(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        for package in args:
            pkg = CACHE[package.name]
            pkg.mark_delete()

    def run(self, callback):
        self.check()

        #return super(DebPackager, self).run(callback)

    def clear(self):
        self.__packages = {}
        CACHE.clear()

    def package(self, *args, **kwargs):
        return DebFile(*args, **kwargs)

DEB = DebPackager(__AVAILABLE, 'deb')
