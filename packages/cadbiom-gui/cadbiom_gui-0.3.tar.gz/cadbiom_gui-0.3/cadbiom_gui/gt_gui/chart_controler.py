# -*- coding: utf-8 -*-
## Filename    : chart_controler.py
## Author(s)   : Michel Le Borgne
## Created     : 4/3/2010
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
##     http:
##     mailto:
##
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""Main GUI controllers + auxiliary class (ChartClipboard)

- :class:`ChartClipboard`: A clipboard to handle the copy of nodes through models
- :class:`ChartControler`: A controler for graphical views
- :class:`NavControler`: A controler for navigation view (overview section in the GUI)

"""
# Standard imports
from __future__ import print_function
import itertools as it
from string import ascii_uppercase
from math import sqrt
import re

# Custom imports
import gtk
from gtk.gdk import (
    Cursor,
    ARROW,
    BOTTOM_LEFT_CORNER,
    BOTTOM_RIGHT_CORNER,
    TOP_LEFT_CORNER,
    TOP_RIGHT_CORNER,
    LINE_ON_OFF_DASH,
)

# Cadbiom imports
from cadbiom_gui.gt_gui.graphics.drawing_style import Arrow
from cadbiom.models.guard_transitions.chart_model import CMacroNode, CNode, CSimpleNode
from cadbiom import commons as cm

LOGGER = cm.logger()


class ChartClipboard(object):
    """A clipboard used by ChartControler to handle the copy of nodes through models.
    """

    def __init__(self):
        self.clip_node = None

    def put_node(self, node):
        """register a chart model node in the clipboard"""
        self.clip_node = node

    def get_node(self):
        """retrieve the current node in the clipboard"""
        node = self.clip_node
        self.clip_node = None
        return node

    def has_element(self):
        """test if the clipboard has a registered node"""
        return self.clip_node is not None

    def has_macro(self):
        """test if the clipboard has a registered macro node"""
        return self.clip_node.is_macro() if self.clip_node else False


class ChartControler(object):
    """Implement a controler for graphical views

    Used by::

        - the main graph editor widget as this
        - NavControler for the overview widget through inheritance

    Signals::

        - current_change: Inform CharterInfo that the currently selected transition,
        model or node has changed. Used to dispatch related information in the GUI.
        - edit_node: Inform Charter that a MacroNode will be edited.

    TODO: just show metadata on double click on another item
    => add a signal to inform CharterInfo objects

    :param model: Current chart model
    :param mouse_role: Mouse action "select", "resizing", "moving"
    :param current_node: Currently selected node
    :param current_node_center: Tuple of coordinates (x, y) of the current node
    :param current_handle: Id of the node corner currently selected for resizing
        (only for MacroNodes)
    :param current_transition: Currently selected transition
    :param m_vscreen_coord: Mouse virtual screen coordinates (xloc, yloc)
    :param lastx: coordinates of last click in view
    :param lasty: coordinates of last click in view
    :param clipboard: Clipboard object used to copy nodes through models
    :param drawing_style:
    :param signal_dict: Structure to assign observers to each signal of ChartControler
    :param gen_name: Generator of unique names for new nodes
    :param node_copy_count: Generator of ints used in the naming of copied nodes

    :type model: <ChartModel>
    :type mouse_role: <str>
    :type current_node: <CNode>
    :type current_node_center: <tuple <float>,<float>>
    :type current_handle: <int>
    :type current_transition: <CTransition>
    :type m_vscreen_coord: <tuple <float>,<float>>
    :type lastx: <float>
    :type lasty: <float>
    :type clipboard: <ChartClipboard>
    :type drawing_style:
    :type signal_dict: <dict <str>:<list>>
    :type gen_name: <generator>
    :type node_copy_count: <generator>
    """

    cursors = []
    cursors.append(Cursor(ARROW))
    cursors.append(Cursor(TOP_LEFT_CORNER))
    cursors.append(Cursor(TOP_RIGHT_CORNER))
    cursors.append(Cursor(BOTTOM_RIGHT_CORNER))
    cursors.append(Cursor(BOTTOM_LEFT_CORNER))
    LSIGNALS = ["current_change", "edit_node"]

    def __init__(self, model, clipboard):
        self.model = model
        # mouse role
        self.mouse_role = "select"
        # Set default node
        self.current_node = self.model.get_root()
        # Note: current_node_center should be initialized to None
        # only if current_node is also None...
        self.current_node_center = None
        self.current_handle = 0
        self.current_transition = None
        # coordinate of last click in virtual screen 1x1
        self.m_vscreen_coord = None
        # coordinates of last click in view
        self.lastx = 0
        self.lasty = 0
        self.clipboard = clipboard
        self.drawing_style = None
        self.signal_dict = {signal: list() for signal in self.LSIGNALS}

        # Generator for the auto-naming of new nodes
        self.gen_name = self.nodes_names_generator()
        # Generator for the auto-naming of copied nodes
        self.node_copy_count = it.count(1)

    def attach(self, signal, obs):
        """Register an observer for the given signal

        :param signal: Name of the signal ("current_change" or "edit_node")
        :param obs: The observer
        :type signal: <str>
        :type obs: <CharterInfo> or <Charter>
        """
        lobs = self.signal_dict[signal]
        if not obs in lobs:
            lobs.append(obs)

    def detach(self, signal, obs):
        """Remove an observer for the given signal

        :param signal: Name of the signal ("current_change" or "edit_node")
        :param obs: The observer
        :type signal: <str>
        :type obs: <CharterInfo> or <Charter>
        """
        self.signal_dict[signal].remove(obs)

    def notify(self, signal):
        """Emit a signal subsequently to a mouse action

        - current_change: Tell CharterInfo that the current selection has changed
        - edit_node: Tell Charter that the current MacroNode will be edited

        :param signal: name of the signal
        :type signal: <str>
        """
        LOGGER.debug("ChartControler notify signal: %s to %s", signal, self.signal_dict[signal])

        lobs = self.signal_dict[signal]
        if signal == "current_change":
            # Tell CharterInfo that the selection has changed
            for obs in lobs:
                obs.update(self.current_node, self.current_transition)
        elif signal == "edit_node":
            # Tell Charter that the MacroNode will be edited
            for obs in lobs:
                obs.update(self.current_node)
        else:
            raise Exception("ChartControler: Unknown signal")

    def set_view(self, view):
        """
        As it says
        """
        self.view = view

    def set_mouse_role(self, role):
        """
        As it says
        """
        self.mouse_role = role

    def on_button_press(self, widget, event):
        """Callback when a mouse button is pressed on the DrawingArea
        (contained in the ChartView object)

        - Detect the current element under the mouse (node or transition)
        - Select it, and notify observers
        - Interpret mouse actions according to the current mouse role::

            - Double click: Edit the node if it is a MacroNode
            - Left click: Resize (a MacroNode) or move
            - Right click: Open context menu

        TODO: just show metadata on double click on another item

        :param widget: gtk DrawingArea that emit the event
        :param event: gdk mouse event with attributes (x, y)
        :type widget: <NavView> or <ChartView>
        :type event: <gtk.gdk.Event>
        """
        self.lastx = event.x
        self.lasty = event.y

        # cursor coordinates in virtual screen 1x1
        xloc = event.x / self.view.draw_width
        yloc = event.y / self.view.draw_height
        self.m_vscreen_coord = (xloc, yloc)

        # Get current object under the mouse
        (node, handle, center, trans) = self.model.find_element(
            self.m_vscreen_coord, self.drawing_style
        )

        # Note: We are always in a node, which one?
        if node == self.model.get_root():
            # we found the root of the sub_model - no resizing allowed
            handle = 0
        self.current_handle = handle


        if self.current_node != node:
            # Node detected, update current node and notify observers
            if self.current_node:
                self.current_node.selected = False

            self.current_node = node
            node.selected = True
            self.current_node_center = center

            # Notify that we have found something (red color for selected element)
            self.notify("current_change")
            # For deselection, see at the end of the transitions block
            self.model.notify()

        if self.current_transition != trans:
            # Transition detected, update current node/transition and notify observers
            if self.current_transition:
                self.current_transition.selected = False

            if trans:
                node.selected = False
                trans.selected = True
                self.current_transition = trans
            else:
                self.current_transition = None

            # Notify that we have found something (red color for selected element)
            self.notify("current_change")
            # TODO: Don't know why, but the transitions requires
            # a notification to the model (this is not the case for nodes that
            # can be selected without notify but still require notify to deselect..)
            self.model.notify()


        # Action (depending on mouse button and event type)
        if event.type == gtk.gdk._2BUTTON_PRESS:
            # Double click
            self.mouse_role = "select"
            if self.current_node and self.current_node.is_macro():
                self.notify("edit_node")

            # TODO: just show metadata on double click on another item

        if event.button == 1:
            # Left click
            if self.mouse_role == "select" and node:
                # got a node
                if handle != 0:
                    # we get a handle => resizing
                    self.mouse_role = "resizing"
                else:
                    self.mouse_role = "moving"
        elif event.button == 3:
            # Right click
            self.context_menu(event)

    def context_menu(self, event):
        """Menu appearing on right click"""
        menu = gtk.Menu()
        node = self.current_node
        transition = self.current_transition
        # Create menu-item copy for nodes only
        if not transition:
            class_name = node.__class__.__name__
            action = "Copy the current {}".format(
                "model" if class_name == "CTopNode" else class_name[1:]
            )

            menu_items = gtk.MenuItem(action)
            menu.append(menu_items)
            menu_items.connect("activate", self.menuitem_response, action, node)
            menu_items.show()
        # Create menu-item remove (do not remove top node)
        if transition or node != self.model.get_root():
            action = "Remove"
            menu_items = gtk.MenuItem(action)
            menu.append(menu_items)
            menu_items.connect(
                "activate", self.menuitem_response, action, transition or node
            )
            menu_items.show()
        # Create menu-item paste
        action = "Paste"
        menu_items = gtk.MenuItem(action)
        menu.append(menu_items)
        if self.clipboard.has_element():
            menu_items.connect("activate", self.menuitem_response, action, node)
        else:
            menu_items.set_sensitive(False)
        menu_items.show()
        # Create menu item paste component
        action = "Paste the model components"
        menu_items = gtk.MenuItem(action)
        menu.append(menu_items)
        if self.clipboard.has_macro():
            menu_items.connect("activate", self.menuitem_response, action, node)
        else:
            menu_items.set_sensitive(False)
        menu_items.show()

        menu.popup(None, None, None, 3, event.time)

    def menuitem_response(self, widget, action, item):
        """Callback for the context menu described in context_menu()

        :param action: Option selected
        :param item: Current selected node
        :param widget: Widget that emitted the event
        :type action: <str>
        :type item: <CTransition> or <CNode>
        """

        def update_nodes_model(sub_nodes):
            """
            - Set recursively the model for all the given nodes
            - Rename the nodes and make them as unique as possible
            - Update the transitions of the destination model
            - Update the nodes of the destination model

            .. TODO: Do not rename nodes/transitions if they are copied on a new model.
                Follow copy_number variable...
            """
            for sub_node in sub_nodes:
                if isinstance(sub_node, CMacroNode):
                    # MacroNode => recursive process
                    # LOGGER.debug("menuitem_response:: MacroNode here: %s", sub_node)
                    update_nodes_model(sub_node.sub_nodes)

                    # Update the transitions of the destination MODEL
                    # not the parent node himself, this will eventually be done later
                    node.model.transition_list += list(it.chain(*sub_node.transitions))

                assert sub_node.model is not None

                # LOGGER.debug("menuitem_response:: update model for %s", sub_node)
                sub_node.model = node.model

                ## New model ? do not rename...
                # Naming
                if sub_node.is_start() or sub_node.is_trap():
                    # Renumber start and trap nodes (add a number)
                    sub_node.name += str(node.start_trap_nodes_count)
                    node.start_trap_nodes_count += 1
                else:
                    # Rename all other nodes (names must be as unique as possible)
                    sub_node.name += "_" + str(copy_number)

                # Update model (do not ask me why this duplication of dict...)
                # simple_node_dict is for the GUI: list only CSimpleNodes
                # Start/Trap/Input/Perm/Macro/Top are only in node_dict
                if isinstance(sub_node, CSimpleNode) and not isinstance(
                    sub_node, CMacroNode
                ):
                    node.model.simple_node_dict[sub_node.name] = sub_node
                node.model.node_dict[sub_node.name] = sub_node

        def update_transitions(child_node):
            """
            Update the macro_node of the new transitions
            Update the transitions of the destination MODEL with the child_node ones
            Rename transitions
            Update names of nodes in conditions

            .. note:: This will also update child_node transitions (side effect)
            .. note:: Must be before new_transitions.update
                in order to avoid double counting of transitions
                (node.transitions already contains current model transitions
                and we don't want to modify them)
            """
            for transitions in child_node.transitions:
                # Model
                node.model.transition_list += transitions
                # MacroNode
                for transition in transitions:
                    transition.macro_node = node
                    # print("transition", transition)
                    # print("macro node", transition.macro_node)
                    # print("ori out:", transition.ori.outgoing_trans)
                    # print("ori in:", transition.ori.incoming_trans)
                    # print("event:", transition.event)
                    # print("influencing places:", transition.get_influencing_places())

                    # Rename nodes in the condition
                    # Ex: "A and not D) or (A or B) and (D and not A"
                    # Becomes: 'A and not D) or (A_1 or B) and (D and not A_1'
                    for place in transition.get_influencing_places():
                        transition.condition = re.sub(
                            r"([( ]|^)(%s)([) ]|$)" % place,
                            r"\g<1>%s\g<3>" % (place + "_" + str(copy_number)),
                            transition.condition
                        )

                    # Rename the transition
                    transition.event += "_" + str(copy_number)

            # Clean transitions duplicates added by update_nodes_model()
            node.model.transition_list = list(set(node.model.transition_list))


        if "Copy" in action:
            if not isinstance(item, CNode):
                return
            # Only for nodes
            child_node = item.copy()
            self.clipboard.put_node(child_node)

        elif action == "Remove":
            self.remove_node_or_transition(item)

        elif action == "Paste":
            if self.clipboard.has_element() and isinstance(item, CMacroNode):
                # Add a CMacroNode/CTopNode to the current model
                node = item
                child_node = self.clipboard.get_node()
                # Prepare naming of copied nodes
                copy_number = next(self.node_copy_count)

                # Update the parent and the model of child_node
                node.sub_nodes.append(child_node)
                child_node.father = node
                child_node.set_model(node.model)
                child_node.name += "_" + str(copy_number)

                # print("current child node model updated:", child_node.model)
                # print("current child node type:", type(child_node))

                if isinstance(child_node, CMacroNode):
                    # child_node is a complex node, we have to recursively
                    # update its content

                    # Update the model of the children of child_node (MacroNode)
                    update_nodes_model(child_node.sub_nodes)

                    # Update the macro_node of the new transitions
                    # Update the transitions of the destination MODEL
                    update_transitions(child_node)

                    # Add transitions to the current top/macro node ?
                    # => NO!! Transitions must remain in their complex node
                    # of belonging; nevertheless they are already referenced
                    # in the model thanks to update_transitions()

                # Coordinates in new node
                child_node.xloc = self.m_vscreen_coord[0]
                child_node.yloc = self.m_vscreen_coord[1]

                # Refresh ui
                node.model.modified = True
                node.model.notify()

        elif action == "Paste the model components":
            if self.clipboard.has_element() and isinstance(item, CMacroNode):
                # Add the content of a CMacroNode/CTopNode to the current model
                child_node = self.clipboard.get_node()

                if not isinstance(child_node, CMacroNode):
                    return

                node = item
                # Prepare naming of copied nodes
                copy_number = next(self.node_copy_count)

                # Add nodes to the current top/macro node
                # For direct chilren: Update their parent
                for snode in child_node.sub_nodes:
                    node.sub_nodes.append(snode)
                    snode.father = node

                # Update the model attr of the children of child_node
                # Note: Don't update the model of child_node, since it is
                # not used (we use only its children)
                update_nodes_model(child_node.sub_nodes)

                # Update the macro_node of the new transitions
                # Update the transitions of the destination MODEL
                update_transitions(child_node)

                # Add transitions to the current top/macro node
                # Note: Don't overwrite data of the current MacroNode => update
                # print("Transitions before:", node.new_transitions)
                node.new_transitions.update(child_node.new_transitions)
                # print("Transitions copied:", child_node.new_transitions)

                # Refresh ui
                node.model.modified = True
                node.model.notify()

    def remove_node_or_transition(self, item):
        """Remove the given transition or the given node

        Called by Charter object when Delete key is pressed, or when the Remove
        option is selected on the the context-menu hover an item on the DrawingArea.

        :param item:
        :type item: <CTransition> or <CNode> but not <CTopNode>
        """
        # Remove the item
        item.remove()

        if not isinstance(item, CNode):
            # Transition
            self.current_transition = None
            # TODO: Don't know why, but the deletion of transitions requires
            # a notification to the model (this is not the case for nodes)
            self.model.notify()

        # Reset selection
        self.current_node = None
        self.current_node_center = None
        # Current handle is now the TopNode
        self.current_handle = 0

        # Refresh ChartInfo in order to display actualized data about the model
        self.notify("current_change")

    def on_button_release(self, widget, event):
        """Callback when a mouse button is released on the DrawingArea
        (in the ChartView object)

        :param widget: gtk DrawingArea that emit the event
        :param event: gdk mouse event with attributes (x, y)
        :type widget: <NavView> or <ChartView>
        :type event: <gtk.gdk.Event>
        """
        # rubout last click characteristics
        if self.mouse_role == "select":
            return

        elif self.mouse_role == "resizing" or self.mouse_role == "moving":
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"

        elif self.mouse_role == "new_trans" and self.current_node:
            self.new_transition(event.x, event.y)

        elif self.current_node and self.current_node.is_macro():
            # assume node creation
            self.new_node(self.mouse_role)

    def new_node(self, node_type):
        """Creation of a new node

        Called during the :meth:`on_button_release` callback.

        @param node_type: type of the node (string)
        """
        xnode = self.m_vscreen_coord[0]
        ynode = self.m_vscreen_coord[1]
        if node_type == "simple":
            self.current_node = self.current_node.add_simple_node(
                next(self.gen_name), xnode, ynode
            )
        elif node_type == "macro":
            self.current_node = self.current_node.add_macro_subnode(
                next(self.gen_name), xnode, ynode, 0.25, 0.25
            )
        elif node_type == "start":
            self.current_node = self.current_node.add_start_node(xnode, ynode)
        elif node_type == "trap":
            self.current_node = self.current_node.add_trap_node(xnode, ynode)
        elif node_type == "perm":
            self.current_node = self.current_node.add_perm_node(
                next(self.gen_name), xnode, ynode
            )
        elif node_type == "input":
            self.current_node = self.current_node.add_input_node(
                next(self.gen_name), xnode, ynode
            )
        elif node_type == "env":
            self.current_node = self.current_node.add_env_node(
                next(self.gen_name), xnode, ynode, 0.25, 0.25
            )
        else:  # bug!
            raise TypeError("new_node: UNKNOWN TYPE: %s" % node_type)

        self.current_transition = None
        self.current_handle = 0
        self.m_vscreen_coord = (0.0, 0.0)
        self.notify("current_change")
        self.view.window.set_cursor(ChartControler.cursors[0])
        self.mouse_role = "select"

    def nodes_names_generator(self):
        """Return a generator of names for new nodes.

        Names are generated in lexicographic order and we try to avoid names
        that are already in the model (this is important in order to avoid
        overwriting of nodes).
        """
        for size in it.count(start=1):
            for tpl in it.combinations(ascii_uppercase, size):
                name = "".join(tpl)
                if name in self.model.node_dict:
                    continue
                yield name

    def new_transition(self, xmo, ymo):
        """Create a new transition

        Called during the :meth:`on_button_release` callback.

        @param xmo, ymo: int mouse screen coordinates
        """
        # are we in a node?
        xloc = xmo / self.view.draw_width
        yloc = ymo / self.view.draw_height
        #        w_coef = 1.0/self.view.draw_width
        #        h_coef = 1.0/self.view.draw_height
        (node, handle, center, trans) = self.model.find_element(
            (xloc, yloc), self.drawing_style
        )
        if not node:  # no extremity (never happens)
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"
            self.model.notify()  # rubout the draft transition
            return
        # are we in same container
        if self.current_node.father != node.father:
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"
            self.model.notify()  # rubout the draft transition
            return
        # we are in extremity node - current node is origin node
        # is origin node correct and extremity node correct
        if self.current_node.is_for_origin() and node.is_for_extremity():
            trans = self.current_node.father.add_transition(self.current_node, node)
            if trans:
                self.current_node.selected = False
                self.current_node = None
                self.m_vscreen_coord = (0.0, 0.0)
                self.current_transition = trans
                trans.selected = True
                self.notify("current_change")
                self.model.notify()
                self.view.window.set_cursor(ChartControler.cursors[0])
                self.mouse_role = "select"
            else:
                self.view.window.set_cursor(ChartControler.cursors[0])
                self.mouse_role = "select"
                self.model.notify()  # rubout the draft transition
        else:
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"
            if self.current_node:
                self.current_node.selected = False
            self.model.notify()  # rubout the draft transition
            return

    def on_motion_notify(self, widget, event):
        """Callback moving the cursor in the DrawingArea
        (in the ChartView object)

        :param widget: gtk DrawingArea that emit the event
        :param event: gdk mouse event with attributes (x, y)
        :type widget: <NavView> or <ChartView>
        :type event: <gtk.gdk.Event>
        """
        swi = self.view.draw_width
        she = self.view.draw_height

        # transform mouse coordinates to virtual screen 1.0 x 1.0
        xvirt = event.x / swi
        yvirt = event.y / she

        if self.mouse_role == "select":
            (node, handle, center, trans) = self.model.find_element(
                (xvirt, yvirt), self.drawing_style
            )
            if node == self.model.get_root():
                handle = 0
            # detect a new handle
            if handle != self.current_handle:
                self.current_handle = handle
                self.view.window.set_cursor(ChartControler.cursors[handle])

        elif self.mouse_role == "resizing":
            self.current_node.resize(
                xvirt, yvirt, self.current_handle, swi, she, self.model.get_root()
            )

        elif self.mouse_role == "moving":
            v_dx = xvirt - self.m_vscreen_coord[0]
            v_dy = yvirt - self.m_vscreen_coord[1]
            v_size = self.current_node.accept(self.drawing_style)
            self.current_node.move(v_dx, v_dy, v_size, self.model.get_root())
            self.m_vscreen_coord = (xvirt, yvirt)
        elif self.mouse_role == "new_trans":
            if self.current_node:
                self.draft_transition(event.x, event.y)

    def draft_transition(self, xmo, ymo):
        """
        draw a transition arrow in dotted line
        @param xmo,ymo: mouse coordinates
        """
        view = self.view
        self.model.notify()
        xr1 = int(self.current_node_center[0] * self.view.draw_width)
        yr1 = int(self.current_node_center[1] * self.view.draw_height)

        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_line_attributes(1, LINE_ON_OFF_DASH, 0, 0)
        # line
        pixmap.draw_line(grc, xr1, yr1, int(xmo), int(ymo))
        # arrow
        unx = xmo - xr1
        uny = ymo - yr1
        norm = sqrt(unx ** 2 + uny ** 2)
        if norm != 0:
            unx = unx / norm
            uny = uny / norm
            arr = Arrow()
            arr.draw(view, (unx, uny), (xmo, ymo))
        grc = view.window.new_gc()
        view.window.draw_drawable(
            grc, view.pixmap, 0, 0, 0, 0, view.draw_width, view.draw_height
        )

    ## API for communication with charter ######################################
    def set_action_select(self, widget):
        """
        As it says
        """
        self.mouse_role = "select"

    def set_action_new_simple_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "simple"

    def set_action_new_macro_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "macro"

    def set_action_new_start_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "start"

    def set_action_new_trap_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "trap"

    def set_action_new_input_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "input"

    def set_action_new_transition(self, widget):
        """
        As it says
        """
        if self.current_node:
            self.current_node.selected = False
        self.current_node = None
        self.current_handle = 0
        self.m_vscreen_coord = None
        if self.current_transition:
            self.current_transition.selected = False
        self.current_transition = None
        self.mouse_role = "new_trans"

    def set_action_new_perm_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "perm"


class NavControler(object):
    """Controler for navigation view (overview section in the GUI)
    Implement a controler for navigation views
    """

    def __init__(self):
        self.lastx = 0  # coordinates of last click in view
        self.lasty = 0
        self.in_ret = False
        self.obs = []

    def set_view(self, view):
        """
        As it says
        """
        # attribute view is assigned when a view is created
        self.view = view

    def attach(self, obs):
        """
        observer management
        """
        if not obs in self.obs:
            self.obs.append(obs)

    def detach(self, obs):
        """
        observer management
        """
        self.obs.remove(obs)

    def notify(self, depx, depy):
        """
        observer management
        """
        for obs in self.obs:
            obs.update(depx, depy)

    def on_button_press(self, widget, event):
        """
        action when a mouse button is pressed
        """
        self.lastx = event.x
        self.lasty = event.y
        cond = self.view.x_ret <= self.lastx
        cond = cond and (self.lastx <= (self.view.x_ret + self.view.w_ret))
        if cond:
            cond2 = self.view.y_ret <= self.lasty
            vvv = self.view.y_ret + self.view.h_ret
            cond2 = cond2 and (self.lasty <= vvv)
            if cond2:
                self.in_ret = True

    def on_button_release(self, widget, event):
        """
        action when a mouse button is released
        """
        self.in_ret = False

    def on_motion_notify(self, widget, event):
        """
        callback
        """
        if self.in_ret:
            depx = event.x - self.lastx
            depy = event.y - self.lasty
            alloc = widget.get_allocation()
            # limits
            vv1 = self.view.x_ret + depx + self.view.w_ret
            vv2 = self.view.x_ret + depx
            if (vv1 > alloc.width) or (vv2 < 0):
                depx = 0
            vv1 = self.view.y_ret + depy + self.view.h_ret
            vv2 = self.view.y_ret + depy
            if (vv1 > alloc.height) or (vv2 < 0):
                depy = 0
            self.lastx = self.lastx + depx
            self.lasty = self.lasty + depy
            # reticule move
            if (not depx == 0) or (not depy == 0):
                depx = float(depx) / alloc.width
                depy = float(depy) / alloc.height
                self.notify(depx, depy)
