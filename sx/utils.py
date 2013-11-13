# -*- coding: utf-8 -*-
"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import


__author__ = 'pussbb'

import os

import sys
if sys.version_info[0] < 3:
    import imp
    imp.reload(sys)
    sys.setdefaultencoding("UTF-8")

import subprocess
import pipes

from sx.exceptions import ScalixExternalCommandFailed, \
    ScalixExternalCommandNotFound, ScalixExternalCommandException
import sx.logger as logger

def current_directory():
    """returns absolute file path to current module

    """
    return os.path.dirname(os.path.realpath(__file__))

def absolute_file_path(filename, directory=None, create_dir_if_needed=False):
    """

    @param filename:
    @param directory:
    @return:
    """
    if not directory:
        directory = current_directory()
    else:
        directory = os.path.realpath(directory)

    if not os.path.isdir(directory) and create_dir_if_needed:
        os.makedirs(directory)

    return os.path.join(directory, filename)


def properties_from_file(filename, replace_dots=False):
    """

    @rtype : dict
    @param filename:
    @param replace_dots:
    @return:
    """
    properties = {}
    for line in open(filename, 'r'):
        if line.startswith('#'):
            continue
        name, value = line.strip().split('=')
        if replace_dots:
            name = name.replace('.', '_')
        properties[name] = value
    return properties


def command_exists(command):
    """check if command present in system
    @param command string name of command
    @return True or False

    """
    try:
        execute(command)
        return True
    except ScalixExternalCommandException as exception:
        logger.warning("Command {0} not found ".format(command), exception)
        return False


BASH_CONDITIONS = (
    "|",
    "||",
    "&&",
    "&",
    ";",
    "$",
    "2>&1",
)

def bash_command(command, with_find=True):
    """helper function to inject bash command to find command for e.g.
    on some system command $ifconfig -a won't execute because need to
    use $/sbin/ifconfig -a

    """
    result = command
    if not command.startswith("$(") and not command.startswith("{"):
        template = "$(type -P {0})"
        if not with_find:
            template = "{{{0}}}"
        result = template.format(command)
    return result

def execute(*args, **kwargs):

    """
    Execute an external command and make sure it succeeded. Raises
    :py:class:`ScalixExternalCommandFailed` when the command exits with
    a nonzero exit code.

    :returns: the standard output of the external command
              is returned as a string.
    """

    # got one argument - list
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]

    command = [bash_command(args[0], kwargs.get('with_find', True))]
    escape = kwargs.get('escape', True)
    for item in args[1:]:
        if not item:
            continue
        if item[0] not in ["'", "\"", "$"] and \
            item not in BASH_CONDITIONS and escape:
            item = pipes.quote(item)
        command.append(item)

    command.append(';')

    command_string = " ".join(command)
    logger.debug("Executing cmd: ", command_string)

    shell = subprocess.Popen(command_string,
                             close_fds=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=None,
                             executable='/bin/bash',
                             shell=True,
                             universal_newlines=True)

    stdout, stderr = shell.communicate()

    if shell.returncode == 127:
        raise ScalixExternalCommandNotFound(command_string, shell.returncode,
                                          stdout, stderr)

    if shell.returncode != 0:
        raise ScalixExternalCommandFailed(command_string, shell.returncode,
                                          stdout, stderr)

    result = stdout or stderr

    return result.strip().split('\n')

if __name__ == "__main__":
    print(execute(["java", "-version"]))
    print(execute("java", "-help"))

