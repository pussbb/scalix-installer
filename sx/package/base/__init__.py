__author__ = 'pussbb'

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

    def install(self, package):
        raise NotImplementedError()

    def update(self, package):
        raise NotImplementedError()

    def uninstall(self, package):
        raise NotImplementedError()


class PackageBaseFile(object):

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

    def is_32bit(self):
        return self.arch in ['i386', 'i586', 'i686',]

    def is_64bit(self):
        return self.arch == 'x86_64'

    def is_source(self):
        raise NotImplementedError()

    def __repr__(self, indent=""):
        return '{name}\n{indent}File: {file}\n{indent}Version: {ver}\n' \
               '{indent}Description: {desc}\n{indent}Architecture: {arch}\n' \
               '{indent}License: {lic}'\
            .format(name=self.name, indent=indent, file=self.file,
                    ver=self.version, desc=self.description, arch=self.arch,
                    lic=self.license)
