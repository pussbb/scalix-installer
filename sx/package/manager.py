# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import os
import sys

from sx.package.base.deb import DEB
from sx.package.base.rpm import RPM

from sx.package import *

import sx.utils as utils

class PackageManager(object):
    """ Class to manipulate with packages
    get packages from directory, check if package for system etc.
    """

    def __init__(self, system):
        self.system = system
        self.packages = []
        self.packages_dict = {}

    @staticmethod
    def available_drivers(self):
        """returns list of available drivers

        """
        return [driver for driver in [DEB, RPM] if driver.available]

    def scan_folder(self, folder):
        """scan folder recursively for package and add them._

        @param folder - string

        """
        packages = {}
        self.packages_dict = {}
        del self.packages[:]
        self.system.packager.clear()
        for root, _, files in os.walk(folder, followlinks=True):
            for file_ in files:
                if file_.endswith(self.system.packager.file_extention):
                    self.__add_package(root, file_, packages)

        self.packages_dict = packages
        #make ordere list of packages
        for name in self.system.packager.order(packages):
            self.packages.append(self.packages_dict[name])

    def __add_package(self, directory, filename, packages):
        """append package to the list if it can be installed/upgraded in system

        @param directory - string
        @param filename - string
        @param package - temprory list

        """
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
        """checks if  package for platform

        @param package - instance of AbstractPackageFile

        """
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

    @staticmethod
    def default_proccess_callback(reason, filename, precents=0):
        """default callback function for installation proccess

        """

        if reason == PKG_INST_START:
            print("Installing {0}     ".format(filename))
        elif reason == PKG_INST_PROGRESS:
            print("\b\b\b%d%s" % (precents, '%'), end="")
        elif reason == PKG_INST_STOP:
            print(" Done!")
        elif reason == PKG_UNINST_START:
            print("Uninstalling {0} ".format(filename), end=" ")
        elif reason == PKG_UNINST_PROGRESS:
            print("\b\b\b%d%s" % (precents, '%'), end=" ")
        elif reason == PKG_UNINST_STOP:
            print(" Done!")

    def proccess(self, callback=None):
        """proccess install/upgrade or uninstall packages

        """

        if callback is None:
            callback = PackageManager.default_proccess_callback

        for package in self.packages:
            if package.install or package.upgrade:
                self.system.packager.add(package)
            elif package.unistall:
                self.system.packager.uninstall(package)

        self.system.packager.run(callback)


    def format_dependencies(self, dependecies):
        """help

            package_name {
                'require': [
                    (pack, '>=', ver),
                    ()
                ]
                'conflicts':[
                    (pack, '>=', ver),
                    ()
                ]
            }
        """
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
            message += ' has following unresolved dependencies :\n'
            for type, type_data in data.items():
                for dep in type_data:
                    message += "{0} ({1}) {3} {4} {5} {2}\n"\
                        .format(dep_indent, type, arch_string, *dep)
            result += message
        return result

    def format_problems(self, problems):
        """

        """
        result = "Following problems occurred with packages:\n"
        package_indent = " " * 5
        problem_indent = package_indent * 5
        for package_name, data in problems.items():
            item = "{0}{1} has following problems:\n".format(package_indent,
                                                             package_name)
            for problem in data:
                item += "{0}{1}\n".format(problem_indent, problem)
            result += item
        return result
