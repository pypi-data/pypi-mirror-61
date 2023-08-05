# -*- coding: utf-8 -*-
## Filename    : chart_checker_controler.py
## Author(s)   : Michel Le Borgne
## Created     : 05/2011
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
Collection of widgets for properties checking

Classes:

- :class:`ChartChecker`: GUI interface for query checking
- :class:`QueryCheckingForm`: Main form of ChartChecker Window
- :class:`SolutionWindow`: Show solutions found by the solver
- :class:`PropertyVisitor`: Used to parse places in a start property and force
  their use by the simulator
- :class:`InhibWindow`: Show inhibitors - Not used anymore

"""
from collections import defaultdict
import traceback
import pkg_resources

import gtk

from cadbiom.models.clause_constraints.mcl.MCLAnalyser import MCLAnalyser
from cadbiom_gui.gt_gui.chart_simulator.chart_simul_controler import ChartSimulControler
from cadbiom_gui.gt_gui.chart_simulator.chart_chrono import ChartChrono
from cadbiom_gui.gt_gui.utils.warn import ok_warn, cancel_warn, confirm
from cadbiom_gui.gt_gui.utils.reporter import CompilReporter
from cadbiom.models.guard_transitions.simulator.chart_simul import ChartSimulator
from cadbiom.models.clause_constraints.mcl.MCLQuery import MCLSimpleQuery

from cadbiom.models.biosignal.sig_expr import SigBinExpr
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond

from cadbiom import commons as cm

LOGGER = cm.logger()


class ChartChecker(object):
    """Provides a GUI interface for query checking"""

    def __init__(self, emvc, reporter, parent=None):
        self.__emvc = emvc  # edit mvc - link with charter
        self.__reporter = reporter
        self.__occ_form = QueryCheckingForm(emvc, reporter)
        self.__current_form = self.__occ_form

        # graphical interface
        self.__main_window = gtk.Window()
        self.__main_window.set_title("Property check: " + self.__emvc.model.name)
        self.__main_window.connect("destroy", self.__on_destroy)
        self.__main_window.set_position(gtk.WIN_POS_CENTER)
        self.__main_window.resize(600, 300)

        if parent:
            # Set window above all windows
            self.__main_window.set_transient_for(parent.main_window)

        # Event on_escape key pressed
        self.__main_window.connect("key_press_event", self.on_escape)

        # register as auxiliary window
        self.__emvc.win_register(self)

        # display
        self.__main_window.add(self.__current_form.get_frame())
        self.__main_window.show_all()

    def __on_destroy(self, widget):
        """
        delete window and dependant sub widgets
        """
        self.__current_form.clean_subwin()
        if self.__main_window:
            self.__main_window.destroy()

    def destroy(self):
        """
        call back adaptor
        """
        self.__on_destroy(None)

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.__main_window.destroy()


class QueryCheckingForm(object):
    """General simple query checking; used by ChartChecker

    .. TODO::
        Exemple example_model.bcx:
        Final property: "C"
        Start property: A and G

        Pourquoi G se retrouve dans les places frontières des solutions et pas A ?
        Car c'est déjà une frontière et pas A...
        => bug ?
    """

    def __init__(self, emvc, er_rep):
        self.__emvc = emvc
        self.__model = emvc.model  # chart model
        self.__mcla = None  # clause constraint model analyser
        self.__error_reporter = er_rep
        template = pkg_resources.resource_filename(
            __name__, "../chart_glade/occurence_form.glade"
        )
        self.__wtree = gtk.glade.XML(template)
        self.__window = self.__wtree.get_widget("windowOcc")
        wid = self.__wtree.get_widget("frameOcc")
        self.__frame = wid.get_child()
        wid.remove(self.__frame)

        # information
        happen_button = self.__wtree.get_widget("possible")
        happen_button.set_active(True)
        self.property_happen = True
        happen_button.connect("toggled", self.rb_callback, "p")
        never_happen_button = self.__wtree.get_widget("impossible")
        never_happen_button.connect("toggled", self.rb_callback, "i")

        self.step_entry = self.__wtree.get_widget("max_step")
        self.step_entry.set_text("10")
        self.step_entry.connect("changed", self.on_entry_changed)
        self.property_entry = self.__wtree.get_widget("property_entry")
        self.property_entry.connect("changed", self.on_entry_changed)
        self.inv_prop_entry = self.__wtree.get_widget("property_entry2")
        self.inv_prop_entry.connect("changed", self.on_entry_changed)
        self.start_prop_entry = self.__wtree.get_widget("property_entry3")
        self.start_prop_entry.connect("changed", self.on_entry_changed)

        # yes/no button
        is_satisfiable_button = self.__wtree.get_widget("button_yn")
        is_satisfiable_button.connect("clicked", self.on_yn)
        # conditions button
        search_solutions_button = self.__wtree.get_widget("button_cond")
        search_solutions_button.connect("clicked", self.on_cond)

        # condition exploration
        self.max_sol_entry = self.__wtree.get_widget("entry_nbsol")
        self.max_sol_entry.set_text("10")
        self.max_sol_entry.connect("changed", self.on_entry_changed)
        self.but_solutions = self.__wtree.get_widget("but_solutions")
        self.but_solutions.connect("clicked", self.on_solutions)
        self.but_solutions.set_sensitive(False)

        self.but_mac = self.__wtree.get_widget("but_mac")
        self.but_mac.connect("clicked", self.on_mac)
        self.but_mac.connect("clicked", self.on_entry_changed)
        self.but_mac.set_sensitive(False)


        # Tooltips
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(
            self.property_entry,
            "Final property that will occur at the end of the simulation.\n"
            "The writing of this field obeys a syntax of propositional logic. "
            "Concretely, you must specify the name of the entities of interest "
            "linked by logical operators (NOT or AND). Parentheses are allowed.",
        )
        self.tooltips.set_tip(
            self.start_prop_entry,
            "Property that will be part of the initial state of the model.\n"
            "In concrete terms, some entities can be activated by this mechanism "
            "without modifying the model.",
        )
        self.tooltips.set_tip(
            self.inv_prop_entry,
            "Invariant property that will never occur during the simulation.\n"
            "The given logical formula will be enclose by a logical not() and "
            "will be checked at each step of the simulation.",
        )
        self.tooltips.set_tip(is_satisfiable_button, "Run a quick satisfiability test")
        self.tooltips.set_tip(
            search_solutions_button,
            "Search non optimal solutions.\n"
            "If non-optimal solutions are found, the search for optimal "
            "solutions (Minimal Activation Condition) will be unlocked.",
        )
        self.tooltips.set_tip(self.but_solutions, "Show non-optimal solutions")
        self.tooltips.set_tip(
            self.but_mac,
            "Search and display MACs (Minimal Activation Conditions).\n"
            "This process can be expensive depending on the model considered. "
            "Command line access is recommended for the heaviest tasks.",
        )

        self.tooltips.enable()
        self.tooltips.set_delay(cm.TOOLTIPS_DELAY)

        # children
        self.__aux_win = []

    def get_frame(self):
        """
        as name says
        """
        return self.__frame

    def rb_callback(self, widget, idw):
        """
        happen and never happen call back
        """
        if idw == "p":
            self.property_happen = True
        else:
            self.property_happen = False

    def on_entry_changed(self, widget):
        """
        react in cas of change in entries
        """
        #  buttons
        self.but_solutions.set_sensitive(False)
        self.but_mac.set_sensitive(False)

    def on_yn(self, widget):
        """
        lauch a satisfiability test
        """

        def is_satisfiable(query, max_step):
            """Launch the solver processing, catch/print exceptions, warn the user"""
            try:
                reachable = self.mcla.sq_is_satisfiable(query, max_step)

            except Exception as e:
                LOGGER.error("QueryCheckingForm:on_yn: %s", e)
                print(traceback.format_exc())
            finally:
                # Check the reporter
                if self.__error_reporter.error:
                    cancel_warn(self.__error_reporter.memory)
                    self.__error_reporter.reset()
                    return

            if reachable:
                ok_warn("Yes, we can!", "green")
            else:
                ok_warn("NO", "red")

        # get info
        final_prop = self.property_entry.get_text()
        if len(final_prop) == 0:
            cancel_warn("Missing property")
            return
        inv_prop = self.inv_prop_entry.get_text()
        start_prop = self.start_prop_entry.get_text()
        max_step_str = self.step_entry.get_text()
        if len(max_step_str) == 0:
            cancel_warn("Number of steps not specified")
            return
        max_step = int(max_step_str)
        self.mcla = MCLAnalyser(self.__error_reporter)
        self.mcla.build_from_chart_model(self.__model)
        if self.__error_reporter.error:
            cancel_warn(self.__error_reporter.memory)
            self.__error_reporter.reset()
            return

        # solve happen/never happen problem
        if self.property_happen:
            if len(inv_prop) == 0:
                inv_prop = None
            else:
                # Enclose the invariant property in a logical not
                inv_prop = "not (" + inv_prop + ")"

            if len(start_prop) == 0:
                start_prop = None

            query = MCLSimpleQuery(start_prop, inv_prop, final_prop)

        else:
            if len(inv_prop) != 0:
                # Enclose final AND invariant properties in a logical not
                final_prop = "not (" + final_prop + " and " + inv_prop + ")"

            query = MCLSimpleQuery(start_prop, inv_prop, None)

        is_satisfiable(query, max_step)

    def on_cond(self, widget):
        """Launch solution computations
        If solutions are found, MAC search is unlocked.
        """

        def search_solutions(query, max_step, max_sol):
            """Launch the solver processing, catch/print exceptions, warn the user"""
            try:
                solutions = self.mcla.sq_frontier_solutions(query, max_step, max_sol)

                LOGGER.debug(
                    "QueryCheckingForm.on_cond:: Solutions: %s", len(solutions)
                )

            except Exception as e:
                LOGGER.error("QueryCheckingForm:on_cond: %s", e)
                print(traceback.format_exc())
            finally:
                # Check the reporter
                if self.__error_reporter.error:
                    cancel_warn(self.__error_reporter.memory)
                    self.__error_reporter.reset()
                    return

            return solutions

        # desactivate buttons
        self.but_solutions.set_sensitive(False)
        self.but_mac.set_sensitive(False)

        # get info
        final_prop = self.property_entry.get_text()
        if len(final_prop) == 0:
            cancel_warn("Missing property")
            return
        inv_prop = self.inv_prop_entry.get_text()
        start_prop = self.start_prop_entry.get_text()
        max_step_str = self.step_entry.get_text()
        if len(max_step_str) == 0:
            cancel_warn("Number of steps not specified")
            return
        max_step = int(max_step_str)
        max_sol_str = self.max_sol_entry.get_text()
        if len(max_sol_str) == 0:
            cancel_warn("Number of solutions not specified")
            return
        max_sol = int(max_sol_str)

        self.mcla = MCLAnalyser(self.__error_reporter)
        self.mcla.build_from_chart_model(self.__model)
        if self.__error_reporter.error:
            cancel_warn(self.__error_reporter.memory)
            self.__error_reporter.reset()
            return

        # solve happen/never happen problem
        if self.property_happen:
            LOGGER.debug("QueryCheckingForm.on_cond:: Solve happen problem!")

            if len(inv_prop) == 0:
                inv_prop = None
            else:
                # Enclose the invariant property in a logical not
                inv_prop = "not (" + inv_prop + ")"

            if len(start_prop) == 0:
                start_prop = None

            query = MCLSimpleQuery(start_prop, inv_prop, final_prop)

        else:
            LOGGER.debug("QueryCheckingForm.on_cond:: Solve never happen problem!")

            if len(inv_prop) != 0:
                # Enclose final AND invariant properties in a logical not
                final_prop = "not (" + final_prop + " and " + inv_prop + ")"

            query = MCLSimpleQuery(start_prop, inv_prop, None)

        self.lsol = search_solutions(query, max_step, max_sol)

        if self.lsol is None:
            return

        # affectation
        self.property = final_prop
        self.inv_prop = inv_prop
        self.start_prop = start_prop
        self.max_step = max_step
        self.max_sol = max_sol

        if len(self.lsol) == 0:
            cancel_warn("No solution")
            return

        # activate buttons
        self.but_solutions.set_sensitive(True)
        self.but_mac.set_sensitive(True)

    def on_solutions(self, widget):
        """
        display solutions
        """
        SolutionWindow(self.lsol, self.__emvc, self.__error_reporter, self)

    def on_mac(self, widget):
        """
        launch mac computations
        """
        ask = confirm(
            None,
            "This process takes time.\n"
            + "The interface may freeze during this time.\n"
            + "Do you want to continue?",
        )
        if ask:
            query = MCLSimpleQuery(self.start_prop, self.inv_prop, self.property)
            mac_list = tuple(self.mcla.mac_search(query, self.max_step))
            if not mac_list:
                ok_warn(
                    "The solver could not find a MAC,\n"
                    + "you should refine your query."
                )
            else:
                # MACs solutions
                SolutionWindow(
                    mac_list,
                    self.__emvc,
                    self.__error_reporter,
                    self,
                    title=str(len(mac_list)) + " Minimal Activation Conditions",
                )

    # sub windows management
    def win_register(self, win):
        """
        register sub window for destroy
        """
        self.__aux_win.append(win)

    def win_remove(self, win):
        """
        used when the sub window destroys itself
        """
        if win in self.__aux_win:
            self.__aux_win.remove(win)

    def clean_subwin(self):
        """
        destroy all registered subwindows
        """
        for win in self.__aux_win:
            win.destroy()

    def destroy(self):
        """
        destroy all
        """
        self.clean_subwin()
        if self.__window:
            self.__window.destroy()


class SolutionWindow(object):
    """Show solutions (non-optimal or Minimal Activation Conditions)"""

    def __init__(self, l_fsol, emvc, reporter, parent, title=""):
        """
        @param l_fsol: list<FrontierSolution>
        @param emvc: edit_mvc
        @param reporter: Classical reporter
        @param parent: parent widget
        """
        self.emvc = emvc
        self.reporter = reporter
        # frontier place list extraction and ic sequence extraction
        self.l_solutions = []
        self.l_icseq = []
        for fsol in l_fsol:
            self.l_solutions.append(fsol.sorted_activated_frontier)
            self.l_icseq.append(fsol.ic_sequence)

        self.aux_win = []
        self.simul = None

        self.compt = 0
        self.choice = 0
        self.textview_list = []

        # window creation
        template = pkg_resources.resource_filename(
            __name__, "../chart_glade/checker_solutions.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.window = self.wtree.get_widget("window1")
        # Favicon
        favicon = pkg_resources.resource_filename(
            __name__,
            "../images/favicon.ico"
        )
        self.window.set_icon_from_file(favicon)

        self.window.set_resizable(True)
        height = gtk.gdk.screen_height()
        height = int(height * 0.30)
        self.window.set_size_request(700, height)
        # Ability to destroy opened ChartSimulControler
        self.window.connect("destroy", self.on_destroy)
        # Event on_escape key pressed
        self.window.connect("key_press_event", self.on_escape)

        # Info label: Set title
        if title:
            info = self.wtree.get_widget("label_nbsol")
            info.set_text(title)
        else:
            info = self.wtree.get_widget("label_nbsol")
            info.set_text(str(len(self.l_solutions)) + " solutions found")

        # button save choice
        save_choice_button = self.wtree.get_widget("but_sv_choice")
        save_choice_button.connect("clicked", self.on_save, False)

        # button save all
        save_all_button = self.wtree.get_widget("but_sv_all")
        save_all_button.connect("clicked", self.on_save, True)
        if len(self.l_solutions) == 1:
            save_all_button.set_sensitive(False)

        # button frame
        self.frame_sol = self.wtree.get_widget("frame_sol")
        vbox = gtk.VBox(False, 0)
        self.frame_sol.add(vbox)
        vbox.show()

        scroll = gtk.ScrolledWindow()
        vbox.pack_start(scroll)

        vbox2 = gtk.VBox()
        scroll.add_with_viewport(vbox2)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.button_group = None

        frame = self.build_button_frame(self.l_solutions[0])
        vbox2.pack_start(frame)

        for sol in self.l_solutions[1:]:
            hsep = gtk.HSeparator()
            vbox2.pack_start(hsep, False, False)

            frame = self.build_button_frame(sol, self.button_group)
            vbox2.pack_start(frame)

        # Buttons
        # button inhibitor => Disabled unknown function, See .glade to reactivate
        # inhibitor_button = self.wtree.get_widget("but_inhib")
        # inhibitor_button.connect("clicked", self.on_inhib)
        # inhibitor_button.set_sensitive(False)
        # button simulation
        simulation_button = self.wtree.get_widget("but_simul")
        simulation_button.connect("clicked", self.on_simul)
        # button chronogram
        chronogram_button = self.wtree.get_widget("but_chrono")
        chronogram_button.connect("clicked", self.on_chrono)

        # Tooltips
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(
            save_choice_button,
            "Export the selected solution and its trajectory of events to a file",
        )
        self.tooltips.set_tip(
            save_all_button,
            "Export all the solutions and their trajectories of events to a file",
        )
        self.tooltips.set_tip(
            simulation_button,
            "Replay the selected trajectory step by step on the model",
        )
        self.tooltips.set_tip(
            chronogram_button,
            "Display the chronogram of the activation of the places in "
            "the selected trajectory",
        )

        self.tooltips.enable()
        self.tooltips.set_delay(cm.TOOLTIPS_DELAY)

        # register
        parent.win_register(self)
        self.parent = parent

        # display
        self.window.show_all()
        # gtk.main()

    def on_destroy(self, widget):
        """
        when leaving the window
        """
        self.clean_subwin()
        if self.simul:
            self.simul.on_destroy(None)
        self.win_remove(self)

    def destroy(self):
        """
        when leaving the window
        """
        self.clean_subwin()
        if self.simul:
            self.simul.on_destroy(None)
        if self.window:
            self.window.destroy()

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.window.destroy()

    def build_button_frame(self, state_list, group=None):
        """
        ???
        """
        template = pkg_resources.resource_filename(
            __name__, "../chart_glade/button_frame.glade"
        )
        wtree = gtk.glade.XML(template)
        wid = wtree.get_widget("button_frame")
        frame = wid.get_child()
        wid.remove(frame)

        # textview
        tname = "tw" + str(self.compt)
        text = wtree.get_widget("textview")
        text.set_name(tname)

        text_buffer = text.get_buffer()
        str_state = "\n"
        for state in state_list:
            str_state += state + "\t"
        str_state += "\n"
        text_buffer.set_text(str_state)
        text.set_editable(False)

        self.textview_list.append(state_list)

        # radio button
        rname = "rb" + str(self.compt)
        rbut = wtree.get_widget("rButton")
        rbut.set_name(rname)

        if group:
            rbut.set_group(group)
        else:
            self.button_group = rbut
            rbut.set_active(True)

        rbut.connect("toggled", self.rb_callback, self.compt)
        self.compt += 1
        return frame

    def rb_callback(self, widget, id_frame):
        """
        radio button call_back
        """
        self.choice = id_frame

    def on_save(self, widget, all_sol=True):
        """
        open a window to save as xml file
        @param all_sol : boolean - True if we take all solutions
        """
        choice = gtk.FileChooserDialog(
            "Save solution",
            None,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK),
        )
        choice.set_default_response(gtk.RESPONSE_OK)

        # add a filter to see only xml files for biochart (*.txt)
        ffilter = gtk.FileFilter()
        ffilter.set_name("txt files")
        ffilter.add_pattern("*.txt")
        choice.add_filter(ffilter)

        # add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            self.create_solution_file(choice.get_filename(), all_sol)
        elif response == gtk.RESPONSE_CANCEL:
            pass
            # print 'Closed, no files selected'
        choice.destroy()

    def create_solution_file(self, sol_file, all_bool):
        """
        make a xml file with the current model
        """
        if all_bool:
            init_places = self.l_solutions
            input_clocks = self.l_icseq
        else:
            init_places = [self.l_solutions[self.choice]]
            input_clocks = [self.l_icseq[self.choice]]

        sfile = open(sol_file, "w")
        for i in range(len(init_places)):
            spla = init_places[i]
            icseq = input_clocks[i]
            for elemt in spla:
                sfile.write(str(elemt) + "\t")
            for ica in icseq:
                sfile.write("\n" + ica)
            sfile.write("\n")
        sfile.close()

    def on_inhib(self, widget):
        """
        Compute inhibitors
        """
#
#        start_list = self.l_solutions[self.choice]
#        start_p = logical_and(start_list)
#        inv_p = 'not('+self.parent.property+')'
#        mac_list = self.parent.mcla.mac_search(start_p, inv_p, None,
#                                               self.parent.max_step)
#        inhib_list = []
#        for mac in mac_list:
#            im = []
#            for var in mac:
#                if var in start_list:
#                    continue
#                else:
#                    im.append(var)
#            if im:
#                inhib_list.append(im)
#        if len(inhib_list) == 0:
#            cancel_warn("This solution has not inhibitor")
#        else :
#            Inhib_Window(inhib_list, self.emvc, self.reporter, self)
        pass

    def on_simul(self, widget):
        """Launch simulation of a solution

        .. note:: We also parse the start property since it can activate some
            places (other than frontiers), whose are required for the simulator
            to operate properly.
            Indeed, the simulator accepts to fire transitions only if places
            are activated for a given step.

        .. note:: Mentionner une place frontière en start property va l'activer
            directement et graphiquement; init_places va donc la contenir et
            les solutions également.
            **Cela n'est pas le cas pour une place autre, non frontière**.
            Ici nous rétablissons simplement la liste de places init_places pour
            que le simulateur fonctionne correctement en activant dans le
            graph editor les bonnes places/transitions à chaque étape.

        .. todo:: Mettre à jour les solutions en y ajoutant les places dans
            start property?
        """
        if self.simul:
            self.simul.on_destroy(None)

        # Cast to avoid further modification of the original data
        init_places = list(self.l_solutions[self.choice])

        start_property = self.parent.start_prop
        self.emvc.model.transition_list

        if start_property:
            # Start property parsing
            LOGGER.debug(
                "SolutionWindow:on_simul:\n"
                "   start_property: %s\n"
                "   init_places: %s\n",
                start_property,
                init_places,
            )

            tree_prop = compile_cond(
                start_property,
                # Fake symbol_table: for the parser sigexpr_compiler
                # {'A': ('state', 0), 'C': ('state', 0), ...}
                defaultdict(lambda: ("state", 0)),
                CompilReporter(),
            )

            LOGGER.debug(
                "SolutionWindow:on_simul: tree prop %s %s", tree_prop, repr(tree_prop)
            )

            prop_visitor = PropertyVisitor()
            tree_prop.accept(prop_visitor)
            init_places += prop_visitor.nodes

            LOGGER.debug("SolutionWindow:on_simul: init_places", init_places)


        input_clocks = self.l_icseq[self.choice]
        LOGGER.debug("SolutionWindow:on_simul: clocks", input_clocks)

        # Remove duplicates
        init_places = list(set(init_places))

        self.simul = ChartSimulControler(
            self.emvc, True, self.reporter, init_places, input_clocks, self
        )

    def on_chrono(self, widget):
        """
        Show a chronogram of a trajectory initialized with solution
        """
        # stand alone simulator
        sim = ChartSimulator()
        sim.build(self.emvc.model, True, self.reporter)

        chrono = ChartChrono.for_trajectory(sim)
        self.win_register(chrono)

        # simulation
        init_places = self.l_solutions[self.choice]
        input_clocks = self.l_icseq[self.choice]
        sim.simul_init_places(init_places)
        # input buffer is any input
        if input_clocks:
            sim.set_act_input_stream(input_clocks)
        i = 0
        while i <= self.parent.max_step:
            chrono.register(sim)
            try:
                sim.simul_step()
                i += 1
            except Exception:
                break
        # clean model
        self.emvc.model.clean()
        self.emvc.model.notify()
        # display
        chrono.display_selected_chrono()

    # sub windows management
    def win_register(self, win):
        """
        sub windows management
        """
        if win.__class__ == ChartSimulControler:
            self.simul = win
        self.aux_win.append(win)

    def win_remove(self, win):
        """
        sub windows management
        """
        if win in self.aux_win:
            self.aux_win.remove(win)
        if win == self.simul:
            self.simul = None

    def clean_subwin(self):
        """
        sub windows management
        """
        for win in self.aux_win:
            win.destroy()
        self.aux_win = []


class PropertyVisitor(object):
    """Translate a SigExpression (condition of a transition) into a set of nodes
    that satisfy the condition.

    Used to force the simulator to use nodes mentioned in a start property by
    the user.

    Non mandatory nodes (inhibitors) are not retained.
    Activators can be accessed in the attribute 'nodes'
    """

    def __init__(self):
        self.nodes = list()
        # Flag used to detect if we are in a leaf on in the root of the tree
        # If this is the root, we can set the attribute self.nodes and return
        self.root = True

    def visit_sig_ident(self, tnode):
        """ident -> keep the node"""
        # print("ident node", str(tnode))

        node_name = [tnode.name]
        if self.root:
            self.nodes = node_name
        else:
            return node_name

    def visit_sig_not(self, node):
        """translate a not

        Do not retain the subnode if it is an "ident" node.
        Retain only subnodes if they are in a binary expression linked by a logical "and".

        Because:

            - not (a or b) is valid only if a and b are False;
              thus we don't care of a and b
            - not (a and b) is valid only if a or b are True, or if a and b are False;
              thus a and b can be True alternately and it is sufficient for us.
        """
        # print("not node:", str(node))
        root = self.root
        self.root = False
        subnodes = node.operand.accept(self)

        nodes = []

        if isinstance(node, SigBinExpr):
            # print("operator:", node.operator)

            if node.operator == "and":
                nodes = subnodes

        if root:
            self.nodes = nodes
            return
        return []

    def visit_sig_sync(self, binnode):
        """translate a binary (or/and) expression"""
        # recursive visits
        root = self.root
        self.root = False

        # print("sig sync found", str(binnode))
        nl1 = binnode.left_h.accept(self)
        nl2 = binnode.right_h.accept(self)
        # print("sig sync end", binnode.operator, nl1, nl2, str(binnode))

        nodes = nl1 + nl2

        if root:
            self.nodes = nodes
            return
        return nodes


class InhibWindow(SolutionWindow):
    """Show inhibitors of the current solution

    Not used anymore (code disabled)
    """

    def __init__(self, l_solutions, emvc, reporter, parent):

        SolutionWindow.__init__(
            self,
            l_solutions,
            emvc,
            reporter,
            parent,
            title=str(len(l_solutions)) + " inhibitors",
        )

        # button inhibitor
        button = self.wtree.get_widget("but_inhib")
        button.connect("clicked", self.on_inhib)
        button.set_sensitive(False)


def logical_and(list):
    """
    @return: logical_formula: str - AND of the input list
    """

    if len(list) == 0:
        return
    elif len(list) == 1:
        return list[0]
    else:
        logical_formula = ""
        for elemnt in list:
            logical_formula += elemnt + " and "
        logical_formula = logical_formula[:-5]
        #        print logical_formula
        return "(" + logical_formula + ")"
