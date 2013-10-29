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

        self.package_manager = self.system.package_manager


    def scan_folder(self, folder):

        for root, _, files in os.walk(folder, followlinks=True):
            for file_ in files:
                if file_.endswith(self.package_manager.file_extention):
                    self.package_manager.package(os.path.join(root, file_))
                #print(file_)
