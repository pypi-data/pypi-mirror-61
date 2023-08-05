##
## Filename    : displayFact.py
## Author(s)   : Michel Le Borgne
## Created     : 11/2009
## Revision    :
## Source      :
##
## Copyright 2009-2010 : IRISA/IRSET
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
Widgets for lists of nodes used in Cadbiom Gui
"""
import gtk
import gobject


class ToggleList(gtk.Frame):
    """List view with toggle button (Simple/frontier nodes list)"""

    def __init__(self):
        """Create a view

        Attributes::

            :param list_item: Checkable items in the list.
                Internal structure is a tuple of name and check status
                (<tuple <str>, <boolean>>)
            :type list_item: <gtk.ListStore>
        """

        gtk.Frame.__init__(self)
        self.view = gtk.TreeView()
        self.view.show()
        self.add(self.view)
        self.height = 0

        # model
        self.list_item = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
        self.view.set_model(self.list_item)

        # CellRendererText for names
        self.renderer0 = gtk.CellRendererText()
        self.renderer0.set_property("editable", False)

        # CellRendererToggle for selection
        self.renderer1 = gtk.CellRendererToggle()
        self.renderer1.set_property("activatable", True)
        self.renderer1.connect("toggled", self.toggled_col1_callback)
        # connection of cell renderers to respective columns
        self.column0 = gtk.TreeViewColumn(None, self.renderer1)
        self.column1 = gtk.TreeViewColumn(None, self.renderer0, text=0)
        self.column0.add_attribute(self.renderer1, "active", 1)

        self.column0.set_property("sizing", gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        self.column1.set_property("sizing", gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        self.view.append_column(self.column0)
        self.view.append_column(self.column1)

    def toggled_col1_callback(self, cellrenderer, path):
        """Callback for column1, called when toggled event is fired

        :param path: position of the cell in the list_item
        """
        self.list_item[path][1] = not self.list_item[path][1]

    def set_list_select(self, l_keywords):
        """
        initialize from a list of name - all unselected
        @param l_keywords: list<string>
        """
        self.height = 40 * len(l_keywords)
        [self.list_item.append([kwo, False]) for kwo in l_keywords]

    def set_list_pairs(self, l_pairs):
        """
        initialize from a list of pairs - all unselected
        @param l_pairs: list< pair<string,bool> >
        """
        self.height = 40 * len(l_pairs)
        [self.list_item.append([pair[0], pair[1]]) for pair in l_pairs]

    def get_selected_items(self):
        """Retrieve the names of the selected items"""
        return [item[0] for item in self.list_item if item[1]]

    def set_selected_items(self, selected_list):
        """Set the check status of the given items in the GUI

        .. note:: Given items are checked, others are unchecked.
        """
        for item in self.list_item:
            if item[0] in selected_list:
                item[1] = True
            else:
                item[1] = False

    def get_pair_values(self):
        """Retrieve the cas and word associated (pairs)"""
        return [(item[0], item[1]) for item in self.list_item]

    def deselect_all(self):
        """Deselect all items"""
        for item in self.list_item:
            item[1] = False

    def select_all(self):
        """Select all items"""
        for item in self.list_item:
            item[1] = True

    def clear(self):
        """Remove all items"""
        self.refresh([])

    def refresh(self, newlist):
        """Rebuild the list"""
        self.list_item.clear()
        self.set_list_select(newlist)


class ChoiceList(object):
    """Display a list with marks (this class is not used)"""

    def __init__(self, l_names, callback, title):
        self.callback = callback

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.connect("destroy", gtk.main_quit)
        height = gtk.gdk.screen_height()
        height = int(height * 0.85)
        self.window.set_size_request(300, height)
        self.window.set_title(title)

        # view
        self.choice_view = gtk.TreeView()

        # model
        self.choice_list = gtk.ListStore(gobject.TYPE_STRING)
        l_names.sort()
        for name in l_names:
            self.choice_list.append([name])
        self.choice_view.set_model(self.choice_list)

        # CellRendererText for choice names
        self.renderer0 = gtk.CellRendererText()
        self.renderer0.set_property("editable", False)

        # connection of cell renderers to respective columns
        self.column0 = gtk.TreeViewColumn("", self.renderer0, text=0)
        self.choice_view.append_column(self.column0)

        swin = gtk.ScrolledWindow()
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        swin.set_shadow_type(gtk.SHADOW_IN)
        swin.add_with_viewport(self.choice_view)
        self.window.add(swin)

        # control
        self.choice_view.connect("row_activated", self.choice_selection_callback)
        self.window.show_all()

    def choice_selection_callback(self, widget, path, view_column):
        """
        callback called when a choice is done
        """
        if widget == self.choice_view:
            treeselection = widget.get_selection()
            (choice, iter) = treeselection.get_selected()
            choice_name = choice.get_value(iter, 0)
            self.callback(choice_name)
            self.window.destroy()
