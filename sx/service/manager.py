# -*- coding: utf-8 -*-

""" Module to manipulate with services in system

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import


__author__ = 'pussbb'

from sx.service import AbstractServiceManager, AbstractService
from sx.service.tomcat import ScalixTomcatService

class DebServiceManager(AbstractServiceManager):

    def _init_services(self):
        self._services = {
            'apache': AbstractService('apache2'),
            'sxpostgress': AbstractService('scalix-postgres'),
            'scalix': AbstractService('scalix'),
            'sxtomcat': ScalixTomcatService(),
            'ldapmapper': AbstractService('ldapmapper'),
            'stunnel': AbstractService('stunnel')
        }

