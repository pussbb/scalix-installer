# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function, unicode_literals, with_statement, \
    absolute_import

__author__ = 'pussbb'

import platform
import sys
import webbrowser
import socket
import re

from sx import utils
from sx.exceptions import ScalixExternalCommand, ScalixExternalCommandNotFound
import sx.logger as logger

UNAME_KEYS = [
    'system',
    'node',
    'release',
    'version',
    'machine',
    'processor'
]
"""
Supported platforms item's descripton
(
    'CentOS', # distro name
    '6', # version if needed specify concrete version just do it. e.g. 'Ubuntu'
    'Final', # distro abbreviation
    'x86_64', #platfrom architecture 32bit's or 64 bit's
    'rhel6' # packages release abbreviation
)

"""
SUPPORTED_PLATFORMS = (
    ('CentOS', '6', 'Final', 'x86_64', 'rhel6'),
    ('CentOS', '6', 'Final', 'x86', 'rhel6'),
    ('Ubuntu', '13.10', 'saucy', 'x86_64', '???'),
)

class System(object):

    def __init__(self):
        self.platform = sys.platform
        self.machine = None
        self.system = None
        self.node = None
        self.release = None
        self.version = None
        self.processor = None

        uname_data = platform.uname()
        for index, elem in enumerate(UNAME_KEYS):
            setattr(self, elem, uname_data[index])

        if self.is_linux():
            self.distro, self.distro_version, self.distro_abbr = \
            platform.linux_distribution()

    def __repr__(self):
        result = "System: {system}\nRelease: {release}\n" \
               "Version: {version}\nMachine: {machine}\n" \
               "Proccessor: {processor}".format(**self.__dict__)

        if self.is_linux():
            result = "{result}\nDistribution:{distro}" \
                     " {distro_version} ({distro_abbr})"\
                .format(result=result,**self.__dict__)

        return result

    def is_linux(self):
        return self.platform.startswith('linux')

    def is_64bit(self):
        return self.machine == 'x86_64'

    def is_32bit(self):
        return self.machine in ['i386', 'i586', 'i686',]

    def is_supported(self):
        current_platform = ()
        if self.is_linux():
            current_platform = (self.distro, self.distro_version, self.machine)

        for supported_platform in SUPPORTED_PLATFORMS:
            if current_platform[0] != supported_platform[0]:
                continue
            if not current_platform[1].startswith(supported_platform[1]):
                continue
            if current_platform[2] != supported_platform[3]:
                continue
            return True

        return False

    @staticmethod
    def command_exists(command):
        try:
            utils.execute(command, with_find=False)
            return True
        except ScalixExternalCommandNotFound as exception:
            logger.warning("Command {0} not found ".format(command), exception)
            return False

    @staticmethod
    def run_level():
        try:
            result = utils.execute("runlevel", "|", utils.bash_command("gawk"),
                                   "'{print $2}'")
            return int(result[0])
        except ScalixExternalCommand as exception:
            logger.critical("Could not get run level", exception)
            return -1

    @staticmethod
    def memory_total():
        try:
            #gawk '/MemTotal/ { print $2 }' /proc/meminfo
            return int(utils.execute("gawk", "'/MemTotal/ { print $2 }'",
                               "/proc/meminfo")[0])
        except ScalixExternalCommand as exception:
            logger.critical("Could not get total memory", exception)
            return -1

    @staticmethod
    def memory_free():
        try:
            #"gawk '/MemFree/ { print $2 }' /proc/meminfo"
            return int(utils.execute("gawk", "'/MemFree/ { print $2 }'",
                               "/proc/meminfo")[0])
        except ScalixExternalCommand as exception:
            logger.critical("Could not get free memory", exception)
            return -1

    @staticmethod
    def memory():
        return System.memory_total(), System.memory_free()

    @staticmethod
    def partition_size(folder):
        try:
            #"df -lP %s | gawk '{print $4}'"
            result = utils.execute("df", "-lP", folder, "|",
                                   utils.bash_command("gawk"), "'{print $4}'")
            try:
                return int(result[1])
            except (UnicodeEncodeError, ValueError) as exception:
                logger.critical("Could not get partition size", exception,
                                result)
                return -1
        except ScalixExternalCommand as exception:
            logger.critical("Could not get partition size", exception)
            return -1

    @staticmethod
    def disk_space(*args):
        if not args:
            return System.partition_size('/')
        result = []
        for partition in args:
            result.append(System.partition_size(partition))
        return result

    @staticmethod
    def open_url(url):
        try:
            return webbrowser.open(url, new=1)
        except webbrowser.Error as exception:
            logger.critical("Couldn't open browser", exception, " url ", url)
            return False

    @staticmethod
    def listening_port(port):
        """

        @param port: port number integer
        @return: on success tulip which contain
        (Proto, Recv-Q, Send-Q, Local Address, Foreign Address, State)
        or False
        """

        try:
            result = utils.execute("netstat", "-ln", "|",
                                   utils.bash_command("grep"),
                                   ":{0:d}[^0-9]".format(port))
            return (i for i in result[0].strip().split())

        except ScalixExternalCommand as exception:
            logger.warning("Could not get port is listening ", exception)
        return ()


    @staticmethod
    def get_FQDN():
        return socket.getfqdn()

    @staticmethod
    def is_FQDN():
        pattern = r'^[a-zA-Z0-9\-\.]+\.([0-9a-zA-Z]+)$'
        return re.match(pattern, System.get_FQDN()) != None

    @staticmethod
    def get_ips():
        #print(socket.gethostbyname(socket.gethostname()))
        try:
            lines = utils.execute("ip", "address", "|",
                                  utils.bash_command("grep"),
                                  "[[:space:]]inet[[:space:]]")

            pattern = r"inet\s(\d{1,3}[^127|^192]\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            result = []
            for line in lines:
                match = re.match(pattern, line.strip())
                if match:
                    result.append(match.group(1))
            return result

        except ScalixExternalCommand as exception:
            logger.warning("Could not get ips ", exception)
            return False

    @staticmethod
    def get_mx_records(domain):
        try:
            lines = utils.execute("dig", "-t", "MX", "+short", domain)
            return [i.strip() for i in lines]
        except ScalixExternalCommand as exception:
            logger.warning("Could not get MX records ", exception)
            return False

    @staticmethod
    def get_java_version(raw=False):
        try:
            lines = utils.execute("java", "-version")
            if raw or not lines:
                return lines
            version = re.search(r'^java version "(.*)"$', lines[0].strip())
            if version:
                return version.group(0)
        except ScalixExternalCommand as exception:
            logger.warning("Could not get java version", exception)

    @staticmethod
    def is_ibm_j2sdk():
        result = re.search(r'IBM\s(\w+)\sVM',
                           '\n'.join(System.get_java_version(raw=True) or []),
                           re.I | re.M)
        return result != None

    @staticmethod
    def determine_ip():
        ip_list = socket.gethostbyaddr(System.get_FQDN())[2]
        if ip_list:
            return ip_list[0]
        return '127.0.0.1'

    @staticmethod
    def determine_interface(ip):

        try:
            lines = utils.execute("ip", "addr", "show", "|",
                                  utils.bash_command("grep"),
                                  "[[:space:]]inet[[:space:]]{0}/".format(ip),
                                  "|", utils.bash_command("head"), "-1", "|",
                                  utils.bash_command("gawk"), "'{ print $NF }'")
            if lines:
                return lines[0].strip()

        except ScalixExternalCommand as exception:
            logger.warning("Could not determine interface", exception)
            return False
