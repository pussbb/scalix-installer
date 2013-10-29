# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import os

from sx.package.base.deb import DEB
from sx.package.base.rpm import RPM

class PackageManager(object):

    def __init__(self, system):
        self.system = system
        self.package_drivers = []
        for driver in [DEB, RPM]:
            if not driver.available:
                continue
            self.package_drivers.append(driver)


    def scan_folder(self, folder):

        for root, _, files in os.walk(folder, followlinks=True):
            for file_ in files:

                for driver in self.package_drivers:
                    if file_.endswith(driver.file_extention):
                        driver.package(os.path.join(root, file_))
                #print(file_)
