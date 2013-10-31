# -*- coding: utf-8 -*-
"""Scalix Installer.

Usage:
  merlin.py [--cli] [--debug] [--pkgdir=<pkgdir>] [--logdir=<logdir>] \
[--instance=<instance_name>] [--hostname=<hostname>] [--no-root]
  merlin.py (-h | --help)
  merlin.py --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --cli                         Console only application
  --debug                       Show debug information
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

from sx.exceptions import ScalixException, ScalixUnresolvedDependencies
import sx.version as version
import sx.logger as logger
from sx.system import System
from sx.package.manager import PackageManager

def test(args):
    logger.LOGGER = logger.create_logger('Merlin', directory=args['--logdir'],
                                         debug=args['--debug'])

    logger.info("Initializing Installer version", version.get_version(),
                output=True)
    s = System()

    pm = PackageManager(s)
    #pm.scan_folder('/opt/hg/scalix_server/dist/rpm/')
    #print(pm.__dict__)
    pm.scan_folder('../products/')
    try:
        pm.proccess(*pm.packages)
    except ScalixUnresolvedDependencies as exception:
        print(pm.format_dependencies(exception.dependecies))
    #print(repr(pm))



    return
    print(System.command_exists('wipe'))
    print(System.determine_interface(System.determine_ip()))
    print(System.determine_ip())
    print(System.get_java_version())
    print(System.is_ibm_j2sdk())
    print(System.get_mx_records('allwebsuite.com'))
    print(System.get_ips())
    print(System.get_FQDN())
    print(System.is_FQDN())
    print(*System.listening_port(80))
    print("supported", s.is_supported())
    print("run level", System.run_level())
    print("Memory (total, free)", System.memory())
    print(System.disk_space('/', '/opt'))
    #print(System.open_url('http://python.org/'))

def main(args):
    logger.LOGGER = logger.create_logger('Merlin', directory=args['--logdir'],
                                         debug=args['--debug'])

    logger.info("Initializing Installer version", version.get_version(),
                output=True)
    s = System()
    logger.info('Running on:\n', s, output=True)

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
    #main(ARGS)
    test(ARGS)
