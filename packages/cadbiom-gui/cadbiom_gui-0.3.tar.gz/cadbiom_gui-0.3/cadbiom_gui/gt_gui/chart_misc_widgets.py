## Filename    : charter.py
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
## Contributor(s): Michel Le Borgne
##
"""
Small widgets for Cadbiom gui::

    - SearchManager: List of simple nodes for searching
    - SearchFrontier: Same as SearchManager but specialized on frontier nodes
    - LegendWindow: Widget to display the legend
    - ImportPIDParam: Widget for model importing
    - ImportBioPAXParams: Widget for BioPAX model importing
"""
# Standard imports
import itertools as it
import pkg_resources
import re
import traceback

# Custom imports
import gtk

# Cadbiom imports
from utils.listDisplay import ToggleList
from utils.fileHandling import FileChooser
from utils.reporter import CompilReporter
from utils.warn import cancel_warn, confirm
from cadbiom.models.guard_transitions.analyser.ana_visitors import FrontierVisitor
from cadbiom.models.guard_transitions.chart_model import ChartModel, CStartNode
from cadbiom.models.guard_transitions.analyser import model_corrections
from cadbiom.models.guard_transitions.translators.chart_xml import MakeModelFromXmlFile
from cadbiom.models.guard_transitions.translators.chart_xml_pid import (
    MakeModelFromPidFile,
)
from chart_simulator.chart_simul_controler import DisplayError
from cadbiom import commons as cm

LOGGER = cm.logger()


