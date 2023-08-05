# -*- coding: utf-8 -*-
## Filename    : chart_model.py
## Author(s)   : Michel Le Borgne
## Created     : 4/3/2010
## Revision    :
## Source      :
##
## Copyright 2009 - 2010 : IRISA/IRSET
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
## Contributor(s): Nolwenn Le Meur, Geoffroy Andrieux
##
"""
Classes of nodes, transitions and model for representing a guarded transition model

Classes available and their inheritance relationships:

    - :class:`ChartModel`: Model of a chart
    - :class:`CTransition`
    - :class:`CNode`

      - :class:`CStartNode`

        - :class:`CTrapNode`

      - :class:`CSimpleNode`

        - :class:`CPermNode`
        - :class:`CInputNode`
        - :class:`CMacroNode`

          - :class:`CTopNode`
"""
from __future__ import unicode_literals
from __future__ import print_function
from math import sqrt
from collections import defaultdict
import itertools as it
from antlr3 import ANTLRStringStream, ANTLRFileStream, CommonTokenStream

from condexpLexer import condexpLexer
from condexpParser import condexpParser
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser

from cadbiom import commons as cm

# number of simple nodes before we draw macros as simple nodes
MAX_SIZE_MACRO = 50
MAX_SIZE = 4000  # max number of nodes we draw

LOGGER = cm.logger()


class ChartModelException(Exception):
    """
    Exception for chart models
    """

    def __init__(self, mess):
        self.message = mess


class ChartModel(object):
    """
    Model of a chart - implements the observer pattern as subject
    observers must have an update method

    Attributes::

        :param name: Name of the model
        :param xml_namespace: Version of cadbiom model

            Allowed values::

                - v1 (default): http://cadbiom.genouest.org/
                - v2: http://cadbiom.genouest.org/v2/

            Note: v2 models allow metadata in JSON format.

        :param simple_node_dict: For quick finding - name -> node.
            This is for the GUI: list **only** CSimpleNodes
        :param node_dict: For quick finding - name -> node.
            This is for internal use and this attribute can contain all types of
            nodes: Start/Trap/Input/Perm/Macro/Top/Simple nodes.
        :param transition_list: All the transitions in the model
        :param signal_transition_dict: For quick finding -
            simple node name -> list of influenced transitions.
            i.e: nodes that are in the condition of a transition only.
        :param __root: A virtual macronode on top of the hierarchy.
            This artificial CTopNode node groups all the hierarchy.

            .. seealso:: :meth:`CTopNode`
        :param constraints: biosignal clock constraints
        :param modified: Boolean to test if the model has been modified.
            Used to test if the model can be closed safely without loose of data.
        :param show_macro: Boolean used show/hide the MacroNodes if MAX_SIZE_MACRO
            (default: 50) is exceeded.
        :param max_size: Max number of nodes allowed to be drawn.
            default: MAX_SIZE=2000
        :param __observer_list: For observer pattern (?)
        :param marked_nodes: Set of marked (highlighted/selected) nodes in the
            graph editor
        :param marked_transitions: Set of marked (highlighted/selected) transitions
            in the graph editor
        :type name: <str>
        :type xml_namespace: <str>
        :type simple_node_dict: <dict <str>:<CSimpleNode>>
        :type node_dict: <dict <str>:<CNode>>
        :type transition_list: <list <CTransition>>
        :type signal_transition_dict: <dict <str>:<list <CTransition>>>
        :type __root: <CTopNode>
        :type constraints: <str>
        :type modified: <boolean>
        :type show_macro: <boolean>
        :type max_size: <int>
        :type __observer_list: <list <?>>
        :type marked_nodes: <set>
        :type marked_transitions: <set>
    """

    def __init__(self, name, xml_namespace="http://cadbiom.genouest.org/"):
        """
        :param name: Name of the model (ex: concat of graphs uris).
        :param xml_namespace: Global namespace: Model version.
            ex: http://cadbiom.genouest.org/ (v1),
            or http://cadbiom.genouest.org/v2/ (v2)
        """
        self.name = name
        self.xml_namespace = xml_namespace
        # For quick finding - name -> node
        # simple_node_dict is for the GUI: list only CSimpleNodes
        # Start/Trap/Input/Perm/Macro/Top are only in node_dict
        self.simple_node_dict = dict()
        self.node_dict = dict()
        # All the transitions in the model
        self.transition_list = []
        self.temp_transitions = set()
        # simple node name -> list of influenced transitions
        # i.e: nodes that are in the condition of a transition only
        self.signal_transition_dict = dict()
        # A virtual macronode on top of the hierarchy.
        # This artificial node groups all the hierarchy.
        self.__root = CTopNode(name, self)
        # string of biosignal clock constraints
        self.constraints = ""
        self.modified = False
        self.show_macro = True
        # default value for max number of nodes for drawing
        self.max_size = MAX_SIZE
        # for observer pattern
        self.__observer_list = []
        self.marked_nodes = set()
        self.marked_transitions = set()

    ## observer pattern methods ################################################
    def attach(self, obs):
        """
        observer pattern standard attach methods
        """
        if not obs in self.__observer_list:
            self.__observer_list.append(obs)

    def detach(self, obs):
        """
        observer pattern standard detach methods
        """
        self.__observer_list.remove(obs)

    def notify(self):
        """Observer pattern: standard notify methods

        Notify observers when the model have been changed (move/delete/add item)

        Observers are::

            - ChartView (GtkDrawingArea)
            - NavView (GtkDrawingArea)
            - SearchManager
            - SearchFrontier
        """
        [obs.update() for obs in self.__observer_list]

    def build_from_cadlang(self, file_name, reporter):
        """Build a model from a .cal file of PID database (Test purpose)

        Used only by :class:`library.cadbiom.models.clause_constraints.mcl.TestMCLAnalyser`

        @param file_name: str - path of .cal file
        """
        crep = reporter
        fstream = ANTLRFileStream(file_name)
        lexer = cadlangLexer(fstream)
        lexer.set_error_reporter(crep)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(crep)
        parser.cad_model(self)

    ## model methods ###########################################################
    def draw(self, view):
        """Redraw the model

        Asked from::

            - :class:`cadbiom_gui.gt_gui.chart_view.ChartView`:
            via its update() and on_expose_event() methods
            - :class:`cadbiom_gui.gt_gui.chart_view.NavView`: idem

        @param view: chart_view
        """
        # we don't update views which are not visible
        if not view.window:
            return

        nb_snodes = len(self.simple_node_dict)
        # if model size two large don't draw
        if nb_snodes > self.max_size:
            return

        # if model size too large, don't show macros
        if nb_snodes > MAX_SIZE_MACRO:
            self.show_macro = False
        self.__root.draw(view)

    def get_root(self):
        """
        @return: the root of the hierarchy
        """
        if self.__root.submodel:
            return self.__root.sub_nodes[0]
        else:
            return self.__root

    def find_element(self, m_v_c, dstyle):
        """
        @param m_v_c :coordinates of the mouse in virtual screen
        @param dstyle: drawing style (gives virtual size of fixed size nodes)

        Given the window mouse coordinates, return (node, handle, center)
        where node is the node the mouse is in,  handle the handle of the node
        the mouse is in and c are the coordinates of the node center in view.
        If no handle, handle = 0, handle are 1,2,3,4 clockwise numbered
        from upper left corner
        If no node found returns (None,0,(0,0))
        """
        return self.__root.find_element(m_v_c[0], m_v_c[1], dstyle)

    def make_submodel(self, mnode):
        """
        make a submodel from a macronode (no check) of another model
        """
        self.__root.sub_nodes = []
        self.__root.add_submodel(mnode)

    def is_submodel(self):
        """
        test if it is a submodel (for macro view)
        """
        return self.__root.submodel

    def clean(self):
        """
        Clean markers
        """
        self.__root.clean()

    def clean_code(self):
        """
        Clean code attribute
        """
        self.__root.clean_code()

    def accept(self, visitor):
        """
        Visitors entrance
        """
        return visitor.visit_chart_model(self)

    def get_simple_node_names(self):
        """Return list of the simple nodes in the model

        This function is called each time an update of SearchManager and
        SearchFrontier is required by the user; or by ToggleWholeModel

        .. seealso::

            - :meth:`cadbiom_gui.gt_gui.chart_misc_widgets.SearchManager.display_nodes`
            - :meth:`cadbiom_gui.gt_gui.chart_simulator.chart_simul_controler.ToggleWholeModel`

        .. note:: The signal_transition_dict is refreshed here on condition
            that the transitions of the model have changed.

            The boolean self.modified can't be tested here because it can be True
            only because moved nodes.
        """
        # Refresh transition dictionary
        # Optimization if the model is not modified
        transitions = set(self.transition_list)
        if self.temp_transitions != transitions or not self.signal_transition_dict:
            LOGGER.debug("ChartModel: Rebuild the signal_transition_dict")

            self.signal_transition_dict = defaultdict(list)
            [
                self.signal_transition_dict[place].append(trans)
                for trans in self.transition_list
                for place in trans.get_influencing_places()
            ]
            # Security cast
            self.signal_transition_dict = dict(self.signal_transition_dict)
            self.temp_transitions = transitions

        return self.simple_node_dict.keys()

    def get_matching_node_names(self, regex_obj):
        """Return node names that contain the given regular expression

        :param regex_obj: Compiled regular expression
        :type regex_obj: <_sre.SRE_Pattern>
        """
        return [name for name in self.simple_node_dict.keys() if regex_obj.search(name)]

    def unset_search_mark(self):
        """Notify observers after unmarking nodes and transitions with conditions

        Note: mark status of nodes implies their coloring in the graph editor.
        """
        self.unmark_nodes_and_transitions()
        self.notify()

    def set_search_mark(self, node_names):
        """Notify observers after marking nodes and transitions related to the
        given nodes names

        Note: mark status of nodes implies their coloring in the graph editor.

        :param node_names: List of names
        :type node_names: <list <str>>>
        """
        # Unmark
        self.unmark_nodes_and_transitions()

        # Mark
        for name in node_names:
            node = self.simple_node_dict.get(name, None)
            if node is None:
                # do not mark transition if node doesnt exist (unlikely)
                return
            node.search_mark = True
            self.marked_nodes.add(node)

            for transition in self.signal_transition_dict.get(name, []):
                transition.search_mark = True
                self.marked_transitions.add(transition)

        self.notify()

    def unmark_nodes_and_transitions(self):
        """Handy function to unmark simple nodes and transitions with conditions

        Note: mark status of nodes implies their coloring in the graph editor.

        Called by: :meth:`search_mark`, :meth:`unmark_nodes_and_transitions`

        .. TODO: Sync marked_nodes and marked_transitions in case of deletion.
            => not urgent, the set is reset at the end of this function
        """
        # Unmark simple nodes
        for node in self.marked_nodes:
            node.search_mark = False

        # Unmark transitions with conditions
        for transition in self.marked_transitions:
            transition.search_mark = False

        self.marked_nodes = set()
        self.marked_transitions = set()

    def get_simple_node(self, name):
        """
        :param name: string - name of the node
        :return: a simple node with given name
        """
        return self.simple_node_dict[name]

    def get_node(self, name):
        """
        :param name: string - name of the node
        :return: a node
        """
        return self.node_dict[name]

    def get_influenced_transition(self, node_name):
        """
        :param node_name: Name of a node
        :return: The transitions influenced by the node i.e. when
            the node name appears in the condition
        """
        return self.signal_transition_dict.get(node_name, [])

    ## method for model transformations ########################################
    def mark_as_frontier(self, node_name):
        """Given the name of a simple node, add a start node and a transition
        from the start node to the simple node

        .. warning:: notify observers

        :param node_name: Name of a node
        """
        try:
            snode = self.simple_node_dict[node_name]
            macro = snode.father
            start = macro.add_start_node(0, 0)
            macro.add_transition(start, snode)
        except KeyError:
            raise ChartModelException("Unknown simple node: " + node_name)
        self.notify()

    def __turn_into_other(self, node_name, ntype):
        """
        @param node_name: string
        @param ntype: node type - string
        turn a simple name into a permanent or input node
        The simple name must not have entering transitions
        @warning: notify observer
        """
        try:
            snode = self.simple_node_dict[node_name]
        except KeyError:
            raise ChartModelException("Unknown simple node: " + node_name)
        if len(snode.incoming_trans) != 0:
            raise ChartModelException("Incoming transition on node: " + node_name)
        macro = snode.father
        if ntype == "perm":
            pnode = macro.add_perm_node(node_name, snode.xloc, snode.yloc)
        else:
            pnode = macro.add_input_node(node_name, snode.xloc, snode.yloc)
        for trans in snode.outgoing_tran:
            macro.add_transition(pnode, trans.ext)
        snode.remove()
        self.notify()

    def turn_into_input(self, node_name):
        """
        Turn a simple node into an input node
        """
        self.__turn_into_other(node_name, "input")

    def turn_into_perm(self, node_name):
        """
        Turn a simple node into a perm node
        """
        self.__turn_into_other(node_name, "perm")

    def __repr__(self):
        return "<ChartModel {}>".format(self.name)


