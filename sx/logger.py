# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import logging
import time
import os

import sx.utils

__all__ = ["LOGGER", "info", "warning", "error", "critical", "debug",
           "is_debug"]

#{filename}.{tm_year}-{tm_mon}-{tm_mday}.{tm_hour}-{tm_min}-{tm_sec}.log
LOG_FILENAME_FORMAT = "{filename}.{0}-{1}-{2}.{3}-{4}-{5}.log"
LOG_FORMATTER_FORMAT = "%(asctime)s %(name)s %(levelname)s - %(message)s"

LOGGER = logging.getLogger(__name__)

def create_logger(name, debug_mode=False, filename='scalix-installer',
                 directory=None):
    """create logging instance

    @return logging instance

    """
    logger = logging.getLogger(__name__)
    if debug_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if not filename:
        filename = name
    filename = LOG_FILENAME_FORMAT\
        .format(filename=filename,*time.localtime(time.time()))
    filename = sx.utils.absolute_file_path(filename, directory, True)
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter(LOG_FORMATTER_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def is_debug():
    """ if debug mode enabled

    """
    return LOGGER and LOGGER.isEnabledFor(logging.DEBUG)

def logger_handler():
    """returns default loging handler

    """
    return LOGGER.handlers[0]

def logger_stream():
    """returns stream for a default loging handler

    """
    return logger_handler().stream

def logger_filename(base_name=True):
    """ returns a log file name or full path to that file

    """
    filename = logger_handler().baseFilename
    if base_name:
        filename = os.path.basename(filename)
    return filename

def logger_wrapper(func):
    """ helper wrapper if debug mode is on it will also output massage into
    stdout

    """
    def real_wrapper(*args, **kwargs):
        list_ = []
        debug_mode = is_debug()
        for item in args:
            if isinstance(item, object) and debug_mode:
                item = repr(item)
            else:
                item = str(item)
            list_.append(item)

        if is_debug() or kwargs.get('output', False):
            print(*list_)
        return func(' '.join(list_).strip())
    return real_wrapper

@logger_wrapper
def debug(*args):
    """write massge to log file with DEBUG level

    """
    if not is_debug():
        return
    LOGGER.info(*args)

@logger_wrapper
def info(*args):
    """write massge to log file with INFO level

    """
    LOGGER.info(*args)

@logger_wrapper
def warning(*args):
    """write massge to log file with WARNING level

    """
    LOGGER.warning(*args)

@logger_wrapper
def error(*args):
    """write massge to log file with ERROR level

    """
    LOGGER.error(*args)

@logger_wrapper
def critical(*args):
    """write massge to log file with CRITICAL level

    """
    LOGGER.critical(*args)

