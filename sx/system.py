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

from sx.package.base.rpm import RPM
from sx.package.base.deb import DEB
from sx.service.manager import DebServiceManager

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
    'rpm' # system package manager
)

"""

SUPPORTED_PLATFORMS = (
    ('CentOS', '6', 'Final', ['x86_64', 'i686'], 'rhel6', RPM),

    ('Ubuntu', '13.10', 'saucy', ['x86_64'], 'rhel6', RPM, DebServiceManager()), # '???', DEB
)

class System(object):
    """General class to get information about system on which script is running

    """

    def __init__(self):
        self.platform = sys.platform
        self.__supported = False
        self.packager = None
        self.target_platform = None
        self.service_manager = None

        if not self.is_linux():
            return

        uname_data = platform.uname()
        for index, elem in enumerate(UNAME_KEYS):
            setattr(self, elem, uname_data[index])

        self.arch = self.machine

        self.distro, self.distro_version, self.distro_abbr = \
            platform.linux_distribution()

        extra_data = self.__get_extra_data_if_supported()
        if extra_data:
            self.__supported = True
            self.service_manager = extra_data[-1]
            self.packager = extra_data[-2]
            self.target_platform = extra_data[-3]


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
        """ check is linux

        """
        return self.platform.startswith('linux')

    def is_64bit(self):
        """ is system 64 bit

        @rtype bool
        return True or False

        """
        return self.arch == 'x86_64'

    def is_32bit(self):
        """is system 32 bit

        @rtype bool
        return True or False

        """
        return self.arch in ['i386', 'i586', 'i686',]

    def is_supported(self):
        """ is supported

        @rtype bool
        return True or False

        """
        return self.__supported

    def __get_extra_data_if_supported(self):
        """ if platform supported let's get some additional data(instance of
        packager etc)
        """
        current_platform = (self.distro, self.distro_version, self.arch)
        for supported_platform in SUPPORTED_PLATFORMS:
            if current_platform[0] != supported_platform[0]:
                continue
            if not current_platform[1].startswith(supported_platform[1]):
                continue
            if current_platform[2] not in supported_platform[3]:
                continue
            return supported_platform

        return ()

    @staticmethod
    def command_exists(command):
        """check if command present in system
        @param command string name of command
        @return True or False

        """
        try:
            utils.execute(command, with_find=False)
            return True
        except ScalixExternalCommandNotFound as exception:
            logger.warning("Command {0} not found ".format(command), exception)
            return False

    @staticmethod
    def run_level():
        """Returns run level on linux

        @rtype: int
        @return int if could not determine run level it will return -1

        """
        try:
            cmd = ["runlevel", "|", utils.bash_command("gawk"), "'{print $2}'"]
            return int(utils.execute(cmd)[0])
        except ScalixExternalCommand as exception:
            logger.critical("Could not get run level", exception)
            return -1

    @staticmethod
    def memory_total():
        """ get total memory in system(linux only)

        @rtype int
        @return total memory or -1 if something went wrong

        """
        try:
            #gawk '/MemTotal/ { print $2 }' /proc/meminfo
            result = utils.execute("gawk", "'/MemTotal/ { print $2 }'",
                               "/proc/meminfo")
            return int(result[0])
        except ScalixExternalCommand as exception:
            logger.critical("Could not get total memory", exception)
            return -1

    @staticmethod
    def memory_free():
        """ get free memory in system(linux only)
        @rtype int
        @return total memory or -1 if something went wrong

        """
        try:
            #"gawk '/MemFree/ { print $2 }' /proc/meminfo"
            return int(utils.execute("gawk", "'/MemFree/ { print $2 }'",
                               "/proc/meminfo")[0])
        except ScalixExternalCommand as exception:
            logger.critical("Could not get free memory", exception)
            return -1

    @staticmethod
    def memory():
        """ get total memory and free memory in system(linux only)

        @rtype tuple
        @return tuple with total memory and free  if something went wrong some
        of this values will be have -1

        """
        return System.memory_total(), System.memory_free()

    @staticmethod
    def partition_size(folder):
        """ get folder size in system(linux only)

        @rtype int
        @param folder - string full path to the folder
        @return size or -1 if something went wrong some

        """
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
        """ get folder size for set of folders in system(linux only)

        @rtype list
        @param args list or tuple
        @return list of size for each folder or -1 if something went wrong some

        """
        if not args:
            return System.partition_size('/')
        result = []
        for partition in args:
            result.append(System.partition_size(partition))
        return result

    @staticmethod
    def open_url(url):
        """open url in default browser

        @rtype bool
        @param url string
        @return True or False
        """
        try:
            return webbrowser.open(url, new=1)
        except webbrowser.Error as exception:
            logger.critical("Couldn't open browser", exception, " url ", url)
            return False

    @staticmethod
    def listening_port(port):
        """checks if port opened

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
    def get_fqdn():
        """get  fully qualified domain name (FQDN)

        """
        return socket.getfqdn()

    @staticmethod
    def is_fqdn():
        """ check if fully qualified domain name (FQDN) is valid

        """
        pattern = r'^[a-zA-Z0-9\-\.]+\.([0-9a-zA-Z]+)$'
        return re.match(pattern, System.get_fqdn()) != None

    @staticmethod
    def get_ips():
        """ get ips setted in system local netwoworks which starts with
        127.x.x.x or 192.x.x.x will ignore

        @rtype list
        @return list of ip's in system

        """
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
        """ tries to get mx record for domain

        @type bool
        @return True or False

        """
        try:
            lines = utils.execute("dig", "-t", "MX", "+short", domain)
            return [i.strip() for i in lines]
        except ScalixExternalCommand as exception:
            logger.warning("Could not get MX records ", exception)
            return False

    @staticmethod
    def get_java_version(raw=False):
        """get version of installed java virtual machine

        @return string if java installed and available in system or None if java
        not installed

        """
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
        """check if installed java virtual machine from IBM

        @rtype bool
        @return True or False

        """
        result = re.search(r'IBM\s(\w+)\sVM',
                           '\n'.join(System.get_java_version(raw=True) or []),
                           re.I | re.M)
        return result != None

    @staticmethod
    def determine_ip():
        """ get ip address
        @rtype string
        return machine ip or localhost ip

        """
        try:
            ip_list = socket.gethostbyaddr(System.get_fqdn())[2]
        except socket.error as exception:
            logger.critical(exception)
            return '127.0.0.1'

        if ip_list:
            return ip_list[0]
        return '127.0.0.1'

    @staticmethod
    def determine_interface(ip_str):
        """ get network interface on which ip setted

        @param ip string
        @return string name of interface or None

        """
        try:
            cmd = ["ip", "addr", "show", "|", utils.bash_command("grep"),
                   "[[:space:]]inet[[:space:]]{0}/".format(ip_str), "|",
                   utils.bash_command("head"), "-1", "|",
                   utils.bash_command("gawk"), "'{ print $NF }'"]
            lines = utils.execute(cmd)
            if lines:
                return lines[0].strip()

        except ScalixExternalCommand as exception:
            logger.warning("Could not determine interface", exception)
