## Filename    : edit_mvc.py
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
Class for managing a triple (Model, View, Controler) associated with a model
"""

from cadbiom.models.guard_transitions.chart_model import ChartModel
from chart_view import ChartPage, NavView
from cadbiom_gui.gt_gui.graphics.drawing_style import PlainDrawing, NavDrawing
from cadbiom_gui.gt_gui.chart_controler import ChartControler, NavControler
from layout import LayoutVisitor


class EditMVC(object):
    """Editor object composed of a MVC pattern

    Each instance of EditMVC is corresponding to an independant tab
    in the Cadbiom GUI.

    We use the following classes:
        ChartModel: Model
        ChartControler: Model controller
        NavControler: Overview controller

        ChartPage: Graph editor container
        NavView: Graph editor overview
    """

    def __init__(self, chart, model_name, model=None, layout=False):
        """
        :param chart: The charter using the edit mvc
        :param model_name: Name of the model
        :key model: (optional) Chart model
        :key layout: (optional) Flag to activate the default layout (hierarchical_LR).
            Default False.
        :type chart: <Charter>
        :type model_name: <str>
        :type model: <ChartModel>
        :type layout: <boolean>
        """
        self.charter = chart
        self.ident = chart.ei_id
        chart.ei_id = chart.ei_id + 1
        if model:
            self.model = model
        else:
            self.model = ChartModel(model_name)
        self.controler = ChartControler(self.model, chart.clipboard)
        xor, yor, width, height = chart.graph_notebook.get_allocation()
        # adjustment for notebook (-6, -38)
        self.viewpage = ChartPage(
            width - 6, height - 38, PlainDrawing(), self.controler, self.model
        )
        self.view = self.viewpage.draw
        self.title = self.model.name
        # layout?
        if layout:
            # default layout if necessary
            lvi = LayoutVisitor(self.view, "hierarchical_LR")
            model.accept(lvi)
        # overview navigator
        self.navcontroler = NavControler()
        xor, yor, width, height = chart.overview_window.get_allocation()
        self.nav_view = NavView(
            width, height, NavDrawing(), self.navcontroler, self.model
        )
        self.viewpage.attach(self.nav_view)  # linked to view
        self.navcontroler.attach(self.viewpage)

        # registration of auxiliary windows
        self.aux_win = []
        self.has_display = False

    def change_model(self, new_model):
        """Change the model component"""
        self.clean_subwin()
        self.view.model.detach(self.view)
        # new model
        self.model = new_model
        self.controler.model = self.model
        self.navcontroler.model = self.model
        self.view.model = self.model
        self.nav_view.model = self.model
        self.view.model.attach(self.view)
        self.nav_view.model.attach(self.nav_view)
        self.display()

    def display(self):
        """Update and show"""
        self.view.update()
        self.nav_view.update()
        self.viewpage.notify(None)

    def update(self, node, transition):
        """Used in the observer pattern"""
        self.node = node
        self.transition = transition
        self.view.update()
        self.nav_view.update()
        self.viewpage.notify(None)

    def connect(self, chart):
        """Initialize the GUI when the user switches from an EditMVC to another

        We connect the buttons and of the graphical interface to the components
        of the current EditMVC.
        Then the UI is sync with the current model

        :param chart: Mainwindow class
        :type chart: <Charter>
        """
        # connect buttons to emvc controler
        chart.drawing_buttons_connect()
        # self.tab_button.set_sensitive(True)
        # attach charter to new edit_MVC controler
        self.controler.attach("edit_node", chart)
        chart.chart_info.set_controler(self.controler)
        # Force chart_info to be refreshed
        self.controler.notify("current_change")

        # nav window
        chart.overview_window.get_child().add(self.nav_view)

    def disconnect(self, chart, w_destroy):
        """Inverse connect operation

        :param w_destroy: If true the window and its children are destroyed.
            If False, Subordinate windows are not destroyed.
        :type w_destroy: <boolean>
        """
        if w_destroy:
            chart.drawing_button_disconnect()
            chart.drawing_button_enable()
        else:
            chart.drawing_button_disable()
        self.controler.detach("edit_node", chart)
        # self.tab_button.set_sensitive(False)
        if w_destroy:
            self.clean_subwin()
        chart.overview_window.get_child().remove(self.nav_view)

    def on_zoom_plus(self, widget):
        """Zoom in"""
        self.view.zoom_plus()

    def on_zoom_minus(self, widget):
        """Zoom out"""
        self.view.zoom_minus()

    ## sub windows management ##################################################
    def win_register(self, win):
        """Subordinate windows registration"""
        self.aux_win.append(win)

    def win_remove(self, win):
        """Subordinate windows are destroyed"""
        if win in self.aux_win:
            self.aux_win.remove(win)

    def clean_subwin(self):
        """As it says"""
        for win in self.aux_win:
            win.destroy()
        self.aux_win = []
