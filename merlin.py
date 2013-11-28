# -*- coding: utf-8 -*-
"""Scalix Installer.

Usage:
  merlin.py [--cli] [--pkgdir=<pkgdir>] [--logdir=<logdir>] \
[--instance=<instance_name>] [--hostname=<hostname>] [--no-root]
  merlin.py (-h | --help)
  merlin.py --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --cli                         Console only application
  --pkgdir=<pkgdir>             Directory with packages to install or upgrade
  --logdir=<logdir>             Directory for log file [default: ../logs/]
  --instance=<instance_name>    Scalix Instance name
  --hostname=<hostname>         Set hostname
  --no-root                     No root
"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'


import os

import sys
sys.path.append(os.path.dirname(__file__))

from sx.exceptions import ScalixException, ScalixPackageException, \
    ScalixUnresolvedDependencies, ScalixPackageProblems
import sx.version as version
import sx.logger as logger
from sx.system import System
from sx.package.manager import PackageManager
from sx import utils

def service_test(system):
    print(system.service_manager.available())
    apache_service = system.service_manager.apache
    print(apache_service.exists)
    print(apache_service.commands)
    print(apache_service('restart'))
    print(apache_service.is_running())
    print(apache_service.run_levels())
    print(system.service_manager.enable(apache_service))
    print(apache_service.run_levels())
    print(system.service_manager.disable(apache_service))
    print(apache_service.run_levels())


def package_manager_test(system):

    pm = PackageManager(system)
    pm.scan_folder('../products/')
    print(repr(pm))
    return
    try:
        for package in pm.packages:
            if not package.installed:
                package.install = True
            else:
                package.unistall = True
        pm.proccess()

    except ScalixPackageException as exception:
        if isinstance(exception, ScalixUnresolvedDependencies):
            print(pm.format_dependencies(exception.dependecies))
        elif isinstance(exception, ScalixPackageProblems):
            print(pm.format_problems(exception.problems))
        else:
            # some unexpected exception
            raise
    #print(repr(pm))

def system_tests(system):
    #print(System.command_exists('wipe'))
    print(system.determine_interface(System.determine_ip()))
    print(system.determine_ip())
    print(System.get_java_version())
    print(System.is_ibm_j2sdk())
    print(system.get_mx_records('allwebsuite.com'))
    print(system.get_ips())
    print(System.get_fqdn())
    print(System.is_fqdn())
    print(*system.listening_port(80))
    print("supported", system.is_supported())
    print("run level", system.run_level())
    mem = system.memory()
    print("Memory (total, free)", [utils.size2human(i) for i in mem])
    print([utils.size2human(i) for i in system.disk_space('/', '/opt')])
    #print(System.open_url('http://python.org/'))

def init_logger(args):
    logger.init_logger('Merlin', directory=args['--logdir'])

    logger.info("Initializing Installer version", version.get_version(),
                output=True)
    logger.info("Using log file", logger.logger_filename(), output=True)

def main(args, system):

    if not args['--no-root'] and os.geteuid() != 0:
        raise ScalixException('Error: You need to be root or superuser to run this application')

    if 'DISPLAY' not in os.environ:
        args["--cli"] = True

    # Process Instance
    if args["--instance"]:
        os.environ["OMCURRENT"] = args["--instance"]

    # Process Hostname
    if args["--hostname"]:
        os.environ["OMHOSTNAME"] = args["--hostname"]


if __name__ == '__main__':
    from docopt import docopt

    ARGS = docopt(__doc__, version=version.get_version())
    init_logger(ARGS)
    system = System()
    logger.info('Running on:\n', system, output=True)
    try:
        #main(ARGS, system)
        #system_tests(system)
        package_manager_test(system)
        #service_test(system)
    except:
        raise
    finally:
        if __debug__:
            pass#os.remove(logger.logger_filename(base_name=False))

