__author__ = 'pussbb'

from distutils.version import StrictVersion
from sx.exceptions import ScalixPackageException

class PackageBase(object):

    def __init__(self, available, file_extention):
        self.__available = available
        self.__file_extention = file_extention

    def __repr__(self):
        return "{0} file based".format(self.file_extention)

    @property
    def available(self):
        return self.__available

    @property
    def file_extention(self):
        return self.__file_extention

    def package(self, *args, **kwargs):
        raise NotImplementedError()

    def add(self, *args):
        raise NotImplementedError()

    def order(self, packages):
        raise NotImplementedError()

    def uninstall(self, *args):
        raise NotImplementedError()

    def check(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def clear(self):
        raise  NotImplementedError()

class PackageBaseFile(object):

    def __init__(self):
        self.__install = False
        self.__upgrade = False
        self.__uninstall = False

    def __lt__(self, other):
        #x<y
        return StrictVersion(self.version) < StrictVersion(other.version)

    def __le__(self, other):
        #x<=y
        return StrictVersion(self.version) <= StrictVersion(other.version)

    def __eq__(self, other):
        #x==y
        return StrictVersion(self.version) == StrictVersion(other.version)

    def __ne__(self, other):
        #x!=y and x<>y
        return StrictVersion(self.version) != StrictVersion(other.version)

    def __ge__(self, other):
        #x>=y
        return StrictVersion(self.version) >= StrictVersion(other.version)

    def __gt__(self, other):
        #x>y
        return StrictVersion(self.version) > StrictVersion(other.version)

    def __hash__(self):
        return hash(self)

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def version(self):
        raise NotImplementedError()

    @property
    def description(self):
        raise NotImplementedError()

    @property
    def license(self):
        raise NotImplementedError()

    @property
    def summary(self):
        raise NotImplementedError()

    @property
    def platform(self):
        raise NotImplementedError()

    @property
    def release(self):
        raise NotImplementedError()

    @property
    def arch(self):
        raise NotImplementedError()

    @property
    def noarch(self):
        return self.arch == 'noarch'

    @property
    def requires(self):
        raise NotImplementedError()

    @property
    def provides(self):
        raise NotImplementedError()

    @property
    def confilts(self):
        raise  NotImplementedError()

    def is_32bit(self):
        return self.arch in ['i386', 'i586', 'i686',]

    def is_64bit(self):
        return self.arch == 'x86_64'

    def is_source(self):
        raise NotImplementedError()

    @property
    def installed(self):
        raise NotImplementedError()

    @property
    def upgradable(self):
        raise NotImplementedError()

    @property
    def install(self):
        return self.__install

    @install.setter
    def install(self, state):
        if self.installed and state:
            raise ScalixPackageException("Package has already installed")
        self.__install = state

    @property
    def upgrade(self):
        return self.__upgrade

    @upgrade.setter
    def upgrade(self, state):
        if not self.installed and state:
            raise ScalixPackageException("Package not installed that\'s why"
                                         " it can not be mark for upgrade")
        self.__upgrade =  state

    @property
    def uninstall(self):
        return self.__uninstall

    @uninstall.setter
    def unistall(self, state):
        if not self.installed and state:
            raise ScalixPackageException("Package not installed that\'s why"
                                         " it can not be mark for uninstall")
        self.__uninstall = state


    def __repr__(self, indent=""):
        return '{name}\n{indent}File: {file}\n{indent}Version: {ver}\n' \
               '{indent}Architecture: {arch}\n{indent}License: {lic}\n' \
               '{indent}Requiers: {require}\n{indent}Confilts: {conflicts}\n' \
               '{indent}Provides: {provides}\n'\
            .format(name=self.name, indent=indent, file=self.file,
                    ver=self.version, arch=self.arch, lic=self.license,
                    require=self.requires, conflicts=self.confilts,
                    provides=self.provides)
