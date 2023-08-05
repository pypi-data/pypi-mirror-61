#
## Filename    : warn.py
## Author(s)   : Michel Le Borgne
## Created     : 11/2009
## Revision    :
## Source      :
##
## Copyright 2012 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided hereunder is on an "as is" basis, and IRISA has
## no obligations to provide maintenance, support, updates, enhancements
## or modifications.
## In no event shall IRISA be liable to any party for direct, indirect,
## special, incidental or consequential damages, including lost profits,
## arising out of the use of this software and its documentation, even if
## IRISA have been advised of the possibility of such damage.  See
## the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this library; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
##
## The original code contained here was initially developed by:
##
##     Michel Le Borgne.
##     IRISA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""
A collection of warning widgets
"""

import pygtk

pygtk.require("2.0")
import gtk


def start_warn(message):
    """Warn for a start"""
    mess = gtk.MessageDialog(
        None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, message
    )
    mess.run()
    mess.destroy()


def ok_warn(message, color=None):
    """Simple warning before action"""
    mess = gtk.MessageDialog(
        None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, message
    )
    if color:
        color = gtk.gdk.color_parse(color)
        mess.modify_bg(gtk.STATE_NORMAL, color)
    mess.run()
    mess.destroy()


def cancel_warn(message):
    """Error - imply cancellation of the action"""
    message1 = message + " - CANCELLED"
    mess = gtk.MessageDialog(
        None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, message1
    )
    mess.run()
    mess.destroy()


def system_warn(message):
    """Fatal error - bug or bd problems"""
    message1 = message + " - BD problem or BUG!"
    mess = gtk.MessageDialog(
        None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message1
    )
    mess.run()
    mess.destroy()


def confirm(parent, message):
    """Ask for action
    :return: Choice of the user (True/False)
    :rtype: <boolean>
    """
    dialog = gtk.Dialog(
        "Warning",
        parent,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT),
    )
    label = gtk.Label(message)
    dialog.vbox.pack_start(label, True, False, 0)
    label.show()
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_ACCEPT:
        return True
    elif response == gtk.RESPONSE_REJECT:
        return False


class DialogEntry(gtk.Dialog):
    """Custom dialog entry"""

    def __init__(self, mess):
        """
        :param mess: Message to be displayed in the dialog box
        :type mess: <str>
        """
        gtk.Dialog.__init__(
            self, mess, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        )

        self.set_default_size(350, 75)
        self.entry = gtk.Entry()
        self.vbox.pack_start(self.entry, True, True, 0)
        self.entry.show()

        self.okb = gtk.Button("Ok")
        self.action_area.pack_start(self.okb, False, False, 0)
        self.okb.show()

        self.cancel = gtk.Button("Cancel")
        self.action_area.pack_start(self.cancel, False, False, 0)
        self.cancel.show()
