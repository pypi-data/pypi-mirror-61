# -*- coding: utf-8 -*-
## Filename    : chart_xml.py
## Author(s)   : Geoffroy Andrieux
## Created     : 04/2010
## Revision    :
## Source      :
##
## Copyright 2010 : IRISA
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
## Contributor(s): Michel Le Borgne, Nolwenn Le Meur
##
"""Load and generate Cadbiom xml files

Classes:

- :class:`XmlVisitor`: Visitor used to generate xml cadbiom code when the
  model is exported.
- :class:`MakeHandler`: Make a handler for the parser when the model is loaded.
- :class:`MakeModelFromXmlFile`: Handy class used to parse an xml file.
- :class:`MakeModelFromXmlString`: Handy class used to parse an xml string.
"""
from __future__ import unicode_literals
from __future__ import print_function
import itertools as it
from collections import OrderedDict

from xml.sax import make_parser
from xml.sax import parseString
from xml.sax.handler import ContentHandler
from lxml import etree
from lxml import objectify

from cadbiom.models.guard_transitions.chart_model import ChartModel
import cadbiom.commons as cm

LOGGER = cm.logger()


class XmlVisitor:
    """Visitor used to generate XML Cadbiom code when the model is exported.

    :param model: Chart model - Cadbiom model
    :param fact_list: List of fact ids found in all the transitions.
    :param xml: xml string representation of the model
    :param symb: symbol set used to check double naming of nodes;
        Double declarations are problematic.
    :param default_node_attributes:
    :type model: <ChartModel>
    :type fact_list: <list <str>>
    :type xml: <str>
    :type symb: <set>
    :type default_node_attributes: <tuple <str>>
    """

    def __init__(self, model):
        self.model = model
        self.fact_list = []
        self.xml = ""
        self.symb = set()
        self.default_node_attributes = ("name", "xloc", "yloc", "wloc", "hloc")
        self.visit_chart_model()

    def visit_chart_model(self):
        """Entrance point for visitors

        Called by the constructor and by the
        :meth:`cadbiom.models.guard_transitions.chart_model.ChartModel.accept`
        method.
        """
        self.visit_ctop_node(self.model.get_root())

    def check_name(self, name):
        """
        Detect double declarations
        """
        if name in self.symb:
            raise Exception("XML Parsing: Node double declaration")
        else:
            self.symb.add(name)

    def get_existing_attributes(self, node):
        """Return dict of attributes of the given node

        .. note:: The set of attributes are defined in the default_node_attributes
            attribute of the current class.

        .. note:: We use OrderedDict in order to improve human readability of
            the produced models.

        :return: Dictionary of attributes.
            Keys: names of attributes; Values: Values of attributes;
            Note that values are converted to strings in order to fit with lxml
            requirements.
        :rtype: <OrderedDict <str>:<str>>
        """

        return OrderedDict((
            (attr_name, str(node.__dict__[attr_name]))
            for attr_name in self.default_node_attributes
            if node.__dict__.get(attr_name, None)
        ))

    def visit_cstart_node(self, snode):
        """Return tag name and formated attributes of a start node

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        # double declaration is allowed
        return "CStartNode", self.get_existing_attributes(snode)

    def visit_ctrap_node(self, tnode):
        """Return tag name and formated attributes of a trap node

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        # double declaration is allowed
        return "CTrapNode", self.get_existing_attributes(tnode)

    def visit_csimple_node(self, sin):
        """Return tag name and formated attributes of a simple node

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        self.check_name(sin.name)
        return "CSimpleNode", self.get_existing_attributes(sin)

    def visit_cperm_node(self, pnode):
        """Return tag name and formated attributes of a perm node

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        self.check_name(pnode.name)
        return "CPermNode", self.get_existing_attributes(pnode)

    def visit_cinput_node(self, inn):
        """Return tag name and formated attributes of an input node

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        # double declaration is allowed
        return "CInputNode", self.get_existing_attributes(inn)

    def visit_cmacro_node(self, mnode):
        """Explore subnodes and transitions in the given macro node.

        Return tag name and formated attributes of a macro node.

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        self.check_name(mnode.name)
        save_macro = self.current_element
        macro_node_tag = "CMacroNode"
        # Get attributes
        # Keys: attr names; Values: attr values
        macro_node_attrs = self.get_existing_attributes(mnode)

        # Create new XML tag
        macro = etree.SubElement(self.current_element, macro_node_tag, macro_node_attrs)
        self.current_element = macro

        # nodes
        for snode in mnode.sub_nodes:
            tag, attrs = snode.accept(self)
            if tag == "CMacroNode":
                self.current_element = macro
            else:
                etree.SubElement(self.current_element, tag, attrs)

        # transitions
        for transition in it.chain(*mnode.transitions):
            tag, attrs = transition.accept(self)
            etree.SubElement(self.current_element, tag, attrs)

        self.current_element = save_macro

        return macro_node_tag, macro_node_attrs

    def visit_ctop_node(self, tnode):
        """Interative build of XML tree for model saving

        .. note:: namespace seems to be useless regarding nsmap here,
            because we use the default namespace without prefix...
            See http://lxml.de/tutorial.html#namespaces.
        """
        header = objectify.ElementMaker(
            annotate=False,
            # namespace="http://cadbiom.genouest.org/",
            # nsmap={None: "http://cadbiom.genouest.org/"}
            namespace=self.model.xml_namespace,
            # the default namespace (no prefix)
            nsmap={None: self.model.xml_namespace},
        )
        xmodel = header.model(name=self.model.name)
        self.current_element = xmodel

        def create_xml_element(entity):
            """Create XML element and add it to root object"""
            # get node or transition properties
            tag, attrs = entity.accept(self)
            if tag != "CMacroNode":
                # Create new XML tag
                # Set attributes and values (name, event, coords...)
                element = etree.Element(tag, attrs)

                # Add notes/text of element
                if entity.note:
                    element.text = entity.note
                # Attach element to the model
                xmodel.append(element)

        # nodes
        [create_xml_element(snode) for snode in tnode.sub_nodes]

        # transitions
        [create_xml_element(trans) for trans in it.chain(*tnode.transitions)]

        # constraints
        if tnode.model.constraints:
            # There is text on constraints
            const = etree.Element("constraints")
            const.text = tnode.model.constraints
            xmodel.append(const)

        # Add preamble
        self.xml = '<?xml version = "1.0" encoding="ASCII" standalone="yes" ?>\n'
        self.xml += etree.tostring(xmodel, pretty_print=True)
        # print(etree.tostring(xmodel,pretty_print=True))

    def visit_ctransition(self, trans):
        """Return tag name and formated attributes of a transition

        :return: Tuple of tag name and OrderedDict of attributes
        :rtype: <str>, <OrderedDict <str>:<str>>
        """
        # Mandatory attributes
        attr_names = ("ori", "ext", "event", "condition")
        attr_values = (
            trans.ori.name,
            trans.ext.name,
            trans.event,
            trans.condition,
        )
        attrs = OrderedDict(zip(attr_names, attr_values))

        # Optional attributes
        attr_names = ("action", "fact_ids")
        attrs.update({
            attr_name: str(trans.__dict__[attr_name]) for attr_name in attr_names
            if trans.__dict__[attr_name]
        })

        # Merge facts of the transition with XmlVisitor (why?)
        self.fact_list += trans.fact_ids

        return "transition", attrs

    def return_xml(self):
        """Return the model as xml string.

        .. note:: Used when the model is saved in a .bcx file.
        """
        return self.xml

    def get_fact_ids(self):
        """Get litterature references

        :rtype: <set>
        """
        return set(self.fact_list)


