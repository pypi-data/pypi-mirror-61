## Filename    : charter_info.py
## Author(s)   : Geoffroy Andrieux
## Created     : 03/2010
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
## documentation provided here under is on an "as is" basis, and IRISA has
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
##     Geoffroy Andrieux.
##     IRISA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Michel Le Borgne, Nolwenn Le Meur
##
"""
Widget for displaying information on the elements of the model

CharterInfo: Contains 3 classes inheriting from :class:`Info`:

:class:`ModelInfo`
:class:`NodeInfo`
:class:`TransInfo`

"""
from __future__ import print_function
import gtk
import pkg_resources
import json

from utils.text_page import TextEditConfig, TextPage
from cadbiom import commons as cm


class CharterInfo(gtk.Frame):
    """Windows for displaying information on the elements of the model

    Contains 3 classes whose role is to update in real time the fields in the GUI
    about the currently selected transition, model or node.

    .. seealso::

        :class:`ModelInfo`
        :class:`NodeInfo`
        :class:`TransInfo`

    This class is directly linked to the observers of the :class:`ChartControler`
    thanks to the signal `current_change`.
    """

    def __init__(self, frame):
        self.frame = frame
        self.controler = None
        self.fact_window = None
        self.model_info = ModelInfo(self)
        self.node_info = NodeInfo(self)
        self.trans_info = TransInfo(self)

        self.current_info = self.model_info

    def set_controler(self, new_controler):
        """Associate a controler in a MVC pattern

        .. note:: attach current_change signal to the given controller.

        :param new_controler: New ChartControler
        :type new_controler: <ChartControler>
        """
        if self.controler:
            self.controler.detach("current_change", self)
        self.controler = new_controler
        self.controler.attach("current_change", self)

    def display(self):
        """
        Show all
        """
        chi = self.frame.get_child()
        if chi:
            self.frame.remove(chi)

        self.frame.add(self.current_info.frame)
        self.frame.show()

    def switch_to(self, new_info):
        """
        callback when info change
        """
        if self.current_info is not None:
            self.current_info.warn_change()

        self.current_info = new_info
        self.display()

    def update(self, node, transition):
        """
        Used if registered as an observer
        """
        if node is None and transition is None:
            self.model_info.update(self.controler)
            self.switch_to(self.model_info)

        elif transition is None:
            if node.is_top_node():
                # Update ModelInfo
                self.model_info.update(self.controler)
                self.switch_to(self.model_info)
            else:
                # Update NodeInfo
                self.node_info.update(node)
                self.switch_to(self.node_info)
        else:
            # Update TransInfo
            self.trans_info.update(transition)
            self.switch_to(self.trans_info)

    def enter_callback(self, widget, entry):
        """
        return the entry
        """
        entry_text = entry.get_text()
        print("Entry contents: %s\n" % entry_text)

    def has_transition(self):
        """
        As it says
        """
        return self.current_info.has_transition()


class Info(object):
    """Abstract class

    Implementing a "notes window" for metadata of transitions and nodes

    Used by::

        :class:`ModelInfo`
        :class:`NodeInfo`
        :class:`TransInfo`
    """

    def warn_change(self):
        """Called when ChartInfo is updated (Ex: save notes)"""
        pass

    def has_transition(self):
        """Return the current transition"""
        pass

    def update(self, controler):
        """Used when registered as an observer"""
        pass

    def display_note_window(self, title, note_text):
        """Display a window with the given text content

        Used to display notes from the selected transitions or nodes.

        .. seealso: :class:`NodeInfo`, :class:`TransInfo`.

        :param title: Title of the window
        :param note_text: Text content to display
        :type title: <str>
        :type note_text: <str>
        """
        self.note_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # TEST: Do not save the notes
        # self.note_window.connect("destroy", self.save_note)
        self.note_window.set_title("notes: " + title)
        self.note_window.set_position(gtk.WIN_POS_CENTER)
        self.note_window.set_keep_above(True)
        self.note_window.set_default_size(600, 300)
        self.note_window.connect("key_press_event", self.on_escape)
        # Favicon
        favicon = pkg_resources.resource_filename(
            __name__,
            "images/favicon.ico"
        )
        self.note_window.set_icon_from_file(favicon)

        ed_conf = TextEditConfig()
        self.note_text_page = TextPage(None, ed_conf)
        # TEST: Not editable
        self.note_text_page.write.set_editable(False)
        # Handle JSON data
        try:
            parsed = json.loads(note_text)
            note = json.dumps(parsed, indent=2, sort_keys=True)
        except ValueError:
            note = note_text

        self.note_text_page.set_text(note)
        self.note_window.add(self.note_text_page)
        self.note_window.show_all()

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.note_window.destroy()

    def save_note(self, widget):
        """Save the current text modified in display_note_window"""
        raise NotImplementedError("Abstract method")


