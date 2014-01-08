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
    ('bgf', 'white', 'dark red', 'standout'),
    ('selectable','black', 'dark cyan')
    ]


#urwid.AttrWrap(urwid.Button(('key', "  F10"), " quit", _f10_pressed),
#                'key','key')
FOOTER_TEXT = ('footer', [
    ('key', " F3"), " License  ",
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
        return self.with_padding(urwid.Text(text))

    def with_padding(self, content ,left=10, right=10, min_width=60):
        return urwid.Padding(content, left=10, right=10, min_width=60)

class SxList(urwid.ListBox):

    def focus_next(self):
        try:
            self.body.set_focus(self.body.get_next(self.body.get_focus()[1])[1])
        except:
            pass

    def focus_previous(self):
        try:
            self.body.set_focus(self.body.get_prev(self.body.get_focus()[1])[1])
        except:
            pass

class DialogExit(Exception):
    pass

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

    _blank = urwid.Text("")

    def __init__(self, content, title, ui, width=78, height=10, buttons=None,
                 background=None):
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
        if background is None:
            background =  ('dialog', 'bg', 'bgf')
        #Text widget containing the message:
        if not isinstance(content, urwid.Widget):
            if isinstance(content, list):
                content = self._list_to_widget(content, height)
            else:
                content = urwid.Text(content)
        self.ui = ui
        self.content = content
        msg_widget = urwid.Padding(content, 'center', width - 4)

        #GridFlow widget containing all the buttons:
        button_widgets = []
        if buttons:
            for label, val in buttons:
                btn = urwid.Button(label, self._action, val)
                btn = urwid.AttrWrap(btn, background[1], background[2])
                button_widgets.append(btn)

        #Combine message widget and button widget:
        widget_list = [msg_widget, self._blank]
        pile_index = 1
        if button_widgets:
            pile_index = 2
            widget_list.append(urwid.GridFlow(button_widgets,
                                              12, 2, 1, 'center'))

        self._combined = urwid.AttrWrap(urwid.Filler(
            urwid.Pile(widget_list, pile_index)), background[0])

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
        overlay = urwid.Overlay(pile, self.ui.widget, 'center', width,
                                'middle', height)
        urwid.WidgetWrap.__init__(self, overlay)


    def _list_to_widget(self, list, height):
        parsed_list = []
        for line in list:
            if not isinstance(line, urwid.Widget):
                parsed_list.append(urwid.Text(line.rstrip()))
            else:
                parsed_list.append(line)
        list = SxList(urwid.SimpleListWalker(parsed_list))
        return urwid.AttrWrap(urwid.BoxAdapter(list, height-2), 'selectable',
                              'focustext')

    def _action(self, button, val):
        """
        Function called when a button is pressed.
        Should not be called manually.
        """
        self.b_pressed = val

    def execute(self):
        keys = True
        dim = self.ui.screen.get_cols_rows()
        while True:
            if keys:
                self.ui.screen.draw_screen(dim, self.render(dim,True))

            keys = self.ui.screen.get_input()
            if not keys:
                continue
            if "window resize" in keys:
                dim = self.ui.screen.get_cols_rows()
            if "esc" in keys:
                break

            for event in keys:
                if hasattr(self.content, 'focus_next'):
                    self._scroll_listbox(event, dim)
                else:
                    self._button_events_process(event, dim)
            try:
                self._process_button_values()
            except DialogExit, exception:
                return exception.args[0]

    def _button_events_process(self, event, dim):
        if urwid.is_mouse_event(event):
            self.mouse_event(dim, event[0], event[1],
                                     event[2], event[3], True)
        else:
            self.keypress(dim, event)

    def _scroll_listbox(self, event, dim):

        if urwid.is_mouse_event(event):
            if event[1] is 4:
                self.content.focus_previous()
            if event[1] is 5:
                self.content.focus_next()
            return

        if event in ('down','page down'):
            self.content.focus_next()
        if event in ('up','page up'):
            self.content.focus_previous()

    def _process_button_values(self):
        pass

class ConfirmDialog(Dialog):

    def __init__(self, text, ui, width=50, height=7):

        buttons = [("Yes", True), ("No", False)]
        super(ConfirmDialog, self).__init__(text, 'Confirm', ui,
                                            width, height, buttons)

    def _process_button_values(self):
        if self.b_pressed is None:
            return
        raise DialogExit(self.b_pressed)
