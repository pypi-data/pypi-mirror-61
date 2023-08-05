
## Filename    : CLDynSys.py
## Author(s)   : Michel Le Borgne
## Created     : 05/2011
## Revision    :
## Source      :
##
## Copyright 2011 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided here under is on an "as is" basis, and  has
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
## Contributor(s): Geoffroy Andrieux
##
"""
Classes for building clause constraint models
"""
from collections import defaultdict


class Clause():
    """Objects representing logical clauses

    A clause is represented as a list of literals.

    Attributes:

        :param literals: Variable name
        :type literals: <list <Literal>>
    """
    def __init__(self, list_lit=[]):
        self.literals = list_lit

    @classmethod
    def string_to_clause(cls, text_clause):
        """Transform a string into a clause (not used)

        Example of text: "a,not b,not c".

        .. warning:: strict syntax - no check - for tests only
        """
        # Split into literals
        clause = Clause([])
        # Translate each literal
        for lit in text_clause.split(','):
            spl = lit.split()
            if len(spl) == 1:
                # "a"
                clause.add_lit(Literal(spl[0], True))
            else:
                # "not a"
                clause.add_lit(Literal(spl[1], False))
        return clause

    def add_lit(self, lit):
        """Add a literal to the clause
        @param lit: <Literal>
        """
        self.literals.append(lit)

    def __eq__(self, other):
        """Test if two clauses have the same literals
        Used by clause_list_equal() (never used)
        """
        return frozenset(self.literals) == frozenset(other.literals)

    def __ne__(self, other):
        """Test clause inequality"""
        return not self.__eq__(other)

    def __lt__(self, other):
        """Test if the current clause is shorter than another"""
        return len(self.literals) < len(other.literals)

    def __gt__(self, other):
        """Test if the current clause is longer than another"""
        return len(self.literals) > len(other.literals)

    def __str__(self):
        return "$" + ", ".join(str(lit) for lit in self.literals) + "$"

    def __repr__(self):
        return str(self)


class Literal():
    """Object representing literals.

    A literal is a pair (string, boolean).

    Attributes:

        :param name: Variable name
        :param sign: Boolean the sign of the literal.
            Positive or negative: True or False
        :type name: <str>
        :type sign: <boolean>
    """
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

    def lit_not(self):
        """Return the negation of the literal (opposite sign)"""
        return Literal(self.name, not self.sign)

    def __eq__(self, other):
        """Test literal equality (never used except in tests)"""
        return (other.name == self.name) and (other.sign == self.sign)

    def __ne__(self, other):
        """Test literal inequality"""
        return not self.__eq__(other)

    def __hash__(self):
        """Used for set operations"""
        return hash(self.name) ^ hash(self.sign)

    def opposite(self, other):
        """true if one literal is the negation of the other"""
        return (other.name == self.name) and (other.sign == (not self.sign))

    def code_name(self):
        """Return a string representing the literal"""
        return self.name if self.sign else '_' + self.name

    def __str__(self):
        return self.name if self.sign else 'not ' + self.name

    def __repr__(self):
        return str(self)


