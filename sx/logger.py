# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import logging
import time

import sx.utils as utils

__all__ = ["LOGGER", "info", "warning", "error", "critical"]

#{filename}.{tm_year}-{tm_mon}-{tm_mday}.{tm_hour}-{tm_min}-{tm_sec}.log
LOG_FILENAME_FORMAT = "{filename}.{0}-{1}-{2}.{3}-{4}-{5}.log"
LOG_FORMATTER_FORMAT = "%(asctime)s %(name)s %(levelname)s - %(message)s"
LOGGER = None
DEBUG = False

def create_logger(name, debug=False, filename='scalix-installer',
                 directory=None):

    logger = logging.getLogger(name)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if not filename:
        filename = name
    filename = LOG_FILENAME_FORMAT\
        .format(filename=filename,*time.localtime(time.time()))
    filename = utils.absolute_file_path(filename, directory, True)
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter(LOG_FORMATTER_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def logger_wrapper(func):
    def real_wrapper(*args, **kwargs):
        if LOGGER.isEnabledFor(logging.DEBUG) or kwargs.get('output', False):
            print(*args)
        return func(''.join([str(i) for i in args]).strip())
    return real_wrapper


@logger_wrapper
def info(message):
    LOGGER.info(message)

@logger_wrapper
def warning(message):
    LOGGER.warning(message)

@logger_wrapper
def error(message):
    LOGGER.error(message)

@logger_wrapper
def critical(message):
    LOGGER.critical(message)

