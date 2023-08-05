# -*- coding: utf-8 -*-
## Filename    : MCLQuery.py
## Author(s)   : Michel Le Borgne
## Created     : 10 sept. 2012
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
## Contributor(s): Geoffroy Andrieux - IRISA/IRSET
##
"""
Query internal representation
"""
from cadbiom.models.clause_constraints.mcl.MCLSolutions import MCLException
from cadbiom import commons as cm
from logging import DEBUG

LOGGER = cm.logger()


class MCLSimpleQuery(object):
    """Class packaging the elements of a query

    Object containing 2 main types of attributes describing properties:

        - Attributes in text format: These are logical formulas that are humanly
          readable.
          Ex: `start_prop, inv_prop, final_prop, variant_prop`
        - Attributes in DIMACS format: These are logical formulas encoded in
          the form of clauses containing numerical values.
          Ex: `dim_start, dim_inv, dim_final, dim_variant`

    Textual properties of query are compiled into numeric clauses in the unfolder
    with init_forward_unfolding(), just at the beginning of squery_is_satisfied()
    and squery_solve().

    Attributes:

        :param start_prop: start property; logical formulas
        :param inv_prop: invariant property; logical formulas
        :param final_prop: final property; logical formulas
        :param variant_prop: list of logical formulas from ic_sequence.
            It's the trajectory of events of a solution.
            :Example::

                ['', 'h2 and h2', '', 'h2']

        :param dim_start: start property in DIMACS form - optional
        :param dim_inv: invariant property in DIMACS form - optional
        :param dim_final: final property in DIMACS form - optional
        :param dim_variant: list of lists of dimacs clauses
            :Example::

                [[[16], [16]], [[22], [22]]]

        :param steps_before_check: Number of shifts before testing the
            final property - optional

        :type start_prop: <str>
        :type inv_prop: <str>
        :type final_prop: <str>
        :type variant_prop: <list <str>>

        :type dim_start: <list <DClause>>, default []
        :type dim_inv: <list <DClause>>, default []
        :type dim_final: <list <DClause>>, default []
        :type dim_variant: <list <list <DClause>>
        :type steps_before_check: <int>, default value 0

    NB: DClause: A clause coded as a list of DIMACS coded literals: <list <int>>

    """

    def __init__(self, start_prop, inv_prop, final_prop, variant_prop=list()):
        """
        .. seealso: The class docstring.
        """
        if LOGGER.getEffectiveLevel() == DEBUG:
            LOGGER.debug(
                "MCLSimpleQuery params:: start prop: "
                + str(start_prop)
                + "; inv prop: "
                + str(inv_prop)
                + "; final prop: "
                + str(final_prop)
            )
        # Strings forms of constraints
        self.start_prop = start_prop      # logical formula or None
        self.inv_prop = inv_prop          # logical formula or None
        self.final_prop = final_prop      # logical formula or None
        self.variant_prop = variant_prop  # list<logical formula>

        # DIMACS forms of the preceding attributes
        self.dim_start = []         # list<DClause>
        self.dim_inv = []           # list<DClause>
        self.dim_final = []         # list<DClause>
        self.dim_variant = []       # list<list<DClause>>

        self.steps_before_check = 0

    @classmethod
    def from_frontier_sol(cls, f_sol):
        """Build a query from a frontier solution

        Start property is based on activated frontiers.

        All frontiers that are not in activated_frontier
        **ARE NOT** forced to be inactivated with a negative value.

        Variant property enforces same timing on activated events,
        and the others are free.

        @param f_sol: FrontierSolution (human readable solution)
        @param unfolder: current unfolder
        """
        # start condition enforce activation of solution places
        start_prop = None
        if f_sol.activated_frontier:
            start_prop = " and ".join(f_sol.activated_frontier)

        # no invariant property
        inv_prop = None

        # no final property
        final_prop = None

        # variant property enforce same timing
        # Each event has a list of steps which it belongs
        # Ex: for steps: ['%', '% h2 h2', '%', '% h2']
        # variant property: ['', 'h2 and h2', '', 'h2']
        print("Reading ic_sequence from FrontierSolution...")

        # - Iterate on steps
        # - Get events names in each step
        # (remove the leading "%" and split the string on spaces)
        # - join events names with a logical operator " and "
        var_prop = [
            " and ".join(raw_step[1:].split()) for raw_step in f_sol.ic_sequence
        ]
        # PS: var_prop and any attribute can be [], but keep this for uniformity
        if not var_prop:
            var_prop = None

        n_query = MCLSimpleQuery(start_prop, inv_prop, final_prop)
        n_query.variant_prop = var_prop
        return n_query

    @classmethod
    def from_frontier_sol_new_timing(cls, f_sol, unfolder):
        """Build a query from a frontier solution

        Start property is based on activated frontiers.

        Search all frontiers that are not in activated_frontier
        and force their inactivation with a negative value.

        **Variant property enforces new timing**

        @param f_sol: FrontierSolution (human readable solution)
        @param unfolder: unfolder
        """
        # activation part of start condition
        start_prop = None
        if f_sol.activated_frontier:
            start_prop = " and ".join(f_sol.activated_frontier)

        # no invariant property
        inv_prop = None

        # no final property
        final_prop = None

        # variant property enforce new timing on activated events
        # Each event has a list of steps which it belongs
        # Ex: for steps: ['%', '% h2 h2', '%', '% h2']
        # variant property: ['', 'not (h2) or not (h2)', '', 'not (h2)']
        print("Reading ic_sequence from FrontierSolution...")

        # - Iterate on steps
        # - Get events names in each step
        # (remove the leading "%" and split the string on spaces)
        # - negation of each event with "not ( event )"
        # - join events names with a logical operator " or "
        var_prop = [
            " or ".join("not (" + icp + ")" for icp in raw_step[1:].split())
            for raw_step in f_sol.ic_sequence
        ]
        # PS: var_prop and any attribute can be [], but keep this for uniformity
        if not var_prop:
            var_prop = None

        # Inactivation of other frontier places at start (DIMACS format)
        # Search all frontiers that are not in activated_frontier
        # and force their inactivation with a negative value.
        ## dim_start doit-il etre ordonné ?
        # 1 - Get negative values of activated frontiers in FrontierSolution object
        activated_frontier_neg_values = {
            -unfolder.var_dimacs_code(name) for name in f_sol.activated_frontier
        }

        # 2 - Get values of inactivated frontiers in the FrontSolution object
        dim_start_values = \
            [[val] for val in unfolder.frontiers_negative_values - activated_frontier_neg_values]


        n_query = MCLSimpleQuery(start_prop, inv_prop, final_prop)
        n_query.variant_prop = var_prop
        n_query.dim_start = dim_start_values
        return n_query

    @classmethod
    def from_frontier_sol_same_timing(cls, f_sol, unfolder):
        """Build a query from a frontier solution

        Start property is based on activated frontiers.

        Search all frontiers that are not in activated_frontier
        and force their inactivation with a negative value.

        **Variant property enforces same timing on activated events,
        and the others are free.**

        @param f_sol: FrontierSolution (human readable solution)
        @param unfolder: current unfolder
        """
        # activation part of start condition
        start_prop = None
        if f_sol.activated_frontier:
            start_prop = " and ".join(f_sol.activated_frontier)

        # no invariant property
        inv_prop = None

        # no final property
        final_prop = None

        # variant property enforce same timing on activated events
        # Each event has a list of steps which it belongs
        # Ex: for steps: ['%', '% h2 h2', '%', '% h2']
        # variant property: ['', 'h2 and h2', '', 'h2']
        print("Reading ic_sequence from FrontierSolution...")

        # - Iterate on steps
        # - Get events names in each step
        # (remove the leading "%" and split the string on spaces)
        # - join events names with a logical operator " and "
        var_prop = [
            " and ".join(raw_step[1:].split()) for raw_step in f_sol.ic_sequence
        ]
        # PS: var_prop and any attribute can be [], but keep this for uniformity
        if not var_prop:
            var_prop = None

        # inactivation of other frontier places at start (DIMACS format)
        # Search all frontiers that are not in activated_frontier
        # and force their inactivation with a negative value.
        # Get negative values of activated frontiers in FrontierSolution object
        activated_frontier_neg_values = {
            -unfolder.var_dimacs_code(name) for name in f_sol.activated_frontier
        }

        # Get list of values of inactivated frontiers in the FrontSolution object
        dim_start_values = \
            [[val] for val in unfolder.frontiers_negative_values - activated_frontier_neg_values]


        n_query = MCLSimpleQuery(start_prop, inv_prop, final_prop)
        # list of logical formulas
        n_query.variant_prop = var_prop
        # start property in DIMACS format
        n_query.dim_start = dim_start_values
        return n_query

    def merge(self, query):
        """Return a new query which is a merge of two queries into one.

        - start, invariant and final properties are merged.
        - If both queries have variant properties, they must be on the same horizon
          (number of steps).
        - steps before reach is set to zero.
        - dim properties are also merged: dim_start, dim_inv, dim_final

        :param query: a MCLSimpleQuery
        :raises: `MCLException` If the queries have variant properties with
            different horizons (nb of steps).
        """
        # merge of start properties
        if not self.start_prop:
            start_prop = query.start_prop
        elif not query.start_prop:
            start_prop = self.start_prop
        else:
            start_prop = "(" + self.start_prop + ") and (" + query.start_prop + ")"
        # merge of invariant properties
        if not self.inv_prop:
            i_prop = query.inv_prop
        elif not query.inv_prop:
            i_prop = self.inv_prop
        else:
            i_prop = "(" + self.inv_prop + ") and (" + query.inv_prop + ")"
        # merge of final properties
        if not self.final_prop:
            final_prop = query.final_prop
        elif not query.final_prop:
            final_prop = self.final_prop
        else:
            final_prop = "(" + self.final_prop + ") and (" + query.final_prop + ")"

        n_query = MCLSimpleQuery(start_prop, i_prop, final_prop)

        # merge of variant prop
        var_prop = None
        if not self.variant_prop:
            var_prop = query.variant_prop
        elif not query.variant_prop:
            var_prop = self.variant_prop
        else:
            ll1 = len(self.variant_prop)
            ll2 = len(query.variant_prop)
            if ll1 != ll2:
                raise MCLException(
                    "Tempting to merge two queries with variant prop of different lengths"
                    "current: {}; other: {}".format(ll1, ll2)
                )
            else:
                var_prop = []
                # 2 empty, 1 empty and not the other, none empty
                for current, other in zip(self.variant_prop, query.variant_prop):
                    if current and other:
                        var_prop.append(current + " and " + other)
                    elif current and not other:
                        var_prop.append(current)
                    elif not current and other:
                        var_prop.append(other)
                    else:
                        var_prop.append("")

        n_query.variant_prop = var_prop

        # merge of dim properties
        n_query.dim_start += query.dim_start
        n_query.dim_inv += query.dim_inv
        n_query.dim_final += query.dim_final
        return n_query

    def __str__(self):
        """Print logical formulas in query"""
        str_out = "Start_property: "
        if self.start_prop:
            str_out += self.start_prop
        str_out += "\nInv property: "
        if self.inv_prop:
            str_out += self.inv_prop
        str_out += "\nFinal property: "
        if self.final_prop:
            str_out += self.final_prop
        str_out += "\nVariant property: "
        if self.variant_prop:
            str_out += str(self.variant_prop)
        return str_out