class CNode(object):
    """Abstract node class for guarded transition models
    Base class for model components

    :param father: Parent node. All nodes are aware of their parent node.
        Most of the time it is the CTopNode; but this can differ for nodes
        in CMacroNodes. Such "Complex" nodes can be used to build a linked list
        of nodes since they also contain a list of subnodes.
    :param search_mark: This flag is used to change the color of selected nodes
        with a search from the list of simple/frontier nodes or from search entry
        of the GUI.
        .. seealso:: :meth:`~cadbiom_gui.gt_gui.graphics.drawing_style`
    :param selected: This flag is used to change the color of mouse selected nodes
        .. seealso:: :meth:`~cadbiom_gui.gt_gui.graphics.drawing_style`
    """

    wmin = 0.1
    hmin = 0.1
    depth_max = 3

    def __init__(self, x_coord, y_coord, model, note=""):
        """
        The coordinates of a node are always in the space of its father.
        """
        self.model = model
        self.name = "$$"
        self.note = note
        self.xloc = x_coord
        self.yloc = y_coord
        self.father = None
        self.selected = False
        self.search_mark = False
        self.incoming_trans = []
        self.outgoing_trans = []

    def is_top_node(self):
        """
        As it says
        """
        return False

    def is_macro(self):
        """
        As it says
        """
        return False

    def is_start(self):
        """
        As it says
        """
        return False

    def is_input(self):
        """
        As it says
        """
        return False

    def is_perm(self):
        """
        As it says
        """
        return False

    def is_trap(self):
        """
        As it says
        """
        return False

    def is_simple(self):
        """
        As it says
        """
        return False

    def set_model(self, model):
        """
        As it says
        """
        self.model = model

    def set_name(self, name):
        """
        As it says
        """
        self.name = name

