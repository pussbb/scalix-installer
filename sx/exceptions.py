# -*- coding: utf-8 -*-

"""

"""

from __future__ import unicode_literals

__author__ = 'pussbb'

class ScalixException(Exception):
    """ Base Exception"""

    def __repr__(self):
        return "{0}: {1}".format(self.__class__.__name__, repr(self.__dict__))

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


class ScalixExternalCommandFailed(ScalixException):
    """
    Raised by :py:func:`execute()` when an external command returns with a
    nonzero exit code.
    """

    def __init__(self, message, stdout=None, stderr=None):
        super(self.__class__, self).__init__()
        self.message = message
        self.stdout = stdout
        self.stderr = stderr


