# -*- coding: utf-8 -*-

"""

"""

from __future__ import unicode_literals

__author__ = 'pussbb'

class ScalixException(Exception):
    """ Base Exception"""

    def __repr__(self):
        return u"{0}: {1}".format(self.__class__.__name__, unicode(self.__dict__).encode())

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

class ScalixExternalCommand(ScalixException):
    """Base exception class for executing external commands in shell

    """
    def __init__(self, command, exit_code, stdout, stderr):
        message = "External command failed with exit code {code}!" \
                  " (command: {cmd})\n With message:\n {msg} \n"\
            .format(cmd=command, code=exit_code, msg=stderr or stdout)

        super(ScalixException, self).__init__(message)
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code



class ScalixExternalCommandNotFound(ScalixExternalCommand):
    """Command not found

    """
    pass

class ScalixExternalCommandFailed(ScalixExternalCommand):
    """
    Raised by :py:func:`execute()` when an external command returns with a
    nonzero exit code.
    """

    pass
