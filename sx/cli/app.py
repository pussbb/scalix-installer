# -*- coding: utf-8 -*-


__author__ = 'pussbb'

from . import *
from .. import utils
from . import general
import os

class CliApplication(object):
    """
    A class responsible for providing the application's interface.
    """

    def __init__(self, system, args):
        system_info = 'Runing on {0} {1} {2} runlevel {3}'.format(system.distro,
                                                     system.distro_version,
                                                     system.arch,
                                                     system.run_level())
        HEADER_TEXT[1].append(system_info)
        header = urwid.AttrWrap(urwid.Text(HEADER_TEXT), 'header')
        footer = urwid.AttrWrap(urwid.Text(FOOTER_TEXT), 'footer')
        body = urwid.AttrWrap(general.Welcome(system).widget(), 'body')
        self.system = system
        self.args = args
        self.frame = urwid.Frame(body, header=header, footer=footer)


    def run(self):
        self.ui = urwid.MainLoop(self.frame, PALETTE,
                       unhandled_input=self.unhandled_keypress,
                       pop_ups=True)
        self.ui.run()

    def unhandled_keypress(self, key):
        if key == "f10":
            confirm = ConfirmDialog("Do you want to exit?", self.ui)
            if confirm.execute():
                raise urwid.ExitMainLoop()
        if key == "f3":
            self.show_license()
        if key == "f9":
            ErrorDialog('Opps some error occurred', self.ui).execute()
        is_mouse = urwid.is_mouse_event(key)
        if key in ('up','page up') or (is_mouse and key[1] == 4):
            self.frame.set_focus('body')
        if key in ('down','page down') or (is_mouse and key[1] == 5):
            self.frame.set_focus('footer')

    def show_license(self):

        list_ = []
        file = utils.absolute_file_path('license')
        if not os.path.exists(file):
            file = utils.absolute_file_path('license.activesync')
        if os.path.exists(file):
            list_ = open(file).readlines()
        else:
            list_ = ["No license found."]
        Dialog(list_, 'Scalix License', self.ui, 79, 70).execute()