class CLDynSys(object):
    """Class to describe a dynamic system in clause form.

    :param symb_tab: Symbol table of charter model produced by Table_visitor
        Dict of entities names as keys, and states as values.
        States are described like: (type, deepness); where deepness if the
        imbrication level of macro states (Cf Table_visitor).

        All keys = no_frontiers + frontiers + model name
        (probably a bug for this last one)

        /!\ Should not be used after adding the clauses by GT2Clauses (?)

        :Examples::

            {'PGK_cGMP_active': ('state', 0), ...}
            {'input_place': ('input', 0), ...}
            {'A': ('state', 0), ...}

        :Completed by MCLTranslator with add_free_clock()::

            {"_h_0000": ('clock', -1)}

    :param report: Reporter for error reporting.
    :param base_var_set: Set of ALL variables of the dynamic system
        (including inputs, entities, clocks/events, auxiliary variables)
    :param clauses: Clauses
        Added from MCLTranslator.
    :param aux_clauses: Auxiliary clauses.
        Added from MCLTranslator.
    :param frontiers: All frontiers of the model.
        Used by CLUnfolder.
        Added from MCLTranslator.
        Cf GT2Clauses.visit_csimple_node()
    :param no_frontiers: Places that are not frontiers.
        Added from MCLTranslator.
        Cf GT2Clauses.visit_csimple_node()
    :param free_clocks: Free clocks names inputs.
        Added from MCLTranslator.
    :param place_clocks: Dictionary of clocks as keys and places as values.
        Association between a clock and an inductive place:
        `clock h -> [place P, ...]` where P is a place preceding free clock h.

        :Example::

            {"_h_2772": ["BTG2_gene", ...]}

    :param inputs: Other inputs
    :param lit_compt: Incrementable id for auxiliary variables naming.

    :type symb_tab: <dict <str>: <tuple <str>, <int>>>
    :type report: <Reporter>
    :type base_var_set: <set <str>>
    :type clauses: <list <Clause>>
    :type aux_clauses: <list <Clause>>
    :type frontiers: <list <str>>
    :type no_frontiers: <list <str>>
    :type free_clocks: <list <str>>
    :type place_clocks: <defaultdict <list>>
    :type inputs: <list <str>>
    :type lit_compt: <int>

    The frontiers, free_clocks, place_clocks lists are used for extraction of
    informations from solutions.
    The place_clocks list is used for generating the structural constraints
    OR(place P and clock h) implying that at least one clock transition must
    be activated at each step.

    Additional information about attributes:

        Model Entities: Their names are preserved from the model.
            Added to base_var_set
        Auxiliary variables: They are named by adding a value incremented at their end.
            Added to base_var_set
            Ex: `"_lit00000"`
        Free clock variables: Their names are preserved from the model.
            Added to base_var_set
            Added to free_clocks
            Added to the dict symb_tab: Ex: `{"_h_0000": ('clock', -1)}`
        Place clocks:
            Added to place_clocks::
            Ex: `{"_h_2772": ["BTG2_gene", ...]}`
        Input variables: Their names are "supposed to be" preserved from the model.
            Added to base_var_set
            Added to inputs (May be added multiple times ?)
        Clauses:
            Added to clauses
        Auxiliary clauses:
            Added to aux_clauses
    """
    def __init__(self, symb_tab, report):
        # symbol table of charter model produced by Table_visitor
        # completed by add_free_clock
        self.symb_tab = symb_tab
        self.report = report           # reporter for errors
        # Set of ALL variables of the dynamic system (including auxiliary ones).
        self.base_var_set = set()
        self.clauses = []              # clause form of the dynamic
        # structural constraints valid if there is no timing constraints
        self.aux_clauses = []
        self.frontiers = []            # frontiers places of the model
        self.no_frontiers = []         # Places that are not frontiers

        self.free_clocks = []          # free clocks inputs
        # dictionary of clocks as keys and places as values
        # association between a clock and an inductive place
        # clock h -> [place P, ...] where P is a place preceding free clock h
        self.place_clocks = defaultdict(list)
        self.inputs = []               # other inputs

        self.lit_compt = 0             # for auxiliary variables generation

    def add_var(self, name):
        """Add a logical variable to the dynamic system

        All entities of the model are added here

        :param name: the name of the variable (string)
        """
        if name in self.base_var_set:
            return
        self.base_var_set.add(name)

    def add_aux_var(self):
        """create an auxiliary variable for compiler purpose

        Auxiliary variables are named by adding a value incremented at their end
            ex: "_lit00000"
        """
        name = '_lit' + str(self.lit_compt)
        self.lit_compt += 1
        self.base_var_set.add(name)
        return name

    def add_free_clock(self, hname):
        """add a free clock variable

        :param hname: the name of the clock variable (string)
            Free clocks are associated to the value ('clock', -1) in self.symb_tab

            :Example::

                {"_h_0000": ('clock', -1)}

        """
        if hname in self.base_var_set:
            return
        self.base_var_set.add(hname)
        self.free_clocks.append(hname)
        self.symb_tab[hname] = ('clock', -1)

    def add_place_clock(self, pname, hname):
        """
        add an association hname --> pname between a clock and an inductive place
        """
        self.place_clocks[hname].append(pname)

    def add_input(self, name):
        """add a variable representing an input
        @param name: name of the input
        """
        if not name in self.base_var_set:
            self.base_var_set.add(name)
        self.inputs.append(name) # May be added multiple times ?

    def add_clause(self, clause):
        """add a clause constraint

        PS: How to debug a clause::

            cla_str = str(clause)
            if "_h_0" in cla_str or "A" in cla_str: print(cla_str)
        """
        #TODO: do not add satisfied clauses (n or not n)
        self.clauses.append(clause)

    def add_aux_clause(self, clause):
        """add an auxiliary clause constraint"""
        self.aux_clauses.append(clause)

    def get_var_number(self):
        """Get the number of ALL variables of the dynamic system
        (including inputs, entities, clocks/events, auxiliary variables)
        """
        return len(self.base_var_set)

