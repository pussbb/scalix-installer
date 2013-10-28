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

from sx.exceptions import ScalixExternalCommandFailed
import sx.logger as logger

def current_directory():
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

BASH_CONDITIONS = (
    "|",
    "||",
    "&&",
    "&",
    ";",
    "$",
    "2>&1",
)

def bash_command(command):
    if command.startswith("$(type"):
        return command
    return "$(type -P {cmd})".format(cmd=command)

def execute(*args, **kwargs):

    """
    Execute an external command and make sure it succeeded. Raises
    :py:class:`ScalixExternalCommandFailed` when the command exits with
    a nonzero exit code.

    :returns: the standard output of the external command
              is returned as a string.
    """

    # got one argument - list
    if len(args) == 1 and not isinstance(args[0], basestring):
        args = args[0]

    command = [bash_command(args[0])]

    for item in args[1:]:
        if not item:
            continue
        if item[0] not in ["'", "\"", "$"] and \
            item not in BASH_CONDITIONS :
            item = pipes.quote(item)
        command.append(item)

    command.append(';')

    logger.debug("Executing cmd: "," ".join(command))

    shell = subprocess.Popen(" ".join(command),
                             close_fds=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=None,
                             executable='/bin/bash',
                             shell=True,
                             universal_newlines=True)

    stdout, stderr = shell.communicate()

    if shell.returncode != 0:
        message = "External command failed with exit code {code}!" \
                  " (command: {cmd})\n With message:\n {msg} \n"\
            .format(cmd=command, code=shell.returncode,msg=stderr)
        logger.debug("Executing cmd failed: ", message)
        raise ScalixExternalCommandFailed(message, stdout, stderr)

    result = stdout or stderr
    return result.strip().split('\n')

if __name__ == "__main__":
    print(execute(["java", "-version"]))
    print(execute("java", "-help"))