class SearchManager(object):
    """List of simple nodes for searching


    :param model_changed: Flag updated to True by the model.
        Its value is True until the user clicks on the "update" button.
        This operation is manual since it can be costly.
    :type model_changed: <boolean>
    """

    def __init__(self, chart, notebook, label):
        self.charter = chart
        self.model = None
        self.model_changed = True
        self.notebook = notebook

        # simple nodes
        self.sn_frame = gtk.Frame()
        vbox = gtk.VBox(False, 0)
        self.sn_frame.add(vbox)
        # simple nodes list
        self.sn_viewer = ToggleList()
        label = gtk.Label(label)
        # wrap into scrollwindow
        scroll = gtk.ScrolledWindow()
        scroll.add_with_viewport(self.sn_viewer)
        vbox.pack_start(scroll, True, True, 0)
        # search entry
        self.search_entry = gtk.Entry()
        vbox.pack_start(self.search_entry, False, False, 0)
        # buttons
        hbox = gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        update_button = gtk.Button("Update")
        update_button.connect("clicked", self.on_update)
        hbox.pack_start(update_button, False, False, 0)
        show_button = gtk.Button("Show")
        show_button.connect("clicked", self.on_show)
        hbox.pack_start(show_button, False, False, 0)
        extract_button = gtk.Button("Extract")
        extract_button.connect("clicked", self.on_extract)
        hbox.pack_start(extract_button, False, False, 0)
        clear_button = gtk.Button("Clear")
        clear_button.connect("clicked", self.on_clear)
        hbox.pack_start(clear_button, False, False, 0)
        notebook.append_page(self.sn_frame, label)


        # Tooltips
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(update_button, "Sync the list of nodes with the model")
        self.tooltips.set_tip(show_button, "Show the selected nodes on the model")
        self.tooltips.set_tip(extract_button, "Extract the selected nodes to another model")
        self.tooltips.set_tip(clear_button, "Reset the selection")
        self.tooltips.set_tip(
            self.search_entry,
            "Search for nodes by their names.\nYou can use regular expressions"
        )

        self.tooltips.enable()
        self.tooltips.set_delay(cm.TOOLTIPS_DELAY)

    def update(self):
        """The model informs observers that the model has changed

        We keep this value to True until the user clicks on the "update" button.
        """
        self.model_changed = True

    def display_nodes(self):
        """Display node names on the widget

        - On :meth:`set_model` at the initialization of the model
        - On :meth:`on_update` by a click on the button "update" by the user
        """
        # get node names
        lnode = self.model.get_simple_node_names()
        lnode.sort()
        # display node names
        self.sn_viewer.refresh(lnode)

    def set_model(self, model):
        """Refresh the GUI with the given model

        Called by :meth:`~cadbiom_gui.gt_gui.edit_mvc.set_current_edit_mvc`
        during the switch to a new/another tab/model.
        """
        if self.model:
            self.model.detach(self)
        self.model = model
        self.model.attach(self)
        self.model_changed = False
        # display node names
        self.display_nodes()
        # Check/tick previously selected nodes
        self.sn_viewer.set_selected_items(
            [node.name for node in self.model.marked_nodes]
        )

    def on_clear(self, widget):
        """Clear button callback: Reset selected nodes, and search entry field
        """
        self.sn_viewer.deselect_all()
        self.search_entry.set_text("")
        if self.model:
            self.model.unset_search_mark()
            self.model_changed = False  # search_mark implies a notify

    def on_update(self, widget):
        """Update button callback: Sync the view of simple nodes with the model"""
        if not self.model:
            return
        # unmarking nodes and transitions with conditions
        self.model.unset_search_mark()
        # display node names
        self.display_nodes()
        self.model_changed = False

    def on_show(self, widget):
        """Show button callback: Show nodes of interest in the graph editor

        Transitions with conditions where the selected nodes are involved
        are also marked
        """
        if not self.model:
            return
        # check model
        if self.model_changed:
            action = confirm(
                None,
                "The model has been modified since the last synchronization.\n"
                "Would you like to continue without updating the set of nodes "
                "and transitions?"
            )
            if not action:
                return

        # Get marked nodes names
        node_names = self.get_selected_or_matching_node_names()
        if not node_names:
            return

        # Set the mark status of all selected nodes/transitions
        # Transitions with conditions where the selected nodes are involved
        # are also marked
        self.model.set_search_mark(node_names)

        # Check/Display the marks in the nodes list
        self.sn_viewer.set_selected_items(node_names)
        self.model_changed = False  # search_mark implies a notify

    def on_extract(self, widget):
        """Extract nodes environment

        - Get selected nodes
        - Get all transitions of interest:
          - ori and ext nodes are concerned
          - ori or ext are concerned and the second node is a Start/Trap node
        """
        if not self.model:
            return
        # check model
        if self.model_changed:
            action = confirm(
                None,
                "The model has been modified since the last synchronization.\n"
                "Would you like to continue without updating the set of nodes "
                "and transitions before the extraction?"
            )
            if not action:
                return

        # Get marked nodes names
        node_names = self.get_selected_or_matching_node_names()
        if not node_names:
            return

        # Init new model
        submodel = ChartModel(self.model.name + "_extract")
        tnode = submodel.get_root()

        # Convert nodes names to nodes objects
        old_nodes = {self.model.node_dict[name] for name in node_names}

        # Get all transitions of interest:
        # - ori and ext nodes are concerned
        # - ori or ext are concerned and the second node is a Start/Trap node
        old_transitions = set()
        for transition in self.model.transition_list + list(
            it.chain(*self.model.signal_transition_dict.values())
        ):
            if {transition.ori, transition.ext}.issubset(old_nodes):
                pass
            elif transition.ori in old_nodes and isinstance(transition.ext, CStartNode):
                old_nodes.add(transition.ext)
            elif transition.ext in old_nodes and isinstance(transition.ori, CStartNode):
                old_nodes.add(transition.ori)
            else:
                continue

            # Keep the transition
            old_transitions.add(transition)

        # LOGGER.debug("Extract old nodes: %s", old_nodes)
        # LOGGER.debug("Extract old transitions: %s", old_transitions)
        # Some nodes are involved in the conditions of the transitions of interest
        # => These nodes have to be extracted
        old_nodes.update([
            self.model.node_dict[node_name]
            for node_name, transitions in self.model.signal_transition_dict.items()
            # Transition of interest encountered ?
            if set(transitions) & old_transitions
        ])

        # LOGGER.debug("Extract old nodes with extra cond nodes: %s", old_nodes)

        ## New model construction
        # Add nodes
        nodes_mapping = {old_node: tnode.add_copy(old_node) for old_node in old_nodes}
        # Add transitions
        for transition in old_transitions:
            new_trans = tnode.add_transition(
                nodes_mapping[transition.ori],
                nodes_mapping[transition.ext]
            )
            new_trans.set_condition(transition.condition)
            new_trans.set_event(transition.event)
            new_trans.set_action(transition.action)
            new_trans.set_note(transition.note)

        # Display in charter
        self.charter.add_edit_mvc(submodel.name, submodel, False)
        self.charter.do_layout(None, "hierarchical_LR")

    def get_selected_or_matching_node_names(self):
        """Get nodes names of interest

        Methods used to find nodes:
            - nodes selected in the list of the GUI
            - parse regex inserted in the search entry

        .. note:: selected items work in conjunction with regular expressions
            in the search entry.

        :return: List of names or None
        :rtype: <list <str>> or None
        """
        node_names = self.sn_viewer.get_selected_items()

        # If no nodes selected, use search entry
        regex = self.search_entry.get_text()
        if not regex:
            return node_names

        try:
            regex_obj = re.compile(regex)
        except Exception as e:
            cancel_warn("Incorrect regular expression:\n {}".format(e))
            return

        return list(set(node_names + self.model.get_matching_node_names(regex_obj)))

    def get_selected_items(self):
        """
        As it says
        """
        return self.sn_viewer.get_selected_items()

    def clear(self):
        """Remove all items"""
        self.sn_viewer.clear()