#    def set_coordinates(self, x, y):
#        """
#        As it says
#        """
#        self.xloc = x
#        self.yloc = y
#        self.model.notify()

    def get_coordinates(self):
        """
        As it says
        """
        return (self.xloc, self.yloc)

    def set_layout_coordinates(self, x_coord, y_coord):
        """
        As it says
        """
        self.xloc = x_coord
        self.yloc = y_coord

    def find_element(self, mox, moy, dstyle):
        """
        The mouse coordinates must be in the same frame than nodes coordinates
        """
        pass

    def remove(self):
        """Remove this node from:
            - its model
            - its father's transitions

        .. warning:: assume it is not a TopNode nor a MacroNode
        """
        if not self.father:
            return

        LOGGER.debug("%s::remove: %s", self.__class__.__name__, self)
        # Remove transitions using the current node
        # Get the parent node:
        # i.e a CTopNode (which contain all the hierarchy of nodes),
        # or a MacroNode
        father = self.father
        temp_transitions = defaultdict(list, father.new_transitions)
        for nodes, transitions in father.new_transitions.items():
            # print("search node:", self.name, "in nodes couple:", nodes)
            # Search current name in nodes
            if self in nodes:
                # Remove related transitions from the node and delete these
                # transitions from the model
                for transition in temp_transitions.pop(nodes):
                    # print("transition to be removed:", transition)
                    transition.remove()

        # Update transitions of father
        father.new_transitions = temp_transitions
        # Remove the node in the father
        father.sub_nodes.remove(self)
        # Remove the references of the node
        # (with error masking because some nodes are not in the 2 dicts.
        # Only SimpleNodes are in both)
        self.model.simple_node_dict.pop(self.name, None)
        self.model.node_dict.pop(self.name, None)

        # Refresh the view
        self.model.modified = True
        self.model.notify()

    def clean(self):
        """
        Abstract
        """
        pass

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)


class CStartNode(CNode):
    """
    Start node show macro-states initialisation
    """

    def __init__(self, x_coord, y_coord, model, **kwargs):
        CNode.__init__(self, x_coord, y_coord, model, **kwargs)
        self.name = "__start__"

    def copy(self, model=None):
        """
        As says
        """
        if not model:
            model = self.model
        return CStartNode(self.xloc, self.yloc, model, note=self.note)

    def is_start(self):
        """
        As says
        """
        return True

    def is_for_origin(self):
        """
        As says
        """
        return True

    def is_for_extremity(self):
        """
        As says
        """
        return False

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        @param dstyle: drawing style (not used here)
        @param w_ratio,h_ratio: affinity ratios for virtual screen (not used here)

        Returns center coordinate in surrounding node - here node coordinates
        """
        return (self.xloc, self.yloc)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        """
        # graphic style
        view.drawing_style.draw_start(self, xfr, yfr, wfr, hfr)

    def find_element(self, mox, moy, dstyle, w_coef, h_coef):
        """
        No handle
        """
        # bounding box in father's frame
        v_bb_size = self.accept(dstyle)
        snw = v_bb_size[0] * w_coef
        snh = v_bb_size[1] * h_coef
        hdec = v_bb_size[2] * h_coef

        # center coordinates in father's frame
        ccx = self.xloc
        ccy = self.yloc + hdec
        in_node = (mox >= ccx - snw) and (mox <= ccx + snw)
        in_node = in_node and (moy >= ccy - snh) and (moy <= ccy + snh)
        if in_node:
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def move(self, v_dx, v_dy, dstyle, top_node):
        """
        Move the node - mx_virt, my virt coordinates of the mouse in virtual screen frame
        click_loc is the location of the clic in node's frame
        """

        # move in reference frame (father's)
        (acx, acy) = self.father.v_affinity_coef(top_node)
        loc_dx = acx * v_dx
        loc_dy = acy * v_dy
        # translation vector in own's frame -> father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy

        # TODO compute limits
        delta = 0.0
        if (new_xloc >= 0) and (new_xloc < 1.0):
            self.xloc = new_xloc
        if (new_yloc > delta) and (new_yloc < 1.0):
            self.yloc = new_yloc
        self.model.modified = True
        self.model.notify()

    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        @param dstyle: drawing style
        @param w_ratio, h_ratio: affinity ratios virtual -> local frame
        """
        (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
        # local axes size (ellipse because of affinities)
        v_size = self.accept(dstyle)
        rlocx = v_size[0] / w_ratio
        rlocy = v_size[1] / h_ratio
        uux = xc2 - self.xloc
        uuy = yc2 - self.yloc
        norm = sqrt(uux ** 2 + uuy ** 2)
        if norm != 0:
            uux = uux / norm
            uuy = uuy / norm
        isx = self.xloc + uux * rlocx
        isy = self.yloc + uuy * rlocy
        return (isx, isy, 0.0, 1)

    def clean(self):
        pass

    def accept(self, visitor):
        """
        Generic visitor acceptor
        """
        return visitor.visit_cstart_node(self)


class CTrapNode(CStartNode):
    """
    Dead end node
    """

    def __init__(self, xcoord, ycoord, model, **kwargs):
        CStartNode.__init__(self, xcoord, ycoord, model, **kwargs)
        self.name = "__trap__"

    def is_trap(self):
        return True

    def is_start(self):
        return False

    def copy(self, model=None):
        if not model:
            model = self.model
        return CTrapNode(self.xloc, self.yloc, model, note=self.note)

    def is_for_origin(self):
        return False

    def is_for_extremity(self):
        return True

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        """
        # graphic context
        view.drawing_style.draw_trap(self, xfr, yfr, wfr, hfr)

    def accept(self, visitor):
        """
        Standard acceptor
        """
        return visitor.visit_ctrap_node(self)


class CSimpleNode(CNode):
    """
    A simple node cannot have sub nodes
    Simple nodes have constant screen dimensions
    """

    def __init__(self, xcoord, ycoord, name, model, **kwargs):
        CNode.__init__(self, xcoord, ycoord, model, **kwargs)
        self.name = name
        self.father = None  # double linkage for coordinate computations
        self.activated = False
        self.was_activated = False

    def copy(self, model=None):
        """
        As says
        """
        if not model:
            model = self.model
        return CSimpleNode(self.xloc, self.yloc, self.name, model, note=self.note)

    def is_simple(self):
        return True

    def is_for_origin(self):
        """
        Can be used as transition origin
        """
        return True

    def is_for_extremity(self):
        """
        Can be used as transition extremity
        """
        return True

    def set_name(self, name):
        """Rename the current node; update simple_node_dict attr of the model"""
        try:
            del self.model.simple_node_dict[self.name]
        except:
            pass
        self.name = name
        self.model.simple_node_dict[name] = self

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        Returns center coordinate in surrounding node
        """
        v_size = self.accept(dstyle)
        xco = self.xloc + (v_size[0] / w_ratio) / 2.0
        yco = self.yloc + (v_size[1] / h_ratio) / 2.0
        return (xco, yco)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        @param xfr: x coordinate of father in view screen
        @param yfr: y coordinate of father in view screen
        @param wfr: width of father in virtual screen
        @param hfr: height of father in virtual screen
        """
        view.drawing_style.draw_simple(self, xfr, yfr, wfr, hfr)

    def find_element(self, mox, moy, dstyle, w_coef, h_coef):
        """
        Simple node - No handle
        """
        # size of the node in father's frame
        v_bb = self.accept(dstyle)
        snw = v_bb[0] * w_coef
        snh = v_bb[1] * h_coef

        # center coordinates in father's frame
        ccx = self.xloc + 0.5 * snw
        ccy = self.yloc + 0.5 * snh
        in_node = (mox >= self.xloc) and (mox <= self.xloc + snw)
        in_node = in_node and (moy >= self.yloc) and (moy <= self.yloc + snh)
        if in_node:
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def move(self, v_dx, v_dy, v_size, top_node):
        """
        Move the node - mx_virt, my virt are virtual coordinates of the mouse
        click_loc is the location of the clic in node's frame
        """
        # move in reference frame (father's)
        (ccx, ccy) = self.father.v_affinity_coef(top_node)
        loc_dx = ccx * v_dx
        loc_dy = ccy * v_dy
        # translation vector in reference frame i.e. father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy

        # check limits
        wloc = v_size[0] * ccx
        hloc = v_size[1] * ccy
        delta = v_size[2] * ccy

        move = False
        if (new_xloc >= 0) and (new_xloc + wloc < 1.0):
            self.xloc = new_xloc
            move = True
        if (new_yloc > delta) and (new_yloc + hloc < 1.0):
            self.yloc = new_yloc
            move = True
        if move:
            self.model.modified = True
            self.model.notify()

    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        Gives the the first point where to branch a transition, the gap between two arrows
        and a boolean horizontal true if arrows start from horizontal edge
        Assume wloc and hloc computed (node drawn) - coordinates in container frame

        @param node2: second node of the transition
        @param dstyle: drawing style
        @param nb_trans: number of transitions to be drawn
        @param w_ratio, h_ratio: dimentions of the screen for fixed size nodes
        """
        return intersect_simple(self, node2, dstyle, nb_trans, w_ratio, h_ratio)

    def clean(self):
        self.activated = False
        self.was_activated = False

    def accept(self, visitor):
        """
        standard visitor acceptor
        """
        return visitor.visit_csimple_node(self)


class CPermNode(CSimpleNode):
    """
    permanent node are never unactivated
    """

    def __init__(self, xcoord, ycoord, name, model, **kwargs):
        CSimpleNode.__init__(self, xcoord, ycoord, name, model, **kwargs)

    def copy(self, model=None):
        if not model:
            model = self.model
        return CPermNode(self.xloc, self.yloc, self.name, model, note=self.note)

    def is_perm(self):
        return True

    def is_simple(self):
        return False

    def is_for_extremity(self):
        return False

    def accept(self, visitor):
        return visitor.visit_cperm_node(self)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        @param xfr, yfr: coordinates of father node (reference frame) in view
        @param wfr,hfr: width and height of father node in view (affinity ratios)
        """
        view.drawing_style.draw_perm(self, xfr, yfr, wfr, hfr)


