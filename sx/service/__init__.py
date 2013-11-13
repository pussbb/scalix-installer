# -*- coding: utf-8 -*-

""" Module to manipulate with services in system
ls -l /etc/rc?.d/*apache2

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import


__author__ = 'pussbb'

import os
import re

import sx.utils as utils
import sx.logger as logger

from sx.exceptions import ScalixExternalCommandFailed,\
    ScalixExternalCommandException

def is_root(func):
    def real_wrapper(self, *args, **kwargs):
        if os.geteuid() != 0:
            raise OSError('You must be a root user')
        return func(self, *args, **kwargs)
    return real_wrapper

def service_support(cmd):
    def wrapper_func(func):
        def real_wrapper(self, *args, **kwargs):
            if cmd and cmd not in self.commands:
                raise NotImplementedError("Service {name} does not support {cmd}"
                    .format(name=self.name, cmd=cmd))
            return func(self, *args, **kwargs)
        return real_wrapper
    return wrapper_func

class AbstractServiceManager(object):

    CHCONF_AVAILABLE = utils.command_exists('chkconfig')

    def __init__(self, services):
        self._services = services

    def __getattr__(self, item):
        service = self._services.get(item)
        if not service:
            raise AttributeError(item)
        return service

    @is_root
    def enable(self, service):
        if not AbstractServiceManager.CHCONF_AVAILABLE:
            raise NotImplementedError()
        try:
            cmd = ['chkconfig', '--level', '345', str(service), 'on']
            utils.execute(cmd)
        except ScalixExternalCommandFailed as exception:
            return False
        return True

    @is_root
    def disable(self, service):
        if not AbstractServiceManager.CHCONF_AVAILABLE:
            raise NotImplementedError()
        try:
            utils.execute('chkconfig', '--del', str(service))
        except ScalixExternalCommandFailed as exception:
            return False
        return True

    def available(self):
        result = []
        for name, service in self._services.iteritems():
            if service.exists:
                result.append(name)
        return result


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
            output = exception.stderr or exception.stdout
            commands = output.split(' ')[-1].strip()
            commands = commands.strip('{}')
            self.commands = [arg.strip() for arg in commands.split('|')]
            self.__exists = True

    @is_root
    def run_levels(self):
        levels = []
        if AbstractServiceManager.CHCONF_AVAILABLE:
            try:
                lines = utils.execute('chkconfig', '--list', self.name)
                levels = re.findall('(\d)\:on', lines[0])
            except ScalixExternalCommandFailed as exception:
                # got message service * supports chkconfig,
                # but is not referenced in any runlevel
                # (run 'chkconfig --add httpd')
                pass
        else:
            cmd = [ 'ls', '-1',
                    '/etc/rc?.d/*{0}'.format(self.name)]
            lines = utils.execute(cmd, escape=False)
            levels = [line[7] for line in lines]
        return levels

    @is_root
    def __call__(self, *args):
        cmd = [
            'service',
            self.name
        ]
        if args[0] not in self.commands:
            raise NotImplementedError("Service {name} does not support {cmd}"
                .format(name=self.name, cmd=args[0]))
        cmd.append(*args)
        try:
            return utils.execute(cmd)
        except ScalixExternalCommandException as exception:
            logger.critical("Service init failed ", exception)

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
        return not lines

    @is_root
    @service_support('restart')
    def restart(self):
        try:
            return utils.execute('service', self.name, 'restart')
        except ScalixExternalCommandException as exception:
            logger.critical("failed to restart service", exception)

    @is_root
    @service_support('start')
    def start(self):
        try:
            return utils.execute('service', self.name, 'start')
        except ScalixExternalCommandException as exception:
            logger.critical("failed to start service", exception)

    @is_root
    @service_support('stop')
    def stop(self):
        try:
            return utils.execute('service', self.name, 'stop')
        except ScalixExternalCommandException as exception:
            logger.critical("failed to stop service", exception)

    @is_root
    @service_support('reload')
    def reload(self, force=False):
        if force:
            return self.force_reload()
        try:
            return utils.execute('service', self.name, 'reload')
        except ScalixExternalCommandException as exception:
            logger.critical("failed to reload service", exception)

    @is_root
    @service_support('status')
    def status(self):
        try:
            return utils.execute('service', self.name, 'status')[0]
        except ScalixExternalCommandException as exception:
            logger.critical("failed to get status of the service", exception)

    @is_root
    @service_support('force-reload')
    def force_reload(self):
        try:
            return utils.execute('service', self.name, 'force-reload')
        except ScalixExternalCommandException as exception:
            logger.critical("failed to force-reload service", exception)