class SearchFrontier(SearchManager):
    """Same as SearchManager but specialized on frontier nodes
    """

    def __init__(self, chart, notebook, label):
        SearchManager.__init__(self, chart, notebook, label)

    def display_nodes(self):
        """Display node names on the widget"""
        # get node names
        lnode = self.get_frontier_node_names()
        lnode.sort()
        # display node names
        self.sn_viewer.refresh(lnode)

    def get_frontier_node_names(self):
        """
        As it says
        """
        fvi = FrontierVisitor()
        self.model.accept(fvi)
        return fvi.frontier


class LegendWindow(object):
    """
    Widget to display the legend
    """

    def __init__(self, parent=None):
        self.win = gtk.Window()
        self.win.set_title("CADBIOM-Chart Legend")
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.connect("destroy", self.on_destroy)
        self.win.connect("key_press_event", self.on_escape)
        # Favicon
        favicon = pkg_resources.resource_filename(
            __name__,
            "images/favicon.ico"
        )
        self.win.set_icon_from_file(favicon)

        # Legend
        image = gtk.Image()
        template = pkg_resources.resource_filename(
            __name__,
            "images/legend.png"
        )
        image.set_from_file(template)
        image.show()

        self.win.add(image)
        self.win.show_all()
        # register itself for parent or emvc
        if parent:
            parent.win_register(self)

        self.parent = parent

    def on_destroy(self, widget):
        """
        standard destroy callback
        """
        if self.parent:
            self.parent.win_remove(self)

    def destroy(self):
        """
        if registered as a child
        """
        if self.win:
            self.win.destroy()

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.destroy()