class ModelInfo(Info):
    """Object used as a model - store information for CharterInfo"""

    def __init__(self, cin):
        template = pkg_resources.resource_filename(
            __name__, "chart_glade/model_info.glade"
        )
        self.page = gtk.glade.XML(template)
        wid = self.page.get_widget("model_frame")
        self.frame = wid.get_child()
        wid.remove(self.frame)
        self.info = cin

        self.name = self.page.get_widget("model_entry")
        self.name.connect("changed", self.set_model)
        self.name.set_editable(True)

        self.nb_nodes = self.page.get_widget("node_entry")
        self.nb_nodes.set_editable(False)
        self.nb_nodes.set_sensitive(False)

        self.nb_trans = self.page.get_widget("trans_entry")
        self.nb_trans.set_editable(False)
        self.nb_trans.set_sensitive(False)

    def set_model(self, widget):
        """Called when the name of the model has been modified by a user
        - set the name of the model,
        - then notify the model.
        """
        self.model.name = self.name.get_text()
        self.model.notify()

    def update(self, controler):
        """
        when used as an observer
        """
        self.model = controler.model
        self.name.set_text(controler.model.name)
        nodes = str(len(self.model.simple_node_dict.keys()))
        trans = str(len(self.model.transition_list))
        self.nb_nodes.set_text(nodes)
        self.nb_trans.set_text(trans)


class NodeInfo(Info):
    """A component of CharterInfo used for nodes

    .. TODO:: Display node notes; move notes code from TransInfo to Info
    """

    def __init__(self, cin):
        template = pkg_resources.resource_filename(
            __name__, "chart_glade/node_info.glade"
        )
        self.page = gtk.glade.XML(template)
        wid = self.page.get_widget("node_frame")
        self.frame = wid.get_child()
        wid.remove(self.frame)
        self.info = cin

        self.name = self.page.get_widget("node_entry")
        self.name.connect("changed", self.set_node)

        # Button
        self.show_notes_button = self.page.get_widget("button_metadata")
        self.show_notes_button.connect("clicked", self.set_note)

    def set_node(self, widget):
        """Called when the node has been modified by a user
        - set the node settings,
        - then notify the model.
        """
        self.node.set_name(self.name.get_text())
        self.node.model.notify()

    def update(self, node):
        """
        Used when registered as an observer
        """
        if node:
            self.node = node
            self.name.set_text(node.name)

    def set_note(self, widget):
        """Associate a text note to a node

        Use the method of the parent class :class:`Info` to display the note.
        """
        self.display_note_window(self.node.name, self.node.note)


class TransInfo(Info):
    """A component of CharterInfo used for transitions"""

    def __init__(self, cin):

        template = pkg_resources.resource_filename(
            __name__, "chart_glade/trans_info.glade"
        )
        self.page = gtk.glade.XML(template)
        wid = self.page.get_widget("trans_frame")
        self.frame = wid.get_child()
        wid.remove(self.frame)
        self.info = cin  # owner
        self.note_window = None

        # Text entries
        self.name = self.page.get_widget("trans_entry")
        self.name.set_editable(False)
        self.evt = self.page.get_widget("evt_entry")
        self.cond = self.page.get_widget("cond_entry")

        # Buttons
        self.show_notes_button = self.page.get_widget("button_metadata")
        # Attached to Charter.on_display_states via clicked event
        self.show_influencing_nodes_button = self.page.get_widget(
            "button_influencing_nodes"
        )

        # Tooltips
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self.show_notes_button, "Show the transition metadata")
        self.tooltips.set_tip(
            self.show_influencing_nodes_button,
            "Show the nodes influencing this transition",
        )
        self.tooltips.enable()
        self.tooltips.set_delay(cm.TOOLTIPS_DELAY)

        # User can change all the entries
        self.name.connect("changed", self.set_trans)
        self.evt.connect("changed", self.set_trans)
        self.cond.connect("changed", self.set_trans)
        self.show_notes_button.connect("clicked", self.set_note)

    def set_trans(self, widget):
        """Called when the transition has been modified by a user
        (and after TransInfo update)

        - set the transition settings,
        - then notify the model.
        """
        if self.lock:
            return

        self.trans.set_name(self.name.get_text())
        self.trans.set_event(self.evt.get_text())
        self.trans.set_condition(self.cond.get_text())
        self.trans.ori.model.notify()

    def warn_change(self):
        """
        As it says
        """
        # TEST: Do not save the notes
        # self.save_note(None)
        pass

    def update(self, trans):
        """
        When registered as an observer
        """
        if trans:
            self.lock = True
            self.trans = trans  # for fact association management
            self.name.set_text(trans.ori.name + "->" + trans.ext.name)
            self.evt.set_text(trans.event)
            self.cond.set_text(trans.condition)
            self.lock = False

    def has_transition(self):
        """
        As it says
        """
        return self.trans

    def set_note(self, widget):
        """Associate a text note to a transition

        Use the method of the parent class :class:`Info` to display the note.
        """
        self.display_note_window(
            self.trans.ori.name + "->" + self.trans.ext.name, self.trans.note
        )

    def save_note(self, widget):
        """
        register the note (deactivated for now)
        """
        if self.note_window:
            text = self.note_text_page.get_text()
            self.trans.note = text
            self.trans.ori.model.modified = True
            self.note_window.destroy()
            self.note_window = None