class CInputNode(CSimpleNode):
    """
    An input node cannot have an in-transition
    """

    def __init__(self, xcoord, ycoord, name, model, **kwargs):
        CSimpleNode.__init__(self, xcoord, ycoord, name, model, **kwargs)
        self.father = None  # double linkage for coordinate computations
        self.activated = False

    def is_input(self):
        return True

    def is_simple(self):
        return False

    def copy(self, model=None):
        if not model:
            model = self.model
        return CInputNode(self.xloc, self.yloc, self.name, model, note=self.note)

    def is_for_extremity(self):
        return False

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        Returns center coordinate in surrounding node
        """
        return (self.xloc, self.yloc)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        special drawing for diamond
        """
        view.drawing_style.draw_input(self, xfr, yfr, wfr, hfr)

    def find_element(self, mox, moy, dstyle, w_coef, h_coef):
        """
        Simple node - No handle
        """
        # size of the box in father's frame
        v_bb = self.accept(dstyle)
        snw = v_bb[0] * w_coef
        snh = v_bb[1] * h_coef

        # center coordinates in father frame
        ccx = self.xloc + 0.5 * snw
        ccy = self.yloc + 0.5 * snh

        # mouse coordinates in self frame
        # mxl = (mox - self.xloc) / snw
        # myl = (moy - self.yloc) / snh
        # test
        in_node = (mox >= self.xloc) and (mox <= self.xloc + snw)
        in_node = in_node and (moy >= self.yloc) and (moy <= self.yloc + snh)

        if in_node:
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def move(self, v_dx, v_dy, v_size, top_node):
        """
        Move the node - mx_virt, my virt are virtual coordinates of the mouse
        click_loc is the location of the clic in node's frame
        """
        # move in reference frame (father's)
        (ccx, ccy) = self.father.v_affinity_coef(top_node)
        loc_dx = ccx * v_dx
        loc_dy = ccy * v_dy
        # translation vector in reference frame i.e. father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy
        # check limits
        wloc = (v_size[0] * ccx) / 2.0
        hloc = (v_size[1] * ccy) / 2.0
        hlabel = v_size[2] * ccy

        move = False
        if (new_xloc >= wloc) and (new_xloc + wloc < 1.0):
            self.xloc = new_xloc
            move = True
        if (new_yloc - hloc > hlabel) and (new_yloc + hloc < 1.0):
            self.yloc = new_yloc
            move = True
        if move:
            self.model.modified = True
            self.model.notify()

    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        An input node can be the origin of some transition to a node.
        One transition by node.
        """
        # local coordinates of node2 center
        (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
        # simple nodes have constant screen dimensions - convert to local ones
        v_size = self.accept(dstyle)
        wloc = (v_size[0] / w_ratio) / 2.0
        hloc = (v_size[1] / h_ratio) / 2.0
        # coordinates of a diamond are center coordinates
        uux = xc2 - self.xloc
        uuy = yc2 - self.yloc
        if uux != 0.0:
            slope = uuy / uux
            if slope < -1:
                if uux < 0.0:
                    return (self.xloc, self.yloc + hloc, 0, True)  # upper corner
                else:
                    return (self.xloc, self.yloc - hloc, 0, True)  # low corner
            elif slope >= -1 and slope <= 1:
                if uux < 0.0:
                    return (self.xloc - wloc, self.yloc, 0, True)  # left corner
                else:
                    return (self.xloc + wloc, self.yloc, 0, True)  # right corner
            else:
                if uux < 0.0:
                    return (self.xloc, self.yloc - hloc, 0, True)  # low corner
                else:
                    return (self.xloc, self.yloc + hloc, 0, True)  # upper corner
        else:
            if uuy >= 0:
                return (self.xloc, self.yloc + hloc, 0, True)  # upper corner
            else:
                return (self.xloc, self.yloc - hloc, 0, True)  # low corner

    def accept(self, visitor):
        return visitor.visit_cinput_node(self)


class CMacroNode(CSimpleNode):
    """Main building block for charts

    Quick note::
        new_transitions attribute is a defaultdict(list) which allow to get
        all transitions related to a couple of nodes.
        In theory there is only 1 transition for each couple of nodes
        (cf. :meth:add_transition).

        transitions attribute is a binding over values of new_transitions
        (so it is read-only!).

        So, every CMacroNode and CTopNode contain all transitions involving nodes
        that they contain.
    """

    def __init__(self, xcoord, ycoord, width, height, name, model, **kwargs):
        CSimpleNode.__init__(self, xcoord, ycoord, name, model, **kwargs)
        self.start_trap_nodes_count = 0  # for start and trap nodes naming
        self.wloc = width
        self.hloc = height
        self.sub_nodes = []
        # list<list<CTransitions>> Sublists: transitions with common extremities
        # self.transitions = []
        # See the property 'transitions' to find a wrapper for old code
        # Key: {<CNode>, <CNode>}; values: [<CTransition>, ...]
        # Ex: defaultdict(<type 'list'>, {frozenset(['A', 'D']): [D -> A, C:, E:],
        self.new_transitions = defaultdict(list)

    @property
    def transitions(self):
        """Compatibility code

        .. note:: The old API uses this attribute as a list<list<CTransitions>>.
            Sublists are transitions with common extremities.

        :return: An iterator over the values of self.new_transitions.
            Similar to: <list <list <CTransitions>>>
        :rtype: <dictionary-valueiterator>
        """
        return self.new_transitions.itervalues()

    @transitions.setter
    def transitions(self, _):
        """Block further modifications of the old attribute transitions
        .. note:: Please modify self.new_transitions instead.
        """
        raise Exception("NOT AUTHORIZED! Please modify new_transitions instead")

    def _find_in_subnodes(self, node):
        """Find a node in the list of sub nodes

        .. warning:: assume two nodes have different coordinates

        @param node: node to be found
        """
        for snode in self.sub_nodes:
            if snode.xloc == node.xloc and snode.yloc == node.yloc:
                return snode
        return None

    def copy(self, model=None):
        """
        Duplicate a macronode - performs a deep copy
        """
        LOGGER.debug("CMacroNode::copy")
        if not model:
            model = self.model
        child_node = CMacroNode(
            self.xloc, self.yloc, self.wloc, self.hloc, self.name, model, note=self.note
        )
        # copy subnodes
        self.copy_subnodes(child_node, model)
        # copy transitions
        self.copy_transitions(child_node)
        return child_node

    def copy_subnodes(self, child_node, model=None):
        """Copy current subnodes to the child node"""
        model = self.model if not model else model
        for snode in self.sub_nodes:
            snc = snode.copy(model)
            child_node.sub_nodes.append(snc)
            snc.father = child_node

            # Note: The model is not updated with this new node
            # because it can be pasted to another model and we don't know
            # which one here.

    def copy_transitions(self, child_node):
        """Copy current transitions to the child node

        TODO: méthode alternative de copie d'un noeud complexe:
        itérer sur les transitions du noeud courant
        et créer les subnodes du child_node en conséquence
        => pas de création des subnodes en amont
        => pas besoin de rechercher les nodes d'après leurs coordonnées
        avec _find_in_subnodes (méthode hasardeuse en cas de nombreux noeuds
        empilés les uns sur les autres => la méthode a du mal à retrouver le bon
        noeud et peut créer des transitions incorrectes)
        """

        LOGGER.warning(
            "CMacroNode: Read copy_transitions alert; "
            "the use of _find_in_subnodes is dangerous (see doc)"
        )
        for nodes, transitions in self.new_transitions.items():
            transitions_group = []
            for trans in transitions:
                # Get duplicated nodes
                origin = trans.ori
                origin_c = child_node._find_in_subnodes(origin)
                # print("origin", origin, id(origin), "vs origin_c", origin_c, id(origin_c))
                extremity = trans.ext
                extremity_c = child_node._find_in_subnodes(extremity)

                # New transition
                transition_c = CTransition(origin_c, extremity_c)
                transition_c.macro_node = child_node
                transition_c.event = trans.event
                transition_c.condition = trans.condition
                transition_c.action = trans.action
                transition_c.note = str(trans.note)
                transitions_group.append(transition_c)

                # Append new transition to the concerned ori and ext nodes
                origin_c.outgoing_trans.append(transition_c)
                extremity_c.incoming_trans.append(transition_c)

                # Note: The model is not updated with this new transition
                # because it can be pasted to another model and we don't know
                # which one here.

            # Set transitions of this macro node (new_transitions is empty here)
            child_node.new_transitions[frozenset([origin_c, extremity_c])] = transitions_group

    def remove(self):
        """Remove this node and its sub-nodes from the model"""

        LOGGER.debug("MacroNode cleaning", len(self.sub_nodes), self.sub_nodes)

        # Remove sub-nodes
        # Explicit copy because sub_nodes is modified by remove()
        for sub_node in list(self.sub_nodes):
            LOGGER.debug("%s have to be deleted", sub_node)
            sub_node.remove()

        assert not self.sub_nodes

        # Now, remove this node
        super(self.__class__, self).remove()

    def set_model(self, model):
        """
        Set the model for a subtree of nodes - used for copy/paste from one model to another
        """
        for snode in self.sub_nodes:
            snode.set_model(model)
        self.model = model
        self.model.modified = True

    def set_name(self, name):
        self.name = name

    def is_macro(self):
        return True

    def is_simple(self):
        return False

    def is_for_origin(self):
        """
        Legitimate transition origin
        """
        return True

    def is_for_extremity(self):
        """
        Legitimate transition extremity
        """
        return True

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        Returns center coordinate in surrounding node (father)
        """
        if self.model.show_macro:
            xcc = self.xloc + self.wloc / 2.0
            ycc = self.yloc + self.hloc / 2.0
        else:
            v_size = self.accept(dstyle)
            xcc = self.xloc + (v_size[0] / w_ratio) / 2.0
            ycc = self.yloc + (v_size[1] / h_ratio) / 2.0
        return (xcc, ycc)

    def virt_to_self_frame(self, xcoord, ycoord, s_width, s_height, top_node):
        """
        xcoord,ycoord must be virtual coordinates
        result is the coordinates of (x,y) in self frame
        @param xcoord, ycoord: coordinate in virtual window (screen -> 1.0 x 1.0 window)
        @param s_width, s_height: screen dimensions
        @param  top_node: root of the sub_model
        """

        if self != top_node:
            (xfath, yfath) = self.father.virt_to_self_frame(
                xcoord, ycoord, s_width, s_height, top_node
            )
            xloc = (xfath - self.xloc) / self.wloc
            yloc = (yfath - self.yloc) / self.hloc
            return (xloc, yloc)
        else:  # top node
            return (xcoord, ycoord)

    def self_to_virtual_frame(self, xcoord, ycoord, top_node):
        """
        Coordinate change
        """
        if self != top_node:
            xfath = self.xloc + xcoord * self.wloc
            yfath = self.yloc + ycoord * self.hloc
            return self.father.self_to_virtual_frame(xfath, yfath, top_node)
        else:
            return (xcoord, ycoord)

    def v_affinity_coef(self, top_node):
        """
        Affinity ratios cw,ch: local_horizontal_length = screen_horizontal_length * cw
        Similar relation for vertical length.
        @param  top_node: root of the sub_model
        """
        if self != top_node:
            (acw, ach) = self.father.v_affinity_coef(top_node)
            return (acw / self.wloc, ach / self.hloc)
        else:
            return (1.0, 1.0)

    def add_macro_subnode(self, name, xcoord, ycoord, width, height):
        """
        Add a macro node as subnode with dimensions
        """
        node = CMacroNode(xcoord, ycoord, width, height, name, self.model)
        # Not CSimpleNode; thus the node is not added to simple_node_dict
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.modified = True
        self.model.notify()
        return node

    def add_simple_node(self, name, xcoord, ycoord):
        """
        Add a simple node
        """
        node = CSimpleNode(xcoord, ycoord, name, self.model)
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.simple_node_dict[name] = node
        self.model.modified = True
        self.model.notify()
        return node

    def add_input_node(self, name, xcoord, ycoord):
        """
        Add input node
        """
        node = CInputNode(xcoord, ycoord, name, self.model)
        # Not CSimpleNode; thus the node is not added to simple_node_dict
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.modified = True
        self.model.notify()
        return node

    def add_copy(self, node):
        """
        add a node of the same type
        """
        nnode = node.copy(self.model)
        nnode.note = str(node.note)
        self.model.node_dict[nnode.name] = nnode
        nnode.father = self
        if nnode.is_simple():
            self.model.simple_node_dict[nnode.name] = nnode
        self.sub_nodes.append(nnode)
        self.model.modified = True
        self.model.notify()
        return nnode

    def add_transition(self, ori, ext):
        """Add a transition to the model

        .. note:: Reflexive transitions are not authorized.
            Duplications of transitions are not authorized.
            BUT! Not exception is raised in these cases. Have fun <3

        :param ori: a simple node
        :param ext: a simple node
        :return: A new transition or None if the couple of nodes was not valid.
        :rtype: <CTransition> or None
        """
        # transition between a node and itself are forbidden
        if ori == ext:
            LOGGER.warning(
                "Reflexive transition: %s -> %s "
                " - This transition will not be taken into account.\n"
                "Please review your model or use a PermanentNode instead.",
                ori.name,
                ext.name
            )
            return

        # Search the current couple of nodes in all the transitions
        # self.new_transitions is a defaultdict with frozensets as keys
        # and lists as values. Each value has at most 2 transitions
        # (one in each direction). Each value is called "transitions group"
        # later in the code.
        nodes_couple = frozenset((ori, ext))
        transitions_group = self.new_transitions[nodes_couple]
        if len(transitions_group) == 0:
            # New transition: the couple was not found before
            return self.build_new_transition_to_nodes(transitions_group, ori, ext)
        elif len(transitions_group) == 1:
            # Duplication of a transition ?
            trans = transitions_group[0]
            if not ((trans.ori == ori) and (trans.ext == ext)):
                # Incomplete transition: add the other one
                return self.build_new_transition_to_nodes(transitions_group, ori, ext)
            else:
                LOGGER.warning(
                    "Duplicated transition: %s -> %s\n"
                    "You should review your model. Only the first transition "
                    "will be taken into account.",
                    ori.name,
                    ext.name
                )
                return
        else:
            LOGGER.error("More than one transition for a couple of nodes")
            LOGGER.error("Current transition: %s -> %s", ori.name, ext.name)
            raise Exception("ERROR: More than one transition for a couple of nodes")

        LOGGER.error("Hi! You should never have reached this part.")
        LOGGER.error("Current transition: %s -> %s", ori.name, ext.name)
        raise Exception("Hi! You should never have reached this part.")

    def build_new_transition_to_nodes(self, transitions_group, ori, ext):
        """Handle a new transition: build and attach it to the model

        :param arg1: List of transitions that concern the given couple of nodes
            The list should not exceed 2 elements (see add_transition())
        :param arg2: Node
        :param arg3: Node
        :type arg1: <list <CTransition>>
        :type arg2: <Node>
        :type arg3: <Node>
        """
        # Build new transition
        new_transition = CTransition(ori, ext)
        new_transition.macro_node = self
        # Append the new transition to the internal structure that groups
        # couple of transitions with same nodes
        transitions_group.append(new_transition)
        # Append new transition to the concerned ori and ext nodes
        new_transition.ori.outgoing_trans.append(new_transition)
        new_transition.ext.incoming_trans.append(new_transition)
        # Append new transition to the model
        self.model.transition_list.append(new_transition)
        self.model.modified = True
        self.model.notify()
        return new_transition

    def add_start_node(self, xcoord, ycoord, name=None):
        """Add a start node"""
        node = CStartNode(xcoord, ycoord, self.model)
        return self.add_start_trap_node(node, name)

    def add_trap_node(self, xcoord, ycoord, name=None):
        """Add a trap node"""
        node = CTrapNode(xcoord, ycoord, self.model)
        return self.add_start_trap_node(node, name)

    def add_start_trap_node(self, node, name):
        """Add a start or trape node to he model

        Handy function called by add_start_node, add_trap_node
        """
        # Not CSimpleNode; thus the node is not added to simple_node_dict
        self.model.node_dict[name] = node

        node.father = self
        if name:
            node.name = name
        else:
            # add a number to have different graphic start nodes
            node.name += str(self.start_trap_nodes_count)
        self.start_trap_nodes_count += 1
        self.sub_nodes.append(node)
        self.model.modified = True
        self.model.notify()
        return node

    def add_perm_node(self, name, xcoord, ycoord):
        """
        Add a perm node
        """
        node = CPermNode(xcoord, ycoord, name, self.model)
        # Not CSimpleNode; thus the node is not added to simple_node_dict
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.modified = True
        self.model.notify()
        return node

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """Draw transitions and nodes contained in this MacroNode

        @param view: drawing area
        @param xfr: x coordinate of father in virtual screen
        @param yfr: y -
        @param wfr: father's width in virtual screen
        @param hfr: father's height in virtual
        @param depth: depth of the node; less than depth_max
        """
        dstyle = view.drawing_style
        # draw node
        dstyle.draw_macro(self, xfr, yfr, wfr, hfr)
        # draw sub graph
        if depth < CMacroNode.depth_max and self.model.show_macro:
            xxr = xfr + self.xloc * wfr
            yyr = yfr + self.yloc * hfr
            w_ratio = wfr * self.wloc
            h_ratio = hfr * self.hloc
            # transitions
            for tgr in self.transitions:
                dstyle.draw_transition_group(tgr, xxr, yyr, w_ratio, h_ratio)
            # nodes
            for snode in self.sub_nodes:
                snode.draw(view, xxr, yyr, w_ratio, h_ratio, depth + 1)

    def move(self, v_dx, v_dy, v_size, top_node):
        """
        Move the node - mx_virt, my virt are virtual coordinates of the mouse
        click_loc (pair) is the location of the clic in node's frame
        """
        # don't try to move a root node
        if self == top_node:
            return
        # move in reference frame (father's)
        (ccx, ccy) = self.father.v_affinity_coef(top_node)
        loc_dx = ccx * v_dx
        loc_dy = ccy * v_dy
        # translation vector in reference frame i.e. father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy
        # check limits
        wloc = v_size[0] * ccx
        hloc = v_size[1] * ccy
        delta = v_size[2] * ccy

        if self.model.show_macro:
            wloc = self.wloc
            hloc = self.hloc
        else:
            wloc = v_size[0] * ccx
            hloc = v_size[1] * ccy
        move = False
        if (new_xloc >= 0) and (new_xloc + wloc < 1.0):
            self.xloc = new_xloc
            move = True
        if (new_yloc > delta) and (new_yloc + hloc < 1.0):
            self.yloc = new_yloc
            move = True
        if move:
            self.model.modified = True
            self.model.notify()

    def find_element(self, mox, moy, dstyle, w_coef, h_coef):
        """
        @param mox, moy: mouse coordinate in container frame
        @param dstyle: drawing style
        @param w_coef, h_coef: affinity ratios for view -> container frame
        """
        # width and height of the node in container frame
        if self.model.show_macro:
            wloc = self.wloc
            hloc = self.hloc
        else:
            bb_size = self.accept(dstyle)
            wloc = bb_size[0] * w_coef
            hloc = bb_size[1] * h_coef
        in_node = (mox >= self.xloc) and (mox <= self.xloc + wloc)
        in_node = in_node and (moy >= self.yloc) and (moy <= self.yloc + hloc)
        if in_node:
            if not self.model.show_macro:
                ccx = self.xloc + 0.5 * wloc
                ccy = self.yloc + 0.5 * hloc
                return (self, 0, (ccx, ccy), None)

            # change coordinates and affinity ratio for self frame
            w_coefloc = w_coef / wloc
            h_coefloc = h_coef / hloc
            mxloc = (mox - self.xloc) / wloc
            myloc = (moy - self.yloc) / hloc
            # search sub node
            for snode in self.sub_nodes:
                (nnn, hhh, ccc, ttt) = snode.find_element(
                    mxloc, myloc, dstyle, w_coefloc, h_coefloc
                )
                if nnn:
                    # n center coordinates in container frame
                    ccx = self.xloc + ccc[0] * self.wloc
                    ccy = self.yloc + ccc[1] * self.hloc
                    return (nnn, hhh, (ccx, ccy), ttt)

            # self center coordinate in container frame
            ccx = self.xloc + 0.5 * self.wloc
            ccy = self.yloc + 0.5 * self.hloc

            # not in a subnode, find a transition at this level
            trans = self.find_transition(mxloc, myloc, dstyle, w_coefloc, h_coefloc)
            if trans:
                return (self, 0, (ccx, ccy), trans)

            # not in a subnode or transition- find handler
            v_size = self.accept(dstyle)
            ddx = v_size[3]
            ddy = v_size[4]

            if (mox < self.xloc + ddx) and (moy < self.yloc + ddy):
                return (self, 1, (ccx, ccy), None)
            if (mox > self.xloc + wloc - ddx) and (moy < self.yloc + ddy):
                return (self, 2, (ccx, ccy), None)
            cond = mox > self.xloc + wloc - ddx
            cond = cond and (moy > self.yloc + hloc - ddy)
            if cond:
                return (self, 3, (ccx, ccy), None)
            if (mox < self.xloc + ddx) and (moy > self.yloc + hloc - ddy):
                return (self, 4, (ccx, ccy), None)
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def find_transition(self, mox, moy, dstyle, w_coef, h_coef):
        """
        Look for transitions pointed by mouse
        No recursive search - transitions are in current node
        """
        for trans in it.chain(*self.transitions):
            if trans.is_me(mox, moy, dstyle, w_coef, h_coef):
                return trans

    def resize(self, mx_virt, my_virt, handle, screen_w, screen_h, top_node):
        """Resize the node with the mouse

        @param  mx_virt, my_virt:  mouse coordinates in virtual window
        @param handle: as determined by find_node
        @param screen_w, screen_h: size of the screen in pixels
        @param top_node: root node of the sub model
        """
        # don't try to resize a root node
        if self == top_node:
            return

        (mx_loc, my_loc) = self.father.virt_to_self_frame(
            mx_virt, my_virt, screen_w, screen_h, top_node
        )
        if handle == 1:  # top left corner
            change = False
            new_xloc = mx_loc
            new_wloc = self.xloc + self.wloc - mx_loc
            if new_xloc > 0 and new_wloc > CNode.wmin:
                self.xloc = new_xloc
                self.wloc = new_wloc
                change = True
            new_yloc = my_loc
            new_hloc = self.yloc + self.hloc - my_loc
            if new_yloc > 0 and new_hloc > CNode.hmin:
                self.yloc = new_yloc
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

        elif handle == 2:  # top right corner
            change = False
            new_wloc = mx_loc - self.xloc
            if self.xloc + new_wloc < 1.0 and new_wloc > CNode.wmin:
                self.wloc = new_wloc
                change = True
            new_yloc = my_loc
            new_hloc = self.yloc + self.hloc - my_loc
            if new_yloc > 0 and new_hloc > CNode.hmin:
                self.yloc = new_yloc
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

        elif handle == 3:  # bottom right corner
            change = False
            new_wloc = mx_loc - self.xloc
            if self.xloc + new_wloc < 1.0 and new_wloc > CNode.wmin:
                self.wloc = new_wloc
                change = True
            new_hloc = my_loc - self.yloc
            if self.yloc + new_hloc < 1.0 and new_hloc > CNode.hmin:
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

        elif handle == 4:  # bottom left corner
            change = False
            new_xloc = mx_loc
            new_wloc = self.xloc + self.wloc - mx_loc
            if new_xloc > 0 and new_wloc > CNode.wmin:
                self.xloc = new_xloc
                self.wloc = new_wloc
                change = True
            new_hloc = my_loc - self.yloc
            if self.yloc + new_hloc < 1.0 and new_hloc > CNode.hmin:
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        Gives the the first point where to branch a transition, the gap between two arrows
        and a boolean horizontal true if arrows start from horizontal edge
        @param node2: second node of the transition
        @param dstyle: drawing style
        @param nb_trans: number of transitions to be drawn
        @param w_ratio,h_ratio: dimentions of the screen for fixed size nodes
        """
        if not self.model.show_macro:
            return intersect_simple(self, node2, dstyle, nb_trans, w_ratio, h_ratio)
        (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
        uux = xc2 - (self.xloc + self.wloc / 2.0)
        uuy = yc2 - (self.yloc + self.hloc / 2.0)
        wloc = self.wloc
        hloc = self.hloc
        limit_slope = hloc / wloc

        if uux != 0.0:
            slope = uuy / uux
            if slope <= -limit_slope:
                if uux > 0:
                    side = 1
                else:
                    side = 3
            elif slope >= limit_slope:
                if uux < 0:
                    side = 1
                else:
                    side = 3
            else:  # -limit_slope < slope < limit_slope
                if uux > 0:
                    side = 2
                else:
                    side = 4
        else:
            if uuy >= 0:
                side = 3
            else:
                side = 1

        if side == 1:
            horizontal = True
            gap = wloc / (nb_trans + 1)
            six = self.xloc + gap
            siy = self.yloc
            return (six, siy, gap, horizontal)
        if side == 3:
            horizontal = True
            gap = wloc / (nb_trans + 1)
            six = self.xloc + gap
            siy = self.yloc + hloc
            return (six, siy, gap, horizontal)
        if side == 2:
            horizontal = False
            gap = hloc / (nb_trans + 1)
            six = self.xloc + wloc
            siy = self.yloc + gap
            return (six, siy, gap, horizontal)
        if side == 4:
            horizontal = False
            gap = hloc / (nb_trans + 1)
            six = self.xloc
            siy = self.yloc + gap
            return (six, siy, gap, horizontal)

    def clean(self):
        self.activated = False
        for node in self.sub_nodes:
            node.clean()
        for gtr in self.transitions:
            for trans in gtr:
                trans.clean()

    def clean_code(self):
        """
        clean the code
        """
        for ltr in self.transitions:
            for trans in ltr:
                trans.clock = None
        for node in self.sub_nodes:
            if node.is_macro():
                node.clean_code()

    def accept(self, visitor):
        """
        Standard visitor acceptor
        """
        return visitor.visit_cmacro_node(self)


class CTopNode(CMacroNode):
    """
    A virtual macronode on top of the hierarchy. A model can be a list of hierarchy.
    This artificial node groups all the hierarchy. From a graphical point of view,
    it represents the virtual drawing window.

    .. note:: We assume that the first node in sub_nodes is the main MacroNode.
        TODO: test if there are another nodes in sub_nodes?
    """

    def __init__(self, name, model, **kwargs):
        CMacroNode.__init__(self, 0.0, 0.0, 1.0, 1.0, name, model, **kwargs)
        self.submodel = False
        self.env_node = None  # for environment interaction in tests
        # nb no father node

    def copy(self):
        """Duplicate a CTopNode
        - Performs a deep copy
        - Reduce displayed dimensions
        - The top node is changed into a macro node
        - The env_node (if any) is not copied.
        """
        LOGGER.debug("CMacroNode::copy")
        child_node = CMacroNode(self.xloc, self.yloc, 0.3, 0.3, self.name, self.model, note=self.note)
        # copy subnodes
        self.copy_subnodes(child_node)
        # copy transitions
        self.copy_transitions(child_node)
        return child_node

    def is_for_origin(self):
        return False

    def is_for_extremity(self):
        return False

    def is_top_node(self):
        return True

    def draw(self, view):
        """The TOP node is virtual - so no drawing
        if there is only one subnode which is a macro - draw it full screen
        (this is the case when a macro node is edited in a new tab)
        """
        dstyle = view.drawing_style
        if self.submodel:
            mno = self.sub_nodes[0]
            w_ratio = 1.0 / mno.wloc
            h_ratio = 1.0 / mno.hloc
            xxr = -mno.xloc * w_ratio
            yyr = -mno.yloc * h_ratio
            mno.draw(view, xxr, yyr, w_ratio, h_ratio, 0)
            return
        # top of a full model
        # transitions
        for tgr in self.transitions:
            if self.submodel:
                dstyle.draw_transition_group(tgr, 0.0, 0.0, 1.0, 1.0, self.sub_nodes[0])
            else:
                dstyle.draw_transition_group(tgr, 0.0, 0.0, 1.0, 1.0)
        # nodes
        for snode in self.sub_nodes:
            snode.draw(view, 0.0, 0.0, 1.0, 1.0, 1)

    def find_element(self, mox, moy, dstyle):
        """
        @param mox,moy :coordinates of the mouse in local frame (own frame for top node)
        @param dstyle: drawing style used in the view

        Given the window mouse coordinates, return (node, handle, center) where node is the
        node the mouse is in,  handle the handle of the node the mouse is in and c are the coordinates
        of the node center in view.
        If no handle, handle = 0, handle are 1,2,3,4 clockwise numbered from upper left corner
        If no node found returns (None,0,(0,0))
        """
        # if model size two large don't draw => don't search
        nb_snodes = len(self.model.simple_node_dict)
        if nb_snodes > self.model.max_size:
            return (self, 0, (0, 0), None)  # no handle for top node

        if self.submodel:
            # TODO check new version with virtual screen
            mno = self.sub_nodes[0]
            # mouse coordinates in father frame
            mox = mox * mno.wloc + mno.xloc
            moy = moy * mno.hloc + mno.yloc
            # top node coefs in father frame
            w_coef = mno.wloc
            h_coef = mno.hloc
            return mno.find_element(mox, moy, dstyle, w_coef, h_coef)
        w_coef = 1.0
        h_coef = 1.0
        for snode in self.sub_nodes:
            (nnn, hhh, ccc, ttt) = snode.find_element(mox, moy, dstyle, w_coef, h_coef)
            if nnn:
                # center in  screen
                ccx = ccc[0] / w_coef
                ccy = ccc[1] / h_coef
                return (nnn, hhh, (ccx, ccy), ttt)
        # no subnode found: try to find a transition at top level
        for trans in it.chain(*self.transitions):
            if trans.is_me(mox, moy, dstyle, w_coef, h_coef):
                ccx = 0.5 / w_coef
                ccy = 0.5 / h_coef
                return (self, 0, (ccx, ccy), trans)
        # no subnode and no transition found
        return (self, 0, (0, 0), None)  # no handle for top node

#    def aff_coefs(self, top_node):
#        """
#        Affinity coefficients
#        """
#        return (1.0, 1.0)

    def aff_coef(self, swidth, sheight, top_node):
        """
        Affinity coefficients
        """
        return (1.0 / swidth, 1.0 / sheight)

    def move(self, v_dx, v_dy, v_size, top_node):
        pass  # no move for top node

    def add_submodel(self, mnode):
        """
        add a submodel (subtree) with root a macro node (no check performed)
        """
        self.submodel = True
        self.sub_nodes.append(mnode)
        self.model.modified = True

    def accept(self, visitor):
        return visitor.visit_ctop_node(self)


