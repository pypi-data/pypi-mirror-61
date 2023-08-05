# -*- coding: utf-8 -*-
## Filename    : MCLAnalyser.py
## Author(s)   : Michel Le Borgne
## Created     : 03/2012
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
Main class to perform dynamic analysis of Cadbiom chart models.

Discrete event system simulation is a standard simulation scheme which consists
in the repetition of the following actions until some halting condition
is satisfied:

    - Find the current events and inputs (including free events)
    - Find the state variables subject to change
    - Perform the state evolution

## Here you will find a global view of the process of dynamic analysis

mac_search:
    Wrapper for __mac_exhaustive_search()
    Return a generator of FrontierSolution objects.

__mac_exhaustive_search:
    Return a generator of FrontierSolution objects.

    Test if the given query is satisfiable according the given maximum number of steps.
    Get the minimum of steps that are mandatory to reach the final property in the query.

    This task is made with: `sq_is_satisfiable(query, max_user_step)`
    Which call internal functions of the unfolder (this is beyond the scope of this doc)

        - Initialisation: `self.unfolder.init_with_query(query)`
        - Ultimate test: `self.unfolder.squery_is_satisfied(max_step)`

    Adjust the attribute `steps_before_check` of the query, this is the number of
    useless shifts that are needed by the unfolder before finding a solution.

    Reload in the query a list of frontiers values that constitute each solution
    previously found.
    These values are in DIMACS format (i.e, numerical values). Since we doesn't
    want further similar solutions, each value has a negative sign
    (which which means that a value is prohibited).


    On banni les solutions précédemment trouvées. Une solution est apparentée à
    un ensemble de places frontières;
    Notons qu'il n'y a pas de contraintes sur les trajectoires ayant permis
    d'obtenir un ensemble de places frontières.

    Pour bannir les solutions 2 choix se présentent:
        - Soit les joindre par des "and" logiques et contraindre chaque solution
          par un "non".
          Ex: Pour 2 solutions `[(A, B), (B, C)]`: `not((A and B) or (B and C))`

        - Soit conserver les valeurs de chaque ensemble de places frontière sous
          forme de clauses constituées de valeurs numériques.
          Ex: Pour 2 solutions `[(A, B), (B, C)]`: `[[-1, -2], [-2, -3]]`

    La deuxième solution est nettement plus performante car elle permet de
    s'affranchir du travail de parsing réalisé par l'intervention d'une grammaire,
    des propriétés de plus en plus complexes au fur et à mesure des solutions
    trouvées.

    Ainsi, chaque nouvelle requête se voit recevoir dans son attribut dim_start,
    l'ensemble des solutions précédentes, bannies, au format DIMACS.


    On cherche ensuite d'abord des solutions non minimales (actuellement 2) via:
    `self.__sq_dimacs_frontier_solutions(query, nb_step, 2)`

    Pour ensuite les élaguer en supprimant les places non essentielles à la
    satisfiabilité de la propriété via:
    `small_fsol = self.less_activated_solution(lfsol)`
    `current_mac = self.__prune_frontier_solution(small_sol, query, nb_step)`

    Ce processus itératif est le plus "time-consuming" car nous n'avons pas
    le controle sur les solutions fournies par SAT et les solutions non minimales
    sont en général très éloignées de la solution minimale, c.-à-d. contiennent
    beaucoup plus de places (ces places excédentaires sont dispensables).


next_mac(self, query, max_step):
    Search a Minimal Access Condition for the given query.

    This is a function very similar to `__mac_exhaustive_search()`, but it
    returns only 1 solution.
    Satisfiability tests and the banishment of previous solutions must be done
    before the call.

---

## Back on the few mentioned functions and their call dependencies:

less_activated_solution(self, dimacs_solution_list):
    Get the solution with the less number of activated frontier places among the given solutions.

__prune_frontier_solution(self, fsol, query, max_step):
    Take a frontier condition which induces a property "prop" and try to
    reduce the number of activated frontier variables from this solution while
    inducing "prop".

    Find at most `nb_sols_to_be_pruned` frontier solutions inducing
    the same final property but with all inactivated frontier places
    forced to be initially False.

    Repeat the operation until there is only one solution.

    Return <DimacsFrontierSol>

    This functions calls __solve_with_inact_fsolution().

