# -*- coding: utf-8 -*-

__author__ = 'pussbb'
from .. import version
import urwid

PALETTE = [
    ('body', 'white', 'light blue'),
    ('header', 'white', 'dark blue', 'bold'),
    ('footer', 'dark cyan', 'dark blue', 'bold'),
    ('key','light cyan', 'dark blue', 'underline'),
    ('bright', 'white', 'light blue', ('bold','standout')),
    ('border','white','light gray'),
    ('dialog','white','dark gray'),
    ('dialog_title','white','light gray', 'bold'),
    ('bg', 'black', 'light gray'),
    ('bgf', 'white', 'dark red', 'standout')
    ]


#urwid.AttrWrap(urwid.Button(('key', "  F10"), " quit", _f10_pressed),
#                'key','key')
FOOTER_TEXT = ('footer', [
    ('key', "  F10"), " quit",
    ])

HEADER_TEXT = (
    'header',
    [' Scalix Installer v {v}. '.format(v=version.get_version()),]
)

BLANK_LINE = urwid.Divider()

class WizardPage(object):

    def __init__(self, app):
        self.app = app

    def widget(self):
        raise NotImplementedError

    def next(self):
        pass

    def previous(self):
        pass

    def text_padd(self, text):
        return urwid.Padding(urwid.Text(text), left=10, right=10, min_width=60)

class Dialog(urwid.WidgetWrap):
    """
    Creates a BoxWidget that displays a message

    Attributes:

    b_pressed -- Contains the label of the last button pressed or None if no
                 button has been pressed.
    edit_text -- After a button is pressed, this contains the text the user
                 has entered in the edit field
    """

    b_pressed = None
    edit_text = None

    _blank = urwid.Text("")
    _edit_widget = None
    _mode = None

    def __init__(self, msg, title, buttons, width, height, body, ):
        """
        msg -- content of the message widget, one of:
                   plain string -- string is displayed
                   (attr, markup2) -- markup2 is given attribute attr
                   [markupA, markupB, ... ] -- list items joined together
        buttons -- a list of strings with the button labels
        width -- width of the message widget
        height -- height of the message widget
        body -- widget displayed beneath the message widget
        """
        attr =  ('dialog', 'bg', 'bgf')
        #Text widget containing the message:
        msg_widget = urwid.Padding(urwid.Text(msg), 'center', width - 4)

        #GridFlow widget containing all the buttons:
        button_widgets = []

        for button in buttons:
            btn = urwid.Button(button, self._action)
            btn = urwid.AttrWrap(btn, attr[1], attr[2])
            btn = urwid.AttrWrap(btn, 'selectable','focus')
            button_widgets.append(btn)

        button_grid = urwid.GridFlow(button_widgets, 12, 2, 1, 'center')

        #Combine message widget and button widget:
        widget_list = [msg_widget, self._blank, button_grid]
        self._combined = urwid.AttrWrap(urwid.Filler(
            urwid.Pile(widget_list, 2)), attr[0])

        bline = urwid.Divider("─")
        vline = urwid.SolidFill("│")
        blcorner = urwid.Text("└")
        brcorner = urwid.Text("┘")
        tline = urwid.Divider("─")
        tlcorner = urwid.Text("┌")
        trcorner = urwid.Text("┐")


        tline_widgets = [('fixed', 1, tlcorner),
                         tline,
                         urwid.Text(('dialog_title', title), align="center")]

        tline_widgets.extend([tline, ("fixed", 1, trcorner)])

        top = urwid.AttrWrap(urwid.Columns(tline_widgets), 'border')

        middle = urwid.Columns([('fixed', 1, vline),
                                        self._combined, ('fixed', 1, vline)],
                                        box_columns=[0,2], focus_column=1)
        middle = urwid.AttrWrap(middle, 'border')
        bottom = urwid.Columns([('fixed', 1, blcorner),
                                        bline, ('fixed', 1, brcorner)])
        bottom = urwid.AttrWrap(bottom, 'border')

        pile = urwid.Pile([('flow',top), middle,
                                ('flow', bottom)], focus_item=1)

        #Place the dialog widget on top of body:
        overlay = urwid.Overlay(pile, body, 'center', width,
                                'middle', height)
        urwid.WidgetWrap.__init__(self, overlay)


    def _action(self, button):
        """
        Function called when a button is pressed.
        Should not be called manually.
        """

        self.b_pressed = button.get_label()
        if self._edit_widget:
            self.edit_text = self._edit_widget.get_edit_text()


class ConfirmDialog(object):

    def __init__(self, text, ui, buttons=None, width=50, height=7):
        if not buttons:
            buttons = ["Yes", "No"]
        self.confirm = Dialog(text, 'Confirm', buttons, width, height, ui.widget)
        self.ui = ui

    def execute(self):
        keys = True
        dim = self.ui.screen.get_cols_rows()
        #Event loop:
        while True:
            if keys:
                self.ui.screen.draw_screen(dim, self.confirm.render(dim,True))
            keys = self.ui.screen.get_input()

            if "window resize" in keys:
                dim = self.ui.screen.get_cols_rows()
            if "esc" in keys:
                return False

            for k in keys:
                self.confirm.keypress(dim, k)

            if self.confirm.b_pressed == "Yes":
                return True
            if self.confirm.b_pressed == "No":
                return False
