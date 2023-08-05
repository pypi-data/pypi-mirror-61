## Filename    : layout
## Author(s)   : Michel Le Borgne
## Created     : 01/2012
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
##     IRISA/IRSET
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s):
##
"""
Layouts are performed by a visitor of the chart model
"""
import pygraphviz as pgv

import cadbiom.commons as cm

LOGGER = cm.logger()


class LayoutVisitor(object):
    """Visitor used to do a gt graph layout

    Available layouts::

        - dot - "hierarchical" or layered drawings of directed graphs.
        This is the default tool to use if edges have directionality.

        - neato - "spring model" layouts.
        This is the default tool to use if the graph is not too large
        (about 100 nodes) and you don't know anything else about it.
        Neato attempts to minimize a global energy function, which is equivalent
        to statistical multi-dimensional scaling.

        - fdp - "spring model" layouts similar to those of neato, but does
        this by reducing forces rather than working with energy.

        - sfdp - multiscale version of fdp for the layout of large graphs.

        - twopi - radial layouts, after Graham Wills 97.
        Nodes are placed on concentric circles depending their distance from a
        given root node.

        - circo - circular layout, after Six and Tollis 99, Kauffman and Wiese 02.
        This is suitable for certain diagrams of multiple cyclic structures,
        such as certain telecommunications networks.

    .. seealso:: https://www.graphviz.org/

    """

    def __init__(self, view, layout_style):
        self.view = view
        self.drawing_style = view.drawing_style
        self.layout = layout_style

    def visit_chart_model(self, model):
        """
         Not used
        """
        model.get_root().accept(self)

    def visit_cstart_node(self, node):
        """
         Not used
        """
        return

    def visit_ctrap_node(self, node):
        """
         Not used
        """
        return

    def visit_csimple_node(self, node):
        """
         Not used
        """
        return

    def visit_cinput_node(self, node):
        """
         Not used
        """
        return

    def visit_cperm_node(self, node):
        """
         Not used
        """
        return

    def visit_cmacro_node(self, node):
        """
        Layouts are done on each macro place
        Change the local coordinates of subnodes according to layout style
        """
        if node.sub_nodes == []:
            return
        agraph = pgv.AGraph(splines="ortho")
        node_dict = dict()
        # build nodes
        for snode in node.sub_nodes:
            agraph.add_node(snode.name)
            anode = agraph.get_node(snode.name)
            node_dict[snode.name] = snode
            if snode.is_macro() and snode.model.show_macro:
                anode.attr["width"] = "%s" % snode.wloc
                anode.attr["height"] = "%s" % snode.hloc
                snode.accept(self)
        # build edges
        for tgr in node.transitions:
            for trans in tgr:
                agraph.add_edge(trans.ori.name, trans.ext.name)
        # layout
        layout_style = self.layout
        if layout_style == "hierarchical_LR":
            agraph.layout(prog="dot", args="-Grankdir=LR")
        elif layout_style == "hierarchical_TB":
            agraph.layout(prog="dot", args="-Grankdir=BT")
        elif layout_style == "neato":
            agraph.layout(prog="neato")
        elif layout_style == "fdp":
            agraph.layout(prog="fdp")
        elif layout_style == "sfdp":
            agraph.layout(prog="sfdp")
        elif layout_style == "twopi":
            agraph.layout(prog="twopi")
        elif layout_style == "circo":
            agraph.layout(prog="circo")
        else:
            LOGGER.error(
                "LayoutVisitor::visit_cmacro_node: Unknow layout: %s", layout_style
            )
            exit(1)

        # change coordinates
        # bounding box for ratios
        bbox = pgv.graphviz.agget(agraph.handle, "bb")
        bbox = bbox.split(",")
        xmin = float(bbox[0])
        xmax = float(bbox[2])
        ymin = float(bbox[1])
        ymax = float(bbox[3])
        # adjust graphic window
        view = self.view
        cond = (xmax - xmin) / 3.0 > view.draw_width
        cond = cond or ((xmax - xmin) / 3.0 < view.draw_width / 2.0)
        if cond:
            view.draw_width = min(int((xmax - xmin) / 3.0), 10400)  # 31200 max
            view.draw_width = max(1300, view.draw_width)
            view.min_width = view.draw_width
        cond = ymax - ymin > view.draw_height
        cond = cond or ymax - ymin < view.draw_height / 2.0
        if cond:
            view.draw_height = min(int(ymax - ymin), 7200)  # 21600 max
            view.draw_height = max(900, view.draw_height)
            view.min_height = view.draw_height
        # reset zoom counter
        view.zoom_count = 0
        gwidth = 1.0
        gheight = 1.0  # virtual window for the macro node
        if xmin == xmax or ymin == ymax:
            LOGGER.error(
                "LayoutVisitor::visit_cmacro_node: Coordinates consistency: "
                "x:(%s vs %s); y:(%s vs %s)",
                xmin, xmax,
                ymin, ymax,
            )
            exit(1)

        x_ratio = gwidth / (xmax - xmin)
        y_ratio = gheight / (ymax - ymin)
        # changing coordinates
        for node in agraph.nodes():
            pos = node.attr["pos"].split(",")
            cnn = node_dict[node]
            xcoord = float(pos[0]) * x_ratio
            ycoord = float(pos[1]) * y_ratio
            cnn.set_layout_coordinates(xcoord, ycoord)

    def visit_ctop_node(self, node):
        """
        Same as macro node
        """
        self.visit_cmacro_node(node)
        return

    def visit_ctransition(self, trans):
        """
         Not used
        """
        return
