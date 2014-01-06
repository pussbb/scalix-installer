# -*- coding: utf-8 -*-

__author__ = 'pussbb'

from . import WizardPage, urwid, BLANK_LINE
from .. import texts

class Welcome(WizardPage):

    def widget(self):
        list = [
            BLANK_LINE,
            self.text_padd(texts.INTRO),
            #urwid.AttrWrap(urwid.Divider("-"), 'bright'),
            BLANK_LINE,
            self.text_padd("Please choose one of the following option:"),
            BLANK_LINE,
        ]
        return urwid.ListBox(urwid.SimpleListWalker(list))
