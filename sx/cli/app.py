# -*- coding: utf-8 -*-


__author__ = 'pussbb'


import urwid

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
        elif key == "f3":
            self.show_license()

    def show_license(self):
        l = []
        file = utils.absolute_file_path('license')
        if not os.path.exists(file):
            file = utils.absolute_file_path('license.activesync')
        if os.path.exists(file):
            for line in open(file).readlines():
                l.append(urwid.Text( line.rstrip()))
        else:
            l.append(urwid.Text("No license found."))

        list = SxList(urwid.SimpleListWalker(l))
        body = urwid.AttrWrap(urwid.BoxAdapter(list, 68),
                              'selectable','focustext')
        dialog = Dialog(body, 'Scalix License', [], 79, 70, self.ui.widget)

        dim = self.ui.screen.get_cols_rows()
        keys = True
        #Event loop:
        while True:
            if keys:
                self.ui.screen.draw_screen(dim, dialog.render(dim,True))
            keys = self.ui.screen.get_input()
            if not keys:
                continue
            if "esc" in keys:
                break
            for event in keys:
                if urwid.is_mouse_event(event):
                    if event[1] is 4:
                        list.focus_previous()
                    if event[1] is 5:
                        list.focus_next()
                    continue

                if event in ('down','page down'):
                    list.focus_next()
                if event in ('up','page up'):
                    list.focus_previous()


