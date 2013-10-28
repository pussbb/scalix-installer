# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import os

import sx.package.drivers.deb as Deb
import sx.package.drivers.rpm as Rpm

class PackageManager(object):

    def __init__(self, system):
        self.system = system
        self.packages = self.__packages_list()

    def __packages_list(self):
        result = {}
        for driver in [Deb,Rpm]:
            if not driver.is_available():
                continue
            result[driver.file_extention()] = {
                'noarch': {},
                'sources': {},
                'other': {},
            }

        return result

    def scan_folder(self, folder):
        self.packages = self.__packages_list()
        for root, _, files in os.walk(folder, followlinks=True):
            for file_ in files:
                if file_.endswith('rpm'):
                    Rpm.RpmFile(os.path.join(root, file_))
                #print(file_)
