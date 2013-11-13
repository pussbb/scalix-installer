# -*- coding: utf-8 -*-

""" Module to manipulate with services in system

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import


__author__ = 'pussbb'

import sx.utils as utils
from sx.exceptions import ScalixExternalCommandException
from sx.service import AbstractServiceManager, AbstractService, is_root
from sx.service.tomcat import ScalixTomcatService


class DebServiceManager(AbstractServiceManager):

    def __init__(self, services=None):
        if services:
            services = dict(services.items() + self.__services().items())
        else:
            services =  self.__services()
        AbstractServiceManager.__init__(self, services)

    @is_root
    def enable(self, service):
        try:
            utils.execute('update-rc.d', str(service), 'defaults')
        except ScalixExternalCommandException as exception:
            return False
        return True

    @is_root
    def disable(self, service):
        try:
            utils.execute('update-rc.d', '-f', str(service), 'remove')
        except ScalixExternalCommandException as exception:
            return False
        return True

    def __services(self):
        return {
            'apache': AbstractService('apache2'),
            'sxpostgress': AbstractService('scalix-postgres'),
            'sxserver': AbstractService('scalix'),
            'sxtomcat': ScalixTomcatService(),
            'ldapmapper': AbstractService('ldapmapper'),
            'stunnel': AbstractService('stunnel')
        }

class RHELServiceManager(AbstractServiceManager):

    def __init__(self, services=None):
        if services:
            services = dict(services.items() + self.__services().items())
        else:
            services =  self.__services()
        AbstractServiceManager.__init__(self, services)

    def __services(self):
        return {
            'apache': AbstractService('httpd'),
            'sxpostgress': AbstractService('scalix-postgres'),
            'sxserver': AbstractService('scalix'),
            'sxtomcat': ScalixTomcatService(),
            'ldapmapper': AbstractService('ldapmapper'),
            'stunnel': AbstractService('stunnel')
        }
