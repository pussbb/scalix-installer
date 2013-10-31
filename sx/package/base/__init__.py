__author__ = 'pussbb'

from distutils.version import StrictVersion

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

class PackageBaseFile(object):

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

    def __repr__(self, indent=""):
        return '{name}\n{indent}File: {file}\n{indent}Version: {ver}\n' \
               '{indent}Architecture: {arch}\n{indent}License: {lic}\n' \
               '{indent}Requiers: {require}\n{indent}Confilts: {conflicts}\n' \
               '{indent}Provides: {provides}\n'\
            .format(name=self.name, indent=indent, file=self.file,
                    ver=self.version, arch=self.arch, lic=self.license,
                    require=self.requires, conflicts=self.confilts,
                    provides=self.provides)
