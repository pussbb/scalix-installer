# -*- coding: utf-8 -*-

__author__ = 'pussbb'
from .. import version
import urwid

PALETTE = [
    ('body', 'white', 'light blue'),
    ('header', 'white', 'dark blue', 'bold'),
    ('footer', 'dark cyan', 'dark blue', 'bold'),
    ('key','light cyan', 'dark blue', 'underline'),
    ('bright', 'white', 'light blue', ('bold','standout'))
    ]

FOOTER_TEXT = ('footer', [
    ('key', "  F10"), " quit",
    ])

HEADER_TEXT = (
    'header',
    [' Scalix Installer v {v}. '.format(v=version.get_version()),]
)

BLANK_LINE = urwid.Divider()

class WizardPage(object):

    def __init__(self, system):
        self.system = system

    def widget(self):
        raise NotImplementedError

    def next(self):
        pass

    def previous(self):
        pass

    def text_padd(self, text):
        return urwid.Padding(urwid.Text(text), left=10, right=10, min_width=80)
