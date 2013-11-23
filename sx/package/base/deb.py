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

class DebFile(AbstractPackageFile):

    def __init__(self, deb_file):
        super(AbstractPackageFile, self).__init__()
        self.file = deb_file
        self.package = DebPackage(deb_file, CACHE)
        self.package.check()
        print(CACHE[self.name])

    def is_source(self):
        return  'Source' in self.package or self.arch == 'source'

    @property
    def requires(self):
        return self.package.required_changes

    @property
    def arch(self):
        return self.package['Architecture']

    @property
    def name(self):
        return self.package.pkgname

    @property
    def install(self):
        return super(DebFile, self).install()

    @property
    def license(self):
        if 'License' in self.package:
            return self.package['License']


    @property
    def confilts(self):
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
        if 'Distribution' in self.package:
            return self.package['Distribution']
        return 'unstable'


class DebPackager(AbstractPackagerBase):

    def add(self, *args):
        return super(DebPackager, self).add(*args)

    def check(self):
        return super(DebPackager, self).check()

    def order(self, packages):
        return packages#return super(DebPackager, self).order(packages)

    def uninstall(self, *args):
        return super(DebPackager, self).uninstall(*args)

    def run(self, callback):
        return super(DebPackager, self).run(callback)

    def clear(self):
        pass#return super(DebPackager, self).clear()

    def package(self, *args, **kwargs):
        return DebFile(*args, **kwargs)

DEB = DebPackager(__AVAILABLE, 'deb')