class CTransition(object):
    """A guarded transition object"""

    def __init__(self, origin, extremity):
        """
        @param origin : CNode
        @param extremity : CNode
        """
        self.macro_node = None
        self.ori = origin
        self.ext = extremity
        self.name = ""
        self.event = ""
        self.condition = ""
        self.action = ""
        self.selected = False
        self.search_mark = False
        self.activated = False
        self.fact_ids = []  # list of associated facts id
        self.note = ""
        # for compiler (avoid redondant clause generation)
        self.clock = None
        self.ori_coord = 0.0  # to be set by layout
        self.ext_coord = 0.0

    def set_event(self, event):
        """
        @param event: string
        """
        self.event = event
        self.ori.model.modified = True

    def set_condition(self, cond):
        """
        @param cond : string
        """
        self.condition = cond
        self.ori.model.modified = True

    def set_action(self, act):
        """
        @param act: string
        """
        self.action = act
        self.ori.model.modified = True

    def set_name(self, name):
        """
        @param name: string
        """
        self.name = name
        self.ori.model.modified = True

    def set_note(self, note):
        """
        @param note: string
        """
        self.note = str(note)

    def get_key(self):
        """
        key for storing the transition in dictionaries
        """
        key = self.ori.name + self.ext.name + self.event
        key = key + self.condition + self.action
        return key

    def clean(self):
        """
        Unmark
        """
        self.activated = False

    def get_influencing_places(self):
        """Return set of places that influence the condition of the transition

        :rtype: <set <str>>
        """
        if not self.condition:
            return set()
        text_c = self.condition + "$"
        reader = ANTLRStringStream(text_c)
        lexer = condexpLexer(reader)
        parser = condexpParser(CommonTokenStream(lexer))
        try:
            return parser.sig_bool()
        except Exception as e:
            LOGGER.error(
                "CTransition::get_influencing_places: %s - %s",
                e.__class__.__name__,
                e
            )
            return set()

    def is_me(self, mox, moy, dstyle, w_coef, h_coef):
        """Tell if mouse position is closed to transition

        :param mox, moy: mouse coordinates in container coord (local coordinates)
        :return: True or False
        :rtype: <boolean>
        """
        v_size = self.accept(dstyle)
        dist_max = max(v_size[0], v_size[1])
        # extremities
        (x_or, y_or) = self.ori_coord
        (x_tg, y_tg) = self.ext_coord

        # distance from mouse cursor
        llx = x_tg - x_or
        lly = y_tg - y_or
        norm = sqrt(llx * llx + lly * lly)
        if norm == 0:
            return  # must not happen
        llx = llx / norm
        lly = lly / norm
        xxx = mox - x_or
        yyy = moy - y_or
        uuu = llx * xxx + lly * yyy
        dist = (xxx - uuu * llx) * (xxx - uuu * llx)
        dist = dist + (yyy - uuu * lly) * (yyy - uuu * lly)
        dist = sqrt(dist)

        if dist < dist_max:
            # are we in the bounds
            ddx = abs(x_or - x_tg)
            ddy = abs(y_or - y_tg)
            if ddx > 0.05:
                condx = (abs(mox - x_or) <= ddx) and (abs(mox - x_tg) <= ddx)
            else:
                condx = True
            if ddy > 0.05:
                condy = (abs(moy - y_or) <= ddy) and (abs(moy - y_tg) <= ddy)
            else:
                condy = True
            return condx and condy
        else:
            return False

    def remove(self):
        """Remove the current transition from its macro node"""
        # Key: {<CNode>, <CNode>}; values: [<CTransition>, ...]
        temp_transitions = defaultdict(list, self.macro_node.new_transitions)
        for nodes, transitions in self.macro_node.new_transitions.items():
            if self in transitions:
                if len(transitions) == 1:
                    # Remove nodes couple/transitions
                    temp_transitions.pop(nodes)
                    continue
                # Multiple transitions for a couple of nodes: remove only the current one
                # => Is it really happen?
                LOGGER.warning(
                    "CTransition::remove: "
                    "Multiple transitions for a couple of nodes;"
                    "Remove only the current transition"
                )
                transitions.remove(self)

        self.macro_node.new_transitions = temp_transitions
        # print("ori out:", self.ori.outgoing_trans)
        # print("ext in:", self.ext.incoming_trans)
        # Nodes must contain the transitions related to them
        self.ori.outgoing_trans.remove(self)
        self.ext.incoming_trans.remove(self)
        # Model must contain all the transitions
        self.ori.model.transition_list.remove(self)
        self.ori.model.modified = True

    def accept(self, visitor):
        """
        standard accept visitor
        """
        return visitor.visit_ctransition(self)

    def __repr__(self):
        return "<CTransition {} -> {}; cond:{}; event:{}>".format(
            self.ori.name, self.ext.name, self.condition, self.event
        )


