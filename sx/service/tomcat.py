# -*- coding: utf-8 -*-

""" Module to manipulate with services in system

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import


__author__ = 'pussbb'

from sx.service import AbstractService

class ScalixTomcatService(AbstractService):

    def __init__(self, name):
        super(AbstractService, self).__init__("scalix-tomcat")