class MakeHandler(ContentHandler):
    """Make a handler for the parser when the model is loaded.

    Users are expected to subclass ContentHandler to support their application.
    The following methods are called by the parser on the appropriate events
    in the input document:

    https://docs.python.org/2/library/xml.sax.handler.html
    """

    def __init__(self, model=None):
        self.pile_node = []
        self.top_pile = None
        self.pile_dict = []
        self.node_dict = dict()
        self.in_constraints = False
        self.constraints = ""
        self.model = model
        self.nodes_types = (
            'CStartNode', 'CTrapNode', 'CSimpleNode', 'CPermNode', 'CInputNode'
        )
        # Memorize the current node/transition because of inner text (note)
        # processing
        self.current_element = None
        # Encoding of node names
        self.encoding = "ascii"

    def init_node_functions(self, top_pile=None):
        """Bind functions to add different types of nodes to the cadbiom model

        .. note:: Must be call after the init of self.top_pile with the xml root
            object.

        .. note:: If called when a MacroNode is encountered; must be called
            when the end-tag is encountered with the parent node set in top_pile
            argument.

        :param top_pile: If set, all futures nodes will belong to this node.
            It is used for MacroNodes: all subnodes belong to them.
        :type top_pile: <CNode>
        """
        if not top_pile:
            top_pile = self.top_pile

        self.add_node_functions = {
            "CStartNode": top_pile.add_start_node,
            "CTrapNode": top_pile.add_trap_node,
            "CSimpleNode": top_pile.add_simple_node,
            "CPermNode": top_pile.add_perm_node,
            "CInputNode": top_pile.add_input_node,
        }

    def startElement(self, name, att):
        """Signal the start of an element

        .. note:: Nodes have to be at the top of the model (Before transitions)
            Transitions do not allow reflexive ones
            (as it could be said in the doc);
            Duplication of transitions are not authorized but only print a
            warning in the shell (they are not taken into account)

        :param arg1: Contains the raw XML 1.0 name of the element.
        :param arg2: Holds an object of the Attributes interface.
        :type arg1: <str>
        :type arg2: <xml.sax.xmlreader.AttributesImpl>
        """
        # print(att.getNames())

        if name in self.nodes_types:
            # TODO: Uniformization of API in CMacroNode() class;
            # the attribute 'name' should be at the same last position...
            element_name = att.get("name", "").encode(self.encoding)
            self.current_element = self.add_node_functions[name](
                name=element_name,
                xcoord=float(att.get("xloc", "0")),
                ycoord=float(att.get("yloc", "0")),
            )
            self.node_dict[element_name] = self.current_element

        elif name == "transition":
            ori = att.get("ori", "").encode(self.encoding)
            ext = att.get("ext", "").encode(self.encoding)
            event = att.get("event", "")
            condition = att.get("condition", "").encode(self.encoding)
            action = att.get("action", "")
            fact_ids_text = att.get("fact_ids", "")[1:-1]
            if len(fact_ids_text) > 0:
                fact_ids = [int(id) for id in fact_ids_text.split(",")]
            else:
                fact_ids = []

            # Get nodes involved in the transition
            # If not present, raise an exception
            # => nodes have to be at the top of the model
            try:
                node_ori = self.node_dict[ori]
                node_ext = self.node_dict[ext]
            except KeyError as exc:
                LOGGER.error("Bad xml file - missing nodes %s in %s -> %s", exc, ori, ext)
                LOGGER.error("Nodes in memory: %s", self.node_dict)
                raise

            self.current_element = self.top_pile.add_transition(node_ori, node_ext)
            # The transition may not be created (origin = ext for example)
            # /!\ Transitions do not allow reflexive ones
            # (as it could be said in the doc)
            # Duplication of transitions are not authorized but only print a
            # warning in the shell (they are not taken into account)
            if self.current_element:
                self.current_element.set_event(event)
                self.current_element.set_condition(condition)
                self.current_element.set_action(action)
                self.current_element.fact_ids = fact_ids

        elif name == "CMacroNode":
            name = att.get("name", "").encode(self.encoding)
            xloc = float(att.get("xloc", "0"))
            yloc = float(att.get("yloc", "0"))
            wloc = float(att.get("wloc", "5"))
            hloc = float(att.get("hloc", "5"))

            node = self.top_pile.add_macro_subnode(name, xloc, yloc, wloc, hloc)
            self.node_dict[name] = node

            self.pile_node.append(node)
            # symbol table put on stack to preserve macro scope for inputs
            new_node_dict = dict()
            self.pile_dict.append(new_node_dict)
            self.top_pile = node
            self.node_dict = new_node_dict

            # Future nodes belong to this MacroNode
            self.init_node_functions(top_pile=node)

        elif name == "constraints":
            self.in_constraints = True
            self.constraints = ""

        elif name == "model":
            if not self.model:
                # Init CharModel: get name and namespace (default v1)
                self.model = ChartModel(
                    att.get("name", ""),
                    att.get("xmlns", "http://cadbiom.genouest.org/"),
                )
            # Root is a virtual macronode on top of the hierarchy.
            # A model can be a list of hierarchy grouped under this node.
            root = self.model.get_root()
            self.pile_node.append(root)
            self.top_pile = root
            self.init_node_functions()
            new_dict = dict()
            self.pile_dict.append(new_dict)
            self.node_dict = new_dict

    def characters(self, chr):
        """Receive notification of character data.

        The Parser will call this method to report each chunk of character data.
        SAX parsers may return all contiguous character data in a single chunk,
        or they may split it into several chunks;
        => we need to do a concatenation

        :param arg1: chunck of characters.
        :type arg1: <str>
        """
        # The current elem is a constraint, a transition or a node
        # print("all", self.current_element, '<'+chr+'>')
        if self.in_constraints:
            self.constraints += chr
        elif self.current_element:
            # node or transition is currently opened in startElement()
            self.current_element.note += chr

    def endElement(self, name):
        """Called when an elements ends

        .. note:: We handle only elements that need post processing like
            transitions and nodes: reset self.current_element that is used
            to load notes (inner text of xml object).
        """

        if name == "transition" or name in self.nodes_types:
            # Close the current node or transition opened in startElement()
            self.current_element = None
        elif name == "CMacroNode":
            # self.top_pile = self.pile_node.pop()
            self.pile_node.remove(self.top_pile)
            self.top_pile = self.pile_node[-1]

            # Future nodes belong to the parent of this MacroNode
            self.init_node_functions()

            # self.node_dict = self.pile_dict.pop()
            self.pile_dict.remove(self.node_dict)
            self.node_dict = self.pile_dict[-1]
        elif name == "constraints":
            self.in_constraints = False
            self.model.constraints = self.constraints + "\n"
        # elif name == 'model':
        #    print(len([e for e in self.top_pile.transitions]))
        #    print(len(self.top_pile.new_transitions))