def intersect_simple(node1, node2, dstyle, nb_trans, w_ratio, h_ratio):
    """Helper function: Intersection of a node with a transition
    """
    # simple nodes have constant screen dimensions - convert to local ones
    v_size = node1.accept(dstyle)
    wloc_snode = v_size[0] / w_ratio
    hloc_snode = v_size[1] / h_ratio

    (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
    uux = xc2 - (node1.xloc + wloc_snode / 2.0)
    uuy = yc2 - (node1.yloc + hloc_snode / 2.0)
    if uux != 0.0:
        slope = uuy / uux
        u_slope = v_size[1] / v_size[0]
        if slope <= -u_slope:
            if uux > 0:
                side = 1
            else:
                side = 3
        elif slope >= u_slope:
            if uux < 0:
                side = 1
            else:
                side = 3
        else:  # -U_SLOPE < slope < U_SLOPE
            if uux > 0:
                side = 2
            else:
                side = 4
    else:
        if uuy >= 0:
            side = 3
        else:
            side = 1

    if side == 1:  # hight horizontal
        horizontal = True
        if nb_trans == 1:
            six = node1.xloc + 0.5 * wloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = wloc_snode * 0.6
            six = node1.xloc + 0.2 * wloc_snode
        siy = node1.yloc
        return (six, siy, gap, horizontal)
    if side == 3:  # low horizontal
        horizontal = True
        if nb_trans == 1:
            six = node1.xloc + 0.5 * wloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = wloc_snode * 0.6
            six = node1.xloc + 0.2 * wloc_snode
        siy = node1.yloc + hloc_snode
        return (six, siy, gap, horizontal)
    if side == 2:  # right vertical
        horizontal = False
        if nb_trans == 1:
            siy = node1.yloc + 0.5 * hloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = hloc_snode * 0.6
            siy = node1.yloc + 0.2 * hloc_snode
        six = node1.xloc + wloc_snode
        return (six, siy, gap, horizontal)
    if side == 4:  # left vertical
        horizontal = False
        if nb_trans == 1:
            siy = node1.yloc + 0.5 * hloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = hloc_snode * 0.6
            siy = node1.yloc + 0.2 * hloc_snode
        six = node1.xloc
        return (six, siy, gap, horizontal)
