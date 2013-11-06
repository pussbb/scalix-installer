# -*- coding: utf-8 -*-

""" Module to manipulate with services in system

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import


__author__ = 'pussbb'

import os

import sx.utils as utils
from sx.exceptions import ScalixExternalCommandFailed

class AbstractServiceManager(object):

    def __init__(self):
        self._services = {}
        self._init_services()

    def __getattr__(self, item):
        service = self._services.get(item)
        if not service:
            raise AttributeError()
        return service

    def _init_services(self):
        raise NotImplementedError()

    def enabled(self, service):
        pass

    def enable(self, service):
        raise NotImplementedError()

    def disable(self, service):
        raise NotImplementedError()

    def available(self):
        return self._services.keys()

def is_root_wrapper(func):
    def real_wrapper(self, *args, **kwargs):
        if os.geteuid() != 0:
            raise OSError('You must be a root user')
        return func(self, *args, **kwargs)
    return real_wrapper

def service_cmd_available(cmd):
    def wrapper_func(func):
        def real_wrapper(self, *args, **kwargs):
            if cmd and cmd not in self.commands:
                raise NotImplementedError("Service {name} does not support {cmd}"
                    .format(name=self.name, cmd=cmd))
            return func(self, *args, **kwargs)
        return real_wrapper
    return wrapper_func

class AbstractService(object):
    """General class for services

    """

    def __init__(self, name):
        self.name = name
        self.__exists = False
        self.commands = []

        try:
            utils.execute('service', self.name)
        except ScalixExternalCommandFailed as exception:
            if exception.exit_code == 3:
                commands = exception.stderr.split(' ')[-1].strip()
                commands = commands.strip('{}')
                self.commands = [arg.strip() for arg in commands.split('|')]
                self.__exists = True

    @is_root_wrapper
    def __call__(self, *args):
        cmd = [
            'service',
            self.name
        ]
        if args[0] not in self.commands:
            raise NotImplementedError("Service {name} does not support {cmd}"
                .format(name=self.name, cmd=args[0]))
        cmd.append(*args)
        return utils.execute(cmd)

    def __str__(self):
        return self.name

    @property
    def exists(self):
        return self.__exists

    def is_running(self):
        cmd = [
            'ps',
            'aux',
            '|',
            utils.bash_command('grep'),
            "$(echo '{0}' | sed s/^\(.\)/[\\1]/g )".format(self.name)
        ]
        lines = utils.execute(cmd)
        if not lines:
            return False
        return True

    @is_root_wrapper
    @service_cmd_available('restart')
    def restart(self):
        return utils.execute('service', self.name, 'restart')

    @is_root_wrapper
    @service_cmd_available('start')
    def start(self):
        return utils.execute('service', self.name, 'start')

    @is_root_wrapper
    @service_cmd_available('stop')
    def stop(self):
        return utils.execute('service', self.name, 'stop')

    @is_root_wrapper
    @service_cmd_available('reload')
    def reload(self, force=False):
        if force:
            return self.force_reload()
        return utils.execute('service', self.name, 'reload')

    @is_root_wrapper
    @service_cmd_available('status')
    def status(self):
        return utils.execute('service', self.name, 'status')[0]

    @is_root_wrapper
    @service_cmd_available('force_reload')
    def force_reload(self):
        return utils.execute('service', self.name, 'force-reload')