class MakeModelFromXmlFile:
    """Handy class used to parse an xml file"""

    def __init__(self, xml_file, model=None):
        """
        :param xml_file: Path of XML file
        :param model: Pre-computed model (never used)
        :type xml_file: <str>
        :type model: <ChartModel>
        """
        self.handler = MakeHandler(model=model)
        self.parser = make_parser()
        self.parser.setContentHandler(self.handler)

        try:
            self.parser.parse(xml_file)

            # The model is currently not modified in comparison to the file
            self.handler.model.modified = False
        except Exception:
            LOGGER.error("Error while reading the XML file <%s>", xml_file)
            raise

    @property
    def model(self):
        """Return the model generated from the XML file

        :rtype: <ChartModel>
        """
        return self.handler.model


class MakeModelFromXmlString:
    """Handy class used to parse an xml string."""

    def __init__(self, xml_string):
        self.model = None
        self.handler = MakeHandler()
        self.parser = make_parser()
        self.parser.setContentHandler(self.handler)

        try:
            parseString(xml_string, self.handler)

            # The model is currently not modified in comparison to the file
            self.handler.model.modified = False
        except Exception:
            LOGGER.error("Error while reading the XML string")
            raise

    @property
    def model(self):
        """Return the model generated from the XML string

        :rtype: <ChartModel>
        """
        return self.handler.model
