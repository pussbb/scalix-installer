__author__ = 'pussbb'


class PackageBase(object):

    def __init__(self, available, file_extention):
        self.__available = available
        self.__file_extention = file_extention

    @property
    def available(self):
        return self.__available

    @property
    def file_extention(self):
        return self.__file_extention

    def package(self, *args, **kwargs):
        raise NotImplemented

    def install(self, package):
        raise NotImplemented

    def update(self, package):
        raise NotImplemented

    def uninstall(self, package):
        raise NotImplemented

