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

from sx.exceptions import ScalixException
import sx.version as version
import sx.logger as logger
from sx.system import System

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
    main(ARGS)
