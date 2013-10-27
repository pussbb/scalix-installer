# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'


class ScalixException(Exception):
    """ Base Exception"""
    pass

class ScalixLicenseError(ScalixException):
    """An exception type used to indicate a problem reading,
    validating, or installing the license.

    """
    pass

class ScalixProcessingException(ScalixException):
    """An exception to be used as a trigger to reset state in a function.
    For example, if a variable may need reset to "None" or the function
    return if any of several problems occur, rather than handle each
    individually, they can be grouped into a try/catch block.

    """
    pass


class ScalixExternalCommandFailed(Exception):
    """
    Raised by :py:func:`execute()` when an external command returns with a
    nonzero exit code.
    """
