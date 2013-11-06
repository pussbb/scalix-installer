# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

__AVAILABLE = True

try:
    import debian
except ImportError as exception:
    __AVAILABLE = False

from sx.package.base import AbstractPackagerBase, AbstractPackageFile

class DebFile(AbstractPackageFile):

    @property
    def requires(self):
        return super(DebFile, self).requires()

    @property
    def arch(self):
        return super(DebFile, self).arch()

    @property
    def name(self):
        return super(DebFile, self).name()

    @property
    def install(self):
        return super(DebFile, self).install()

    @property
    def license(self):
        return super(DebFile, self).license()

    @property
    def confilts(self):
        return super(DebFile, self).confilts()

    @property
    def version(self):
        return super(DebFile, self).version()

    @property
    def summary(self):
        return super(DebFile, self).summary()

    @property
    def upgradable(self):
        return super(DebFile, self).upgradable()

    @property
    def provides(self):
        return super(DebFile, self).provides()

    @property
    def platform(self):
        return super(DebFile, self).platform()

    @property
    def description(self):
        return super(DebFile, self).description()

    @property
    def installed(self):
        return super(DebFile, self).installed()

    @property
    def release(self):
        return super(DebFile, self).release()

    def __init__(self, deb_file):
        super(DebFile, self).__init__()
        self.file = deb_file
        pass

class DebPackager(AbstractPackagerBase):

    def add(self, *args):
        return super(DebPackager, self).add(*args)

    def check(self):
        return super(DebPackager, self).check()

    def order(self, packages):
        return super(DebPackager, self).order(packages)

    def uninstall(self, *args):
        return super(DebPackager, self).uninstall(*args)

    def run(self, callback):
        return super(DebPackager, self).run(callback)

    def clear(self):
        return super(DebPackager, self).clear()

    def package(self, *args, **kwargs):
        return DebFile(*args, **kwargs)

DEB = DebPackager(__AVAILABLE, 'deb')
