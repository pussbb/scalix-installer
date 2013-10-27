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


def execute(*args, **kwargs):

    """
    Execute an external command and make sure it succeeded. Raises
    :py:class:`ScalixExternalCommandFailed` when the command exits with
    a nonzero exit code.

    :returns: the standard output of the external command
              is returned as a string.
    """

    # got one argument - list
    if len(args) == 1:
        args = args[0]

    command = [
        "$(type -P {cmd})".format(cmd=args[0])
    ]

    for item in args[1:]:
        if kwargs.get('escape', False):
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
        raise ScalixExternalCommandFailed(message)
    result = stdout or stderr
    return result.strip().split('\n')

if __name__ == "__main__":
    print(execute(["java", "-version"]))
    print(execute("java", "-help"))

