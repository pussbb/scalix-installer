# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import os

from sx.package.base.deb import DEB
from sx.package.base.rpm import RPM
from sx.package.base import PackageBaseFile
import sx.utils as utils

class PackageManager(object):

    def __init__(self, system):
        self.system = system
        self.packages = []
        self.packages_dict = {}

    @staticmethod
    def available_drivers(self):
        return [driver for driver in [DEB, RPM] if driver.available]

    def scan_folder(self, folder):
        packages = {}
        for root, _, files in os.walk(folder, followlinks=True):
            for file_ in files:
                if file_.endswith(self.system.packager.file_extention):
                    self.__add_package(root, file_, packages)

        self.packages_dict = packages
        self.packages = self.system.packager.order(packages)


    def __add_package(self, directory, filename, packages):
        file_ = utils.absolute_file_path(filename, directory)
        package = self.system.packager.package(file_)

        #for now skip source packages let's deal with only with binary packages
        if package.is_source():
            return

        if not self.package_for_arch(package):
            return

        if package.name in packages and \
                        package <= packages[package.name]:
            return

        packages[package.name] = package


    def package_for_arch(self, package):
        result = False
        if package.is_source():
            result = True
        elif package.noarch:
            if package.name == 'scalix-tomcat-connector'\
                and self.system.target_platform != package.platform:
                    result = False
            else:
                result = True
        elif self.system.target_platform != package.platform:
            if package.name == 'scalix-libical' and not package.is_source():
                result = True
            else:
                result = False
        elif self.system.is_64bit() and (package.is_64bit()
                                       or package.is_32bit()):
            result = True
        elif self.system.is_32bit() and package.is_32bit():
            result = True
        return result

    def __repr__(self):
        result = "Package manager information:\nSystem package manager: {0}\n"\
            .format(repr(self.system.packager))

        result += "Available packages:\n"
        indent = " "*10
        packages = self.packages[:]
        #packages.reverse()
        for package in packages:
            result += "{0} - {1}\n\n".format(" "*5, package.__repr__(indent))
        return result

    def proccess(self, *args, **kwargs):

        if len(args) == 1 and isinstance(args[0], (list, dict)):
            args = args[0]

        for package in args:

            if not isinstance(package, PackageBaseFile):
                package = self.packages_dict.get(package)
                if not package:
                    raise StandardError("Unknown package")
            if not kwargs.get('delete', False):
                self.system.packager.add(package)
            else:
                self.system.packager.uninstall(package)

        self.system.packager.run()

    def format_dependencies(self, dependecies):
        result = "Following dependecies could not resolve:\n"
        package_indent = " " * 5
        dep_indent = package_indent * 5
        for package_name, data in dependecies.items():
            message = "{0}- {1}".format(package_indent, package_name)
            package = self.packages_dict.get(package_name)
            arch_string = ''
            if package:
                message += " {0} ({1})".format( package.version, package.arch)
                arch_string = " ( needs by {0} package) ".format(package.arch)
            message += ' has follow unresolved dependencies :\n'
            for type, type_data in data.items():
                for dep in type_data:
                    message += "{0} ({1}) {3} {4} {5} {2}\n"\
                        .format(dep_indent, type, arch_string, *dep)
            result += message
        return result
