# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import os

from sx.package.base.deb import DEB
from sx.package.base.rpm import RPM
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
                if file_.endswith(self.system.package_manager.file_extention):
                    self.__add_package(root, file_, packages)
        #print(repr(packages))
        self.packages_dict = packages
        self.packages = self.system.package_manager.order(packages)

    def __add_package(self, directory, filename, packages):
        file_ = utils.absolute_file_path(filename, directory)
        package = self.system.package_manager.package(file_)

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
            .format(repr(self.system.package_manager))

        result += "Available packages:\n"
        indent = " "*10
        packages = self.packages[:]
        #packages.reverse()
        for package in packages:
            result += "{0} - {1}\n\n".format(" "*5, package.__repr__(indent))
        return result