class ImportPIDParam(object):
    """
    Widget for model importing
    """

    def __init__(self, chart, parent=None):
        self.charter = chart

        # window creation
        template = pkg_resources.resource_filename(
            __name__,
            "chart_glade/import_parameter.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.main_window = self.wtree.get_widget("window1")
        self.main_window.set_title("Import window")

        self.main_window.set_resizable(True)
        hei = gtk.gdk.screen_height()
        hei = int(hei * 0.20)
        self.main_window.set_size_request(350, hei)

        # Set modal mode for the window (above all windows & block inputs)
        self.main_window.set_modal(True)
        if parent:
            self.main_window.set_transient_for(parent)

        if self.main_window:
            self.main_window.connect("destroy", self.on_destroy)
            self.main_window.connect("key_press_event", self.on_escape)

        self.main_window.set_position(gtk.WIN_POS_CENTER)

        # init param
        self.ai_inter = 0
        self.has_clock = False

        # interpretation radio button
        rbut = self.wtree.get_widget("or_rb")
        rb_name = rbut.get_name()
        rbut.connect("toggled", self.ai_inter_rb_callback, rb_name)

        rbut = self.wtree.get_widget("and_rb")
        rb_name = rbut.get_name()
        rbut.connect("toggled", self.ai_inter_rb_callback, rb_name)

        # Uncomment to add new buttons
#        rb = self.wtree.get_widget("or_and_rb")
#        rb_name = rb.get_name()
#        rb.connect("toggled", self.ai_inter_rb_callback, rb_name)
#
#        rb = self.wtree.get_widget("and_or_rb")
#        rb_name = rb.get_name()
#        rb.connect("toggled", self.ai_inter_rb_callback, rb_name)

        # clock radio button
        rbut = self.wtree.get_widget("withoutClock_rb")
        rbut.connect("toggled", self.clock_rb_callback, False)

        rbut = self.wtree.get_widget("withClock_rb")
        rbut.connect("toggled", self.clock_rb_callback, True)

        # import button
        button = self.wtree.get_widget("importButton")
        button.connect("clicked", self.on_import)

        # display
        self.main_window.show_all()

    def ai_inter_rb_callback(self, widget, ai_name):
        """
        set activator/inhibitor interpretation (and or or)
        """
        if ai_name == "or_rb":
            self.ai_inter = 0
        elif ai_name == "and_rb":
            self.ai_inter = 1

        # Uncomment to add new buttons
#        elif ai_name == "or_and_rb":
#            self.ai_inter = 2
#        else :
#            self.ai_inter = 3

    def clock_rb_callback(self, widget, has_clock):
        """
        set clock generation
        """
        if has_clock:
            self.has_clock = True
        else:
            self.has_clock = False

    def on_import(self, widget):
        """
        lauch import
        """
        fch = FileChooser(
            "Import from PID xml", "xml files", "*.xml", save_window=False
        )
        fch.do_action(self.import_from_pid_file)

    def import_from_pid_file(self, file):
        """
        compile a pid file
        """
        crep = CompilReporter()
        parser = MakeModelFromPidFile(file, crep, self.has_clock, self.ai_inter)
        if crep.error:
            DisplayError(crep, parser.model.name)
        else:
            model = parser.model
            model.modified = False
            self.charter.add_edit_mvc(model.name, model)
            self.destroy()

    def on_destroy(self, widget):
        """
        standard destroy callback
        """
        if self.main_window:
            self.main_window.destroy()

    def destroy(self):
        """
        for parents
        """
        self.on_destroy(None)

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.destroy()


class ImportBioPAXParams(object):
    """
    Widget for BioPAX model importing

    .. note:: requires biopax2cadbiom module
    """

    def __init__(self, chart, parent=None):
        self.charter = chart

        # biopax2cadbiom detection
        try:
            from biopax2cadbiom.commons import SPARQL_PATH
            from biopax2cadbiom.commons import SPARQL_LIMIT
        except ImportError:
            d_err = DisplayError(
                None,
                "biopax2cadbiom module is missing.",
                "biopax2cadbiom project is required to perform this task.\n"
                + "Please install it via the usual command:\n"
                + "pip install biopax2cadbiom",
            )
            d_err.main_window.set_modal(True)
            d_err.main_window.set_transient_for(parent)
            return

        # Init class variables (settings of the window)
        self.cadbiom_file = ""
        self.convert_full_graph = True
        self.graph_uris = list()
        self.provenance_uri = None
        self.numeric_compartments_names = False
        self.blacklist_file = None
        self.triplestore_url = SPARQL_PATH
        self.limit_sparql_results = SPARQL_LIMIT
        self.remove_strongly_connected_components = True

        # window creation
        template = pkg_resources.resource_filename(
            __name__,
            "chart_glade/import_BioPAX_parameters.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.main_window = self.wtree.get_widget("window1")
        self.main_window.set_title("Import window")
        self.main_window.set_resizable(True)
        self.main_window.set_position(gtk.WIN_POS_CENTER)

        # Set modal mode for the window (above all windows & block inputs)
        self.main_window.set_modal(True)
        if parent:
            self.main_window.set_transient_for(parent)

        if self.main_window:
            self.main_window.connect("destroy", self.on_destroy)
            self.main_window.connect("key_press_event", self.on_escape)

        # Init interface
        # Triplestore
        # Graphs URIs
        self.wtree.get_widget("text_graphs_uris").set_text(
            "http://reactome.org/mycobacterium"
        )
        # ProvenanceUri
        self.wtree.get_widget("text_provenance_uri").set_text("")
        # Triplestore URL
        self.wtree.get_widget("text_triplestore_url").set_text(self.triplestore_url)
        # BioPAX level
        self.wtree.get_widget("radio_biopax_level3").set_active(True)
        # BioPAX options
        self.wtree.get_widget("checkbox_convert_full_graph").set_active(False)
        self.wtree.get_widget("checkbox_full_compartment_names").set_active(True)
        self.wtree.get_widget("checkbox_remove_scc").set_active(True)

        # Connect buttons
        # Files
        self.wtree.get_widget("button_blacklist").connect(
            "clicked", self.on_import_blacklist_file
        )
        self.wtree.get_widget("button_output").connect(
            "clicked", self.on_set_output_file
        )
        self.wtree.get_widget("button_make_model").connect(
            "clicked", self.import_BioPAX_data
        )

        # Display
        self.main_window.show_all()

    def on_import_blacklist_file(self, widget):
        """
        Choose blacklist file of entities
        """
        fch = FileChooser(
            "Choose the blacklist file", "txt files", "*.txt", save_window=False
        )
        fch.do_action(self.set_blacklist_file)

    def on_set_output_file(self, widget):
        """
        Choose output model file
        """
        fch = FileChooser("Choose the output file name", "bcx files", "*.bcx")
        fch.do_action(self.set_output_file)
        # Change color to green
        self.wtree.get_widget("button_output").modify_bg(
            gtk.STATE_NORMAL, gtk.gdk.color_parse("green")
        )

    def set_blacklist_file(self, file):
        self.blacklist_file = file

    def set_output_file(self, file):
        self.cadbiom_file = file

    def import_BioPAX_data(self, widget):
        """
        Import from BioPAX data on triplestore
        """
        from biopax2cadbiom import biopax_converter

        # Return if output file is not set
        if self.cadbiom_file == "":
            red = gtk.gdk.color_parse("red")
            self.wtree.get_widget("button_output").modify_bg(gtk.STATE_NORMAL, red)
            return

        # Get parameters
        # List of graphs URIs
        self.graph_uris = (
            self.wtree.get_widget("text_graphs_uris").get_text().split(",")
        )

        # Provenance Uri
        provenance_uri = self.wtree.get_widget("text_provenance_uri").get_text()
        self.provenance_uri = provenance_uri if provenance_uri else None

        # Triplestore URL
        self.triplestore_url = self.wtree.get_widget("text_triplestore_url").get_text()

        # BioPAX level
        biopax2 = self.wtree.get_widget("radio_biopax_level2").get_active()
        self.graph_uris.append(
            "http://biopax.org/lvl2" if biopax2 else "http://biopax.org/lvl3"
        )

        # BioPAX convertion
        self.convert_full_graph = self.wtree.get_widget(
            "checkbox_convert_full_graph"
        ).get_active()
        self.numeric_compartments_names = self.wtree.get_widget(
            "checkbox_full_compartment_names"
        ).get_active()
        self.remove_strongly_connected_components = self.wtree.get_widget(
            "checkbox_remove_scc"
        ).get_active()

        # Color the button in green when the form is valid
        green = gtk.gdk.color_parse("green")
        self.wtree.get_widget("button_make_model").modify_bg(gtk.STATE_NORMAL, green)
        self.wtree.get_widget("button_make_model").set_label(
            "Make model. Please wait..."
        )

        # Do the magick
        # Build parameters for biopax2cadbiom
        params = {
            "cadbiomFile": self.cadbiom_file,
            "convertFullGraph": self.convert_full_graph,
            "listOfGraphUri": self.graph_uris,
            "pickleBackup": False,
            "pickleDir": "",  # don't care, because pickleBackup = False
            "numericCompartmentsNames": self.numeric_compartments_names,
            "blacklist": self.blacklist_file,
            "triplestore": self.triplestore_url,
            "no_scc_fix": True,  # StartNodes are added here
            "limit_sparql_results": self.limit_sparql_results,
            "provenanceUri": self.provenance_uri,
        }

        try:
            # StartNodes are added here, (not in biopax2cadbiom)
            # so we can load the model in memory
            biopax_converter.main(params)

            if self.remove_strongly_connected_components:
                model = model_corrections.add_start_nodes(self.cadbiom_file)
            else:
                model = MakeModelFromXmlFile(self.cadbiom_file).model

            self.charter.add_edit_mvc(model.name, model)
            self.destroy()

        except Exception as e:

            d_err = DisplayError(
                None,
                "Biopax2cadbiom",
                "Biopax2cadbiom exception: "
                + e.__class__.__name__
                + ". Please check logs.\n"
                + traceback.format_exc(),
            )
            d_err.main_window.set_modal(True)

    def on_destroy(self, widget):
        """
        standard destroy callback
        """
        if self.main_window:
            self.main_window.destroy()

    def destroy(self):
        """
        for parents
        """
        self.on_destroy(None)

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.destroy()
