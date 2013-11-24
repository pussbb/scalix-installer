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
        AbstractPackageFile.__init__(self)
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
        except KeyError as _:
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
        except KeyError as _:
            return 'unstable'


class DebPackager(AbstractPackagerBase):

    def __init__(self, available, file_extention):
        AbstractPackagerBase.__init__(self, available, file_extention)
        self.__packages = {}

    def add(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        for pkg in args:
            self.__packages[pkg.name] = pkg

    def __check_dependencies(self, dependencies, pkg_data):
        for dependency in dependencies:
            for dep in dependency:
                dep_name = dep[0]
                dep_data = (dep[0], dep[2], dep[1])
                if dep_name in self.__packages:
                    continue
                try:
                    pkg = CACHE[dep_name]
                    if not pkg.installed:
                        pkg_data['require'].append(dep_data)
                except KeyError as _:
                    pkg_data['require'].append(dep_data)

    def __check_conflicts(self, conflicts, pkg_data):
        for conflict in conflicts:
            if CACHE[conflict[0]].installed:
                pkg_data['conflict'].append(conflict)

    def check(self):
        dependencies = {}
        for name, item in self.__packages.items():
            pkg_data = { 'require': [], 'conflict': [],}
            self.__check_dependencies(item.requires, pkg_data)
            self.__check_conflicts(item.conflicts, pkg_data)

            if pkg_data['require'] or pkg_data['conflict']:
                dependencies[name] = pkg_data

        if dependencies:
            raise ScalixUnresolvedDependencies(dependencies)

        return True

    def __prepend_dep(self, name, packages, queue):
        for dep in packages[name].requires:
            for _dep in dep:
                dep_name = _dep[0]
                if dep_name not in packages or dep_name in queue:
                    continue
                self.__prepend_dep(dep_name, packages, queue)
        queue.append(name)

    def order(self, packages):
        queue = []
        for name in sorted(packages):
            if name in queue:
                continue
            self.__prepend_dep(name, packages, queue)
        return queue


    def uninstall(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        for package in args:
            pkg = CACHE[package.name]
            pkg.mark_delete()

    def run(self, callback):
        self.check()
        if self.__packages:
            sorted_list = self.order(self.__packages)
            for pkg_name in sorted_list:
                self.__packages[pkg_name].package.install()
        elif CACHE.delete_count > 0:
            CACHE.commit()
        self.clear()
        #return super(DebPackager, self).run(callback)

    def clear(self):
        self.__packages = {}
        CACHE.clear()

    def package(self, *args, **kwargs):
        return DebFile(*args, **kwargs)

DEB = DebPackager(__AVAILABLE, 'deb')