__solve_with_inact_fsolution(self, dimacs_front_sol, query, max_step, max_sol):
    Frontier states not activated in dimacs_front_sol (DimacsFrontierSol)
    are **forced to be False at start**; solve this and return DimacsFrontierSol
    objects matching this constraint (their number is defined with the
    argument `max_sols`)
    Return <tuple <DimacsFrontierSol>>

    This function calls __sq_dimacs_frontier_solutions().

__sq_dimacs_frontier_solutions(self, query, max_step, max_sol)
    Search set of minimal solutions for the given query, with a maximum of steps
    Tuple of unique DimacsFrontierSol objects built from RawSolutions
    from the solver.
    Return <tuple <DimacsFrontierSol>>

    This function calls sq_solutions().

sq_solutions(query, max_step, max_sol, vvars)
    This function is the lowest level function exploiting the solver results.
    Return <list <RawSolution>>

    This function calls:
        self.unfolder.init_with_query(query, check_query=False)
        self.unfolder.squery_solve(vvars, max_step, max_sol)


## Quiet deprecated but still used in the GUI:

sq_frontier_solutions(self, query, max_step, max_sol):
    This function is a wrapper of sq_solutions().
    Return <list <FrontierSolution>>
"""
from __future__ import print_function

from antlr3 import ANTLRFileStream, CommonTokenStream

from cadbiom.models.guard_transitions.translators.chart_xml import \
        MakeModelFromXmlFile

from cadbiom.models.guard_transitions.translators.chart_xml_pid import \
        MakeModelFromPidFile

from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.clause_constraints.mcl.MCLTranslators import GT2Clauses
from cadbiom.models.clause_constraints.mcl.CLUnfolder import CLUnfolder
from cadbiom.models.clause_constraints.mcl.MCLSolutions import MCLException

from cadbiom.models.clause_constraints.CLDynSys import CLDynSys
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.clause_constraints.mcl.MCLSolutions import (
    FrontierSolution,
    DimacsFrontierSol,
)
from cadbiom.models.clause_constraints.mcl.MCLQuery import MCLSimpleQuery
from cadbiom import commons as cm

# Standard imports
from logging import DEBUG, INFO

LOGGER = cm.logger()


class MCLAnalyser(object):
    """Query a dynamical system and analyse the solutions

    When loading a model in a MCLAnalyser object, a CLUnfolder is generated which
    implies the compilation of the dynamical system into a clause constraint
    dynamical system and the DIMACS coding of all the variables.
    This coding cannot be changed later.
    The unfolding of constraints is performed efficiently on the numeric form
    of the clause constraints. The CLUnfolder provide various method to convert
    variable names to DIMACS code and back, to extract the frontier of a model
    and to extract informations from raw solutions.

    Attributes and default values:

        :param dynamic_system: dynamical system in clause constraint form
        :param unfolder: computation management: unfolding
        :param reporter: reporter for generic error display
        :param translator_opti: turn on optimizations for ANTLR translation
            (subexpression elimination)
        :param nb_sols_to_be_pruned: For mac search: We search a number of
            solutions that will be pruned later, in order to find the most
            optimized MAC with a reduced the number of activated frontiers.
        :key debug: (optional) Used to activate debug mode in the Unfolder

        :type dynamic_system: None before loading a model / <CLDynSys>
        :type unfolder: None before loading a model / <CLUnfolder>
        :type debug: False / <boolean>
        :type reporter: <ErrorRep>
        :type translator_opti: True / <boolean>
        :type nb_sols_to_be_pruned: 10
    """

    def __init__(self, report, debug=False):
        """The built analyser is void by default

        @param report: a standard reporter
        """
        self.debug = debug
        self.unfolder = None
        self.reporter = report
        self.translator_opti = True

        # For mac search: We search a number of solutions that will be pruned
        # in order to find the most optimized MAC with a reduced the number of
        # activated frontiers.
        ## TODO: ajuster ce paramètre dynamiquement
        self.nb_sols_to_be_pruned = 10

    @property
    def dynamic_system(self):
        """Return the CLDynSys object of the current unfolder"""
        return self.unfolder.dynamic_system

    ## Building MCLAnalyser ####################################################

    def build_from_chart_model(self, model):
        """Build an MCLAnalyser and its CLUnfolder from a chartmodel object.

        Every parser uses this function at the end.

        @param model: <ChartModel>
        """
        # Reloading a MCLAnalyser is forbidden - create a new one is mandatory
        if self.unfolder:
            raise MCLException("This MCLAnalyser is already initialized")

        # Build CLDynSys (dynamical system in clause constraint form)
        # Parse the model data
        vtab = TableVisitor(self.reporter)
        model.accept(vtab)
        if self.reporter.error:
            return
        # PS:
        # Here, all keys of vtab.tab_symb = no_frontiers + frontiers + model name
        # (probably a bug for this last one)
        dynamic_system = CLDynSys(vtab.tab_symb, self.reporter)
        if self.reporter.error:
            return
        # Build clauses and auxiliary variables from events and places in the model
        comp_visitor = GT2Clauses(dynamic_system, self.reporter, self.translator_opti)
        model.accept(comp_visitor)
        if self.reporter.error:
            return
        # Build unfolder
        self.unfolder = CLUnfolder(dynamic_system, debug=self.debug)

    def build_from_chart_file(self, file_name):
        """Build an MCLAnalyser from a .bcx file

        @param file_name: str - path of the .bcx file
        """
        parsing = MakeModelFromXmlFile(file_name)
        # chart model
        self.build_from_chart_model(parsing.model)

    def build_from_pid_file(self, file_name, has_clock=True, ai_interpretation=0):
        """Build an MCLAnalyser from a .xml file of PID database

        @param file_name: str - path of .xml file
        """
        parsing = MakeModelFromPidFile(
            file_name, self.reporter, has_clock, ai_interpretation
        )
        # chart model
        self.build_from_chart_model(parsing.model)

    def build_from_cadlang(self, file_name):
        """Build an MCLAnalyser from a .cal, Cadlang file

        @param file_name: str - path of .cal file
        """
        creporter = self.reporter
        fstream = ANTLRFileStream(file_name)
        lexer = cadlangLexer(fstream)
        lexer.set_error_reporter(creporter)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(creporter)
        model = ChartModel(file_name)
        parser.cad_model(model)
        # chart model
        self.build_from_chart_model(parser.model)

    ## Solutions processing ####################################################

    def less_activated_solution(self, dimacs_solution_list):
        """Get the solution with the less number of activated frontier places
        among the given solutions.

        .. note:: There is not constraint on the complexity of the trajectories;
            only on the number of activated frontier places.

        :param dimacs_solution_list: list of DimacsFrontierSol objects
        :return: 1 DimacsFrontierSol with the less number of activated states.
        :type dimacs_solution_list: <tuple <DimacsFrontierSol>>
        :rtype: <DimacsFrontierSol>
        """
        # Count the number of activated places in each solution
        activated_per_sol = [sol.nb_activated_frontiers for sol in dimacs_solution_list]
        return dimacs_solution_list[activated_per_sol.index(min(activated_per_sol))]

    def __solve_with_inact_fsolution(self, dimacs_front_sol, query, max_step, max_sol):
        """Frontier states not activated in dimacs_front_sol (DimacsFrontierSol)
        are **forced to be False at start**; solve this and return DimacsFrontierSol
        objects matching this constraint (their number is defined with the
        argument `max_sol`).

        :param dimacs_front_sol: A solution to obtain the property.
        :param query: Current query
        :param max_step: Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :param max_sol: Number of wanted solutions.
        :return: DimacsFrontierSol objects matching the constraint of
            useless inactivated frontier places.
        :type dimacs_front_sol: <DimacsFrontierSol>
        :type query: <MCLSimpleQuery>
        :type max_step: <int>
        :type max_sol: <int>
        :return: <tuple <DimacsFrontierSol>>
        :precondition: dimacs_front_sol is a frontier solution for the query
        """
        # Collect inactivated frontier places
        # OLD:
        # inactive_frontier_values = \
        #     [[var] for var in dimacs_front_sol.frontier_values if var < 0]
        # Intersection between pre-computed negative values for all frontiers
        # (negative and positive) in the given solution, and all frontiers.
        inactive_frontier_values = [
            [var]
            for var in self.unfolder.frontiers_negative_values
            & dimacs_front_sol.frontier_values
        ]

        # Append inactivated frontier places as a start property in DIMACS form
        # PS: do not test dim_start: In the worse case, it's an empty list.
        query.dim_start += inactive_frontier_values

        # Must return fsol even if there is no more solution (search first 10 sols)
        # Get <tuple <DimacsFrontierSol>>
        return self.__sq_dimacs_frontier_solutions(query, max_step, max_sol)

    def __prune_frontier_solution(self, fsol, query, max_step):
        """"Take a frontier condition which induces a property "prop" and try to
        reduce the number of activated frontier variables from this solution while
        inducing "prop".

        Find at most `nb_sols_to_be_pruned` frontier solutions inducing
        the same final property but with all inactivated frontier places
        forced to be initially False.

        Repeat the operation until there is only one solution.

        :param fsol: A DimacsFrontierSol for which we assume/assert that the
            system is satisfiable.
        :type fsol: <DimacsFrontierSol>
        :type query: <MCLSimpleQuery>
        :rtype: <DimacsFrontierSol>

        .. todo::
            - regarder si les solutions dimacs_solutions sont si différentes.
            il est possible que le solveur soit relativement optimisé pour qu'on
            puisse en demander moins ou qu'on puisse éliminer les solutions les
            moins diversifiées (détection d'un ensemble commun de places dont on
            forcerait l'inactivation pas l'intermédiaire d'une clause de l'état
            initial).
            - ajuster automatiquement nb_sols_to_be_pruned (10 actuellement)
        """
        # for debug - too expansive to be activated anytime
        # assert(self.sq_is_satisfiable(query, max_step))
        sol_to_prune = fsol
        # Number of activated places in solution
        # We are trying to reduce this number
        current_len = fsol.nb_activated_frontiers
        next_len = 0
        is_pruned = True

        i = 0
        while is_pruned:
            i += 1
            # find at most nb_sols_to_be_pruned frontier solutions inducing
            # the same final property but with all inactivated frontier places
            # forced to be initially False.
            # return sol_to_prune if no more solution

            # PS: We need to index the result in less_activated_solution
            # thus, this why __solve_with_inact_fsolution() returns a tuple.
            dimacs_solutions = self.__solve_with_inact_fsolution(
                sol_to_prune, query, max_step, self.nb_sols_to_be_pruned
            )

            LOGGER.info(
                "MCLA::Prune: Iteration %s, nb pruned inact solutions: %s",
                i,
                len(dimacs_solutions),
            )

            # PS: dimacs_solutions should never be None or empty
            if len(dimacs_solutions) == 1:
                # No new solution has been found,
                # the current solution is the best (sol_to_prune)
                return dimacs_solutions[0]  # it's sol_to_prune variable

            # Seach for less activated solution
            # Get the solution with the less number of activated states
            next_sol = self.less_activated_solution(dimacs_solutions)
            next_len = next_sol.nb_activated_frontiers
            is_pruned = current_len > next_len

            LOGGER.info(
                "MCLA::Prune: Current solution activated length:%s next:%s",
                current_len, next_len
            )

            if is_pruned:
                sol_to_prune = next_sol
                current_len = next_len

        # never reach this point
        raise MCLException("MCLAnalyser:__prune_frontier_solution:: what happened?")

    ## Generic solver for simple queries #######################################

    def sq_is_satisfiable(self, query, max_step):
        """Check if the query is satisfiable.

        .. warning::
            Many logical variables are auxiliary variables with no interest other
            than technical, we want different solutions to differ by their values
            on some set of significant variables.

            **These variables of interest are not checked here!**
                It is just a satisfiability test!

        .. warning:: No frontier place is initialized to False in simple queries.

        :param query:
        :param max_step: Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :type query: <MCLSimpleQuery>
        :type max_step: <int>
        :rtype: <boolean>
        """
        # Initialise the unfolder with the given query
        # Following properties are used from the query:
        #    start_prop, dim_start, inv_prop, dim_inv, final_prop, dim_final,
        #    variant_prop, dim_variant, steps_before_check
        self.unfolder.init_with_query(query, check_query=False)
        # go
        return self.unfolder.squery_is_satisfied(max_step)

    def sq_solutions(self, query, max_step, max_sol, vvars, max_user_step=None):
        """Return a list of RawSolution objects

        This function is the lowest level function exploiting the solver results.

        Parameters are the same as in sq_is_satisfiable() except for vvars
        parameter which deserves some explanations.

        The solver doesn’t provide all solutions of the set of logical constraints
        encoding the temporal property. It gives only a sample of these solutions
        limited in number by the max_sol parameter. **Since many logical variables
        are auxiliary variables with no interest other than technical, we want
        different solutions to differ by their values on some set of significant
        variables. That is the meaning of the vvars parameter.**

        Remark that the variables of interest must be specified in DIMACS code.
        Most of the time, this method is used internally, so DIMACS code is
        transparent to the user.

        The class RawSolution provides a representation of solutions which are
        raw results from the SAT solver with all variable parameters from the
        unfolder, and consequently not easily readable.
        In addition to the solution in DIMACS form (including values for auxiliary
        variables), a RawSolution object registers data which permit information
        extraction from these raw solutions. The most important methods are:

            - frontier_pos_and_neg_values:
                Which extracts the frontier values from the solution.
                These values are in DIMACS code.

            - extract_activated_frontier_values():
                Extracts frontier variables which are active in solution.

            - extract_act_input_clock_seq():
                Extract the sequence of activated inputs and events in the solution.


        In models of signal propagation, we are more interested in frontier solutions.
        The following method is then well adapted: sq_frontier_solutions(),
        because it returns FrontierSolutions.


        :param query: Query.
        :param max_step: Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :param vvars: Variables for which solutions must differ.
            In practice, it is a list with the values (Dimacs code)
            of all frontier places of the system.
        :key max_user_step: (Optional) See :meth:`__mac_exhaustive_search`.
        :type query: <MCLSimpleQuery>
        :type max_step: <int>
        :type vvars: <list <int>>
        :type max_user_step: <int>
        :return: a list of RawSolutions from the solver
        :rtype: <list <RawSolution>>

        .. warning:: no_frontier places are initialized to False in simple queries
            except if initial condition.

        .. warning:: if the query includes variant constraints,
            the horizon (max_step) is automatically adjusted to
            min(max_step, len(variant_constraints)).
        """
        # Initialise the unfolder with the given query
        # Following properties are used from the query:
        #    start_prop, dim_start, inv_prop, dim_inv, final_prop, dim_final,
        #    variant_prop, dim_variant, steps_before_check
        self.unfolder.init_with_query(query, check_query=False)
        # go
        return self.unfolder.squery_solve(
            vvars, max_step, max_sol, max_user_step=max_user_step
        )

    def sq_frontier_solutions(self, query, max_step, max_sol):
        """Compute active frontier places and timings

        Compute the set of frontier place names which must be activated for
        implying query satisfaction and returned it as a list of `FrontierSolution`.

        Quiet deprecated but referenced by:

            - `gt_gui/chart_checker/chart_checker_controler`
            - `cadbiom_cmd/solution_search.py` very old code for debug purpose
              :meth:`mac_inhibitor_search`

        In models of signal propagation, we are more interested in frontier solutions.
        So the current method is better adapted than :meth:`sq_solutions`
        which returns `RawSolutions`.

        This function is a wrapper of :meth:`sq_solutions`.


        The class `FrontierSolution` provides objects wrapping a symbolic
        representation of frontier values and timing from a raw solution.

            - The main attributes are activated_frontier which is a set of
              (string) names of frontier places which are activated in the solution.

            - The second important attribute is ic_sequence, a list of strings
              which describes the successive activated inputs and free events in
              the solution.

        If events h2, h5 and input in3 are activated at step k in the solution,
        then the kth element of the list is “% h2 h5 in3”.
        This format is understood by the Cadbiom simulator.

        .. warning:: no frontier places are initialized to False

        :param query: Query
        :param max_step: int - Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :param max_sol: max number of wanted solutions.
        :type query: MCLSimpleQuery
        :type max_step: <int>
        :type max_sol: <int>
        :return: List of FrontierSolutions built from RawSolutions from the solver.
            So, lists of lists of frontier place names which must be activated
            for implying query satisfaction.
        :rtype: <list <FrontierSolution>>
        """
        vvars = self.unfolder.frontier_values
        # sq_solutions() returns <list <RawSolution>>
        # We transtype them to FrontierSolution
        return [FrontierSolution.from_raw(sol) for sol
                in self.sq_solutions(query, max_step, max_sol, vvars)]


    def __sq_dimacs_frontier_solutions(self, query, max_step, max_sol, max_user_step=None):
        """Search set of minimal solutions for the given query, with a maximum of steps

        DimacsFrontierSol objects provides some interesting attributes like:
        activated_frontier_values (raw values of literals).
        Note: FrontierSolution are of higher level without such attributes.

        :param query: Query
        :param max_step: Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :param max_sol: Max number of solutions for each solve
        :key max_user_step: (Optional) See :meth:`__mac_exhaustive_search`
        :type query: <MCLSimpleQuery>
        :type max_step: <int>
        :type max_sol: <int>
        :type max_user_step: <int>
        :return: Tuple of unique DimacsFrontierSol objects built from RawSolutions
            from the solver.
            .. note:: Unicity is based on the set of activated frontier values.
        :rtype: <tuple <DimacsFrontierSol>>
        """
        vvars = self.unfolder.frontier_values
        # sq_solutions() returns <list <RawSolution>>
        raw_sols = self.sq_solutions(
            query, max_step, max_sol, vvars, max_user_step=max_user_step
        )
        # Get unique DimacsFrontierSol objects from RawSolution objects
        dimacfrontsol = DimacsFrontierSol.get_unique_dimacs_front_sols_from_raw_sols(raw_sols)

        if LOGGER.getEffectiveLevel() == INFO:
            LOGGER.info(
                "MCLA: Nb queried: %s, steps: %s\n"
                "\tget: %s, unique: %s\n"
                "\tactivated fronts per dimacfrontsol: %s",
                max_sol, self.unfolder.current_step,
                len(raw_sols), len(dimacfrontsol),
                [len(sol) for sol in dimacfrontsol]
            )
        return dimacfrontsol

    def __mac_exhaustive_search(self, query, max_user_step):
        """Return a generator of FrontierSolution objects.

        This is a function very similar to next_mac(), but it returns
        many solutions.
        The satisfiability tests and the banishment of the previous solutions
        are done internally in an optimal way.
        There is also a self adjustment of the number of minimum steps during
        which to find solutions until reaching the maximum number set by the user.

        ---

        On cherche ensuite d'abord des solutions non minimales (actuellement 2) via:
        self.__sq_dimacs_frontier_solutions(query, nb_step, 2)

        Pour ensuite les élaguer en supprimant les places non essentielles à la
        satisfiabilité de la propriété via:
        small_fsol = self.less_activated_solution(lfsol)
        current_mac = self.__prune_frontier_solution(small_sol, query, nb_step)

        Ce processus itératif est le plus "time-consuming" car nous n'avons pas
        le controle sur les solutions fournies par SAT et les solutions non minimales
        sont en général très éloignées de la solution minimale, c.-à-d. contiennent
        beaucoup plus de places (ces places excédentaires sont dispensables).

        :param query: Current query.
        :param max_user_step: Number of steps allowed by the user in the unfolding;
            the horizon on which the properties must be satisfied.
            This argument is also used to auto-adjust max_step for an extra step
            in CLUnfolder.
            .. seealso:: :meth:`cadbiom.models.clause_constraints.mcl.CLUnfolder.squery_solve`
        :type query: <MCLSimpleQuery>
        :type max_user_step: <int>
        :return: A generator of FrontierSolution objects which are a wrapper of
            a symbolic representation of frontier values and timings from
            a raw solution.
        :rtype: <generator <FrontierSolution>>
        """
        # list of timed minimal activation conditions on frontier (dimacs code)
        # i.e list<DimacsFrontierSol>
        # mac_list = [] # Not used anymore

        # Keep a list of frontier values to be banned in the next search
        forbidden_frontier_values = query.dim_start

        # Satisfiability test
        reachable = self.sq_is_satisfiable(query, max_user_step)

        # Get the minimum number of steps for reachability
        min_step = self.unfolder.current_step
        # Adjust the number of useless shifts needed before finding a solution
        # (i.e. testing final prop).
        # __steps_before_check can't be >= max_user_step
        # (see squery_is_satisfied() and squery_solve())
        query.steps_before_check = min_step - 1

        while reachable:
            LOGGER.info("Solution reachable in min_step: %s", min_step)

            # Forbidden solutions: already discovered macs
            # (see at the end of the current loop).
            # Ban all sets of activated frontiers (1 set = 1 solution)
            # Equivalent of wrapping each previous solution with a logical AND:
            # AND(not(frontier places))
            query.dim_start = list(forbidden_frontier_values)

            #### redondance partielle avec next_mac()
            # Solutions differ on frontiers: Search only 2 different solutions
            # to avoid all activated solutions
            # Get <tuple <DimacsFrontierSol>>
            dimacs_front_sol = self.__sq_dimacs_frontier_solutions(
                query, min_step, 2, max_user_step=max_user_step
            )

            # Self-adjustment of min_step/max_step may have taken place;
            # resynchronization of values:
            # __steps_before_check can't be >= min_step
            # (see squery_is_satisfied() and squery_solve())
            # __steps_before_check should be min_step - 1 to avoid a maximum of
            # useless checks from (min_step to current_step).
            min_step = self.unfolder.current_step
            query.steps_before_check = min_step - 1

            if not dimacs_front_sol:
                # No more solution
                # Note that self-adjust steps is made via max_user_step
                # argument of CLUnfolder.squery_solve

                LOGGER.info(
                    "MCLA:__mac_exhaustive_search: No more solution; current step %s",
                    self.unfolder.current_step,
                )

                assert self.unfolder.current_step == max_user_step
                # just break the loop
                break

            # Get the solution with the less number of activated states
            small_fsol = self.less_activated_solution(dimacs_front_sol)

            # Prune non essential places for the satisfiability of the property
            # => reduce the number of activated variables
            current_mac = self.__prune_frontier_solution(small_fsol, query, min_step)

            yield current_mac
            # mac_list.append(current_mac)

            # Keep a list of frontier values to be banned in the next search
            # - Get all activated frontiers on the current DimacsFrontierSol
            # - Build a list of their opposite values
            forbidden_frontier_values.append(
                [-var for var in current_mac.activated_frontier_values]
            )
            LOGGER.debug(
                "MCLA::mac_exhaustive_search: forbidden frontiers: %s",
                forbidden_frontier_values,
            )

    def next_mac(self, query, max_step):
        """Search a Minimal Access Condition for the given query.

        This is a function very similar to __mac_exhaustive_search(), but it
        returns only 1 solution.
        Satisfiability tests and the banishment of previous solutions must be
        done before the call.

        ---

        On cherche ensuite d'abord des solutions non minimales (actuellement 2) via:
        self.__sq_dimacs_frontier_solutions(query, nb_step, 2)

        Pour ensuite les élaguer en supprimant les places non essentielles à la
        satisfiabilité de la propriété via:
        small_fsol = self.less_activated_solution(lfsol)
        current_mac = self.__prune_frontier_solution(small_sol, query, nb_step)

        Ce processus itératif est le plus "time-consuming" car nous n'avons pas
        le controle sur les solutions fournies par SAT et les solutions non minimales
        sont en général très éloignées de la solution minimale, c.-à-d. contiennent
        beaucoup plus de places (ces places excédentaires sont dispensables).

        :param max_step: Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :type query: <MCLSimpleQuery>
        :type max_step: <int>
        :return: A FrontierSolution which is a wrapper of a symbolic
            representation of frontier values and timings from a raw solution.
        :rtype: <FrontierSolution> - <list <str>>
        """
        # Solutions differ on frontiers: Search only 2 different solutions
        # to avoid all activated solutions
        # Get <tuple <DimacsFrontierSol>>
        lfsol = self.__sq_dimacs_frontier_solutions(query, max_step, 2)
        if not lfsol:
            return

        # Get the solution with the less number of activated states
        small_fsol = self.less_activated_solution(lfsol)

        # Prune non essential places for the satisfiability of the property
        # => reduce the number of activated variables
        current_mac = self.__prune_frontier_solution(small_fsol, query, max_step)

        return FrontierSolution.from_dimacs_front_sol(current_mac)

    def mac_search(self, query, max_step):
        """Wrapper for __mac_exhaustive_search(); return a generator of
        FrontierSolution objects.

        .. note:: __mac_exhaustive_search() returns DimacsFrontierSols

        :param query: MCLSimpleQuery
        :param max_step: int - Number of steps allowed in the unfolding;
            the horizon on which the properties must be satisfied
        :return: <generator <FrontierSolution>>
        """
        ## TODO: convert start_property in dim_start !! => eviter la recompilation des propriétés
        # Get <generator <DimacsFrontierSol>>
        mac_list = self.__mac_exhaustive_search(query, max_step)
        # Convert to a generator of FrontierSolution objects
        #return tuple(FrontierSolution.from_dimacs_front_sol(mac) for mac in mac_list)
        for mac in mac_list:
            yield FrontierSolution.from_dimacs_front_sol(mac)

    ## Inhibitors ##############################################################

    def is_strong_activator(self, act_sol, query):
        """Test if an activation condition is a strong one (independent of timing)

        .. refactor note: Unclear function

        final property becomes the invariant property
        => Ex: test if "C3 and C4" will never append if start property is "A1 and C1 and B1"
        Cf TestMCLAnalyser...

        @return: False if the problem is satisfiable, True otherwise
        @param act_sol: FrontierSolution with activation condition
        @param query: the query used for act_sol condition
        """
        max_step = len(act_sol.ic_sequence) - 1
        print("max steps:", max_step)

        # Same timings, force inactivated frontiers
        query_1 = MCLSimpleQuery.from_frontier_sol_same_timing(act_sol, self.unfolder)

        inv_prop = 'not(' + query.final_prop + ')'
        #(None, None, 'A1 and C1 and B1', ['', 'h2', '', ''])
        print("naive query1:", query_1.final_prop, query_1.inv_prop,
              query_1.start_prop, query_1.variant_prop)

        query_2 = MCLSimpleQuery(None, inv_prop, None)
        #(None, 'not(C3 and C4)', None, [])
        print("query 2:", query_2.final_prop, query_2.inv_prop,
              query_2.start_prop, query_2.variant_prop)
        query_1 = query_2.merge(query_1)
        #(None, 'not(C3 and C4)', 'A1 and C1 and B1', ['', 'h2', '', '']
        print("merged query1:", query_1.final_prop, query_1.inv_prop,
              query_1.start_prop, query_1.variant_prop)

        return not(self.sq_is_satisfiable(query_1, max_step))


    def next_inhibitor(self, mac, query):
        """
        .. refactor note: Unclear function

        if st_prop contains negation of mac conditions,
        return a different mac if any
        same parameters as __mac_exhaustive_search
        Used for search on cluster

        @param mac: FrontierSolution
        @param query: MCLSimpleQuery
        @param max_step: int - number of dynamical step
        @return: a list of variables (list<string>)
        """
        # query with mac init frontier places and  timing
        inh_query1 = MCLSimpleQuery.from_frontier_sol_same_timing(mac, self.unfolder)
        # query with negation of final prop as invariant property
        if not query.final_prop:
            raise MCLException("Query must have a final property")
        if not query.inv_prop:
            inv_prop = "not (" + query.final_prop + ")"
        else:
            inv_prop = query.inv_prop + "and (not (" + query.final_prop + "))"
        inh_query2 = MCLSimpleQuery(None, inv_prop, None)
        # init + timing + final property not reachable
        inh_query = inh_query1.merge(inh_query2)
        max_step = len(inh_query.variant_prop)
        assert max_step == len(mac.ic_sequence)

        # search solutions - diseable aux clauses
        self.unfolder.set_include_aux_clauses(False)
        next_inhib = self.next_mac(inh_query, max_step)
        self.unfolder.set_include_aux_clauses(True)
        return next_inhib

    def mac_inhibitor_search(self, mac, query, max_sol):
        """Search inhibitors for a mac scenario

        .. refactor note: Unclear function

        @param mac: the mac
        @param query: the property enforced by the mac
        @param max_sol: limit on the number of solutions
        @param max_sol: maximum number of solutions

        @return: a list of frontier solution
        """
        # query with mac init frontier places and  timing
        inh_query1 = MCLSimpleQuery.from_frontier_sol(mac)
        # query with negation of final prop as invariant property
        if not query.final_prop:
            raise MCLException("Query must have a final property")
        if not query.inv_prop:
            inv_prop = "not (" + query.final_prop + ")"
        else:
            inv_prop = query.inv_prop + "and (not (" + query.final_prop + "))"
        inh_query2 = MCLSimpleQuery(None, inv_prop, None)
        # init + timing + final property not reachable
        inh_query = inh_query1.merge(inh_query2)

        max_step = len(inh_query.variant_prop)
        assert max_step == len(mac.ic_sequence)
        # search solutions - diseable aux clauses
        self.unfolder.set_include_aux_clauses(False)
#        lsol = self.sq_frontier_solutions(inh_query, max_step, max_sol)
        lsol = tuple(self.mac_search(inh_query, max_step))
        self.unfolder.set_include_aux_clauses(True)
        return lsol

    def is_strong_inhibitor(self, in_sol, query):
        """Test if an activation condition inhibitor is a strong one
        (i.e independent of timing)

        .. refactor note: Unclear function

        @param in_sol: FrontierSolution with activation condition and inhibition
        @param query: the property which is inhibed
        """
        max_step = len(in_sol.ic_sequence) - 1

        # New timings, force inactivated frontiers
        query_1 = MCLSimpleQuery.from_frontier_sol_new_timing(in_sol, self.unfolder)
        # negation of the query
        if not query.final_prop:
            raise MCLException("Query must have a final property")
        if not query.inv_prop:
            inv_prop = "not (" + query.final_prop + ")"
        else:
            inv_prop = query.inv_prop + "and (not (" + query.final_prop + "))"
        inh_query = MCLSimpleQuery(None, inv_prop, None)
        query_1 = inh_query.merge(query_1)
        return not self.sq_is_satisfiable(query_1, max_step)
