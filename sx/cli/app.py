# -*- coding: utf-8 -*-


__author__ = 'pussbb'


import urwid

from . import *

from . import general

class CliApplication(object):
    """
    A class responsible for providing the application's interface.
    """

    def __init__(self, system):

        system_info = 'Runing on {0} {1} {2}'.format(system.distro,
                                                     system.distro_version,
                                                     system.arch)
        HEADER_TEXT[1].append(system_info)
        header = urwid.AttrWrap(urwid.Text(HEADER_TEXT), 'header')
        footer = urwid.AttrWrap(urwid.Text(FOOTER_TEXT), 'footer')
        body = urwid.AttrWrap(general.Welcome(system).widget(), 'body')
        self.frame = urwid.Frame(body, header=header, footer=footer)


    def run(self):
        urwid.MainLoop(self.frame, PALETTE,
                       unhandled_input=self.unhandled_keypress).run()

    def unhandled_keypress(self, key):
        if key == "f10":
            raise urwid.ExitMainLoop()
