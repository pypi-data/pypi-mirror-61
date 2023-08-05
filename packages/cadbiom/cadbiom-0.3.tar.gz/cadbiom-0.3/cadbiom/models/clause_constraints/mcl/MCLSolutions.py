# -*- coding: utf-8 -*-
## Filename    : MCLSolutions.py
## Author(s)   : Michel Le Borgne
## Created     : 03/9/2012
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
"""Classes used to store solver answers.

:class:`RawSolution`:
    Contain a solution got from SAT solver with all variable parameters
    from the unfolder.

:class:`DimacsFrontierSol`:
    A numerical representation of *frontier values and timings* from a raw solution.

:class:`FrontierSolution`:
    Provides is a wrapper for a symbolic
    representation (human readable) of activated frontiers defined in
    RawSolution and DimacsFrontierSol objects.
"""
# Standard imports
from __future__ import print_function
import itertools as it
#from functools import cached_property
from cached_property import cached_property

from cadbiom import commons as cm

# C++ API
from _cadbiom import get_unshift_code, unflatten

LOGGER = cm.logger()


class MCLException(Exception):
    """Exception for MCLAnalyser"""

    def __init__(self, mess):
        self.message = mess

    def __str__(self):
        return self.message

################################################################################

class RawSolution(object):
    """RawSolution objects contain a solution got from SAT solver with all
    variable parameters from the unfolder.

    The class RawSolution provides a representation of solutions which are
    raw results from the SAT solver with all variable parameters from the
    unfolder, and consequently not easily readable.

    In addition to the solution in DIMACS form (including values for auxiliary
    variables), a RawSolution object registers data which permit information
    extraction from these raw solutions. The most important methods/attributes are:

        - frontier_pos_and_neg_values:
            Extracts the frontier values from the solution.
            These values are in DIMACS code.

        - extract_activated_frontier_values():
            Extracts frontier variables which are active in solution.

        - extract_act_input_clock_seq():
            Extract the sequence of activated inputs and events in the solution.

    ..warning:: IMPORTANT: the solution MUST correspond to the properties registered
        for its computation. Any change in these properties will give incorrect
        results (current_step, etc.).

    Attributes:
        :param shift_direction: Unfolding direction
        :param shift_step: The shift step ss (if n is X_0 code, n+ss is X_1 code) (?)
            Dependant on the run.
        :param solution: DIMACS encoding of **a solution** from the solver
            A solution is list of state vectors (tuple of literals).
            Each literal is a variable.
            ..note:: The solver returns list of solutions.
        :param unfolder: Get the current unfolder for the solution
            (unfolder is used for invariant constants)
        :param current_step: Get current step of the unfolder
            (Thus the current number of steps related to the current solution and
            by extension the maximum of steps until now)
        :type shift_direction: "FORWARD" or "BACKWARD"
        :type shift_step: <int>
        :type solution: <tuple <int>>
        :type unfolder: <CLUnfolder>
        :type current_step: <int>
    """

    def __init__(self, solution, unfolder):
        """
        :param solution: DIMACS encoding of **a solution** from the solver
            (tuple of literals)
        :param unfolder: Current unfolder for the solution
            (unfolder is used for invariant constants)
        :type solution: <tuple <int>>
        :type unfolder: <CLUnfolder>
        """
        self.solution = solution
        self.unfolder = unfolder
        self.shift_step = unfolder.shift_step
        self.current_step = unfolder.current_step
        self.shift_direction = unfolder.shift_direction

    def get_unshift_code(self, var_num):
        """Get the real value of the given variable in the system (remove the shift)

        ..warning:: DEPRECATED Used internally by self.unflatten()

        @param var_num: DIMACS literal coding of a shifted variable x_i
        @return: DIMACS literal coding of  x_0 with same value
        :return: <int>
        """
        # Old API
        # var_code = (abs(var_num) - 1) % self.shift_step + 1
        #
        # if var_code <= self.shift_step:
        #     return var_code * (-1 if var_num < 0 else 1)
        #
        # raise MCLException("Not a DIMACS code of an initial variable")

        # New API via C++ module
        get_unshift_code(var_num, self.shift_step)

    def get_var_name(self, var_num):
        """For translation to symbolic representation
        Return the name of a variable with its value.
        """
        return self.unfolder.get_var_name(var_num)

    def unflatten(self):
        """Extract trajectories from the current solution

        Transform a flat DIMACS representation of a trajectory into a
        <list <list <int>>>.
        Each sublist represents a state vector (the state of all variables of
        the system for 1 step in the trajectory).

        ..note:: This assertion seems to be not true:
            Auxiliary variables introduced by properties compiling are ignored.
            => there are lots of variables on the format "_name"...

        ..note:: Debug with:

            >>> raw_sol = RawSolution()
            >>> print(raw_sol)

        ..note:: The list returns all variables of the system including
            inputs, clocks, auxiliary variables.

        :return: A list of state vectors (<list <int>>) in DIMACS format
        :rtype: <list <list <int>>>
        """

        # Old API
        # lv_traj = []
        # step = 0
        # dec = 0
        # shift_step_init = self.unfolder.shift_step_init
        # # n steps means h0, ..., h(n-1) in constraints for clocks and inputs
        # while dec + self.shift_step < len(self.solution):
        #     #assert [self.get_unshift_code(self.solution[i+dec]) for i in range(shift_step_init)] == [get_unshift_code(self.solution[i+dec], self.shift_step) for i in range(shift_step_init)]
        #     lv_traj.append(
        #         [get_unshift_code(self.solution[i+dec], self.shift_step)
        #          for i in range(shift_step_init)]
        #     )
        #     step += 1
        #     dec = step * self.shift_step # first index of time step
        # return lv_traj # list of lists

        # New API via C++ module
        return unflatten(
            self.solution,
            self.unfolder.shift_step_init,
            self.shift_step
        )

    def extract_activated_frontier_values(self):
        """Extracts frontier variables which are active in solution.

        :return: Set of activated frontier values.
        :rtype: <frozenset>
        """
        if self.shift_direction == "FORWARD":
            # frontier_values: Set of frontier positive values only.
            return (
                frozenset(self.unfolder.frontier_values)
                & self.frontier_pos_and_neg_values
            )
        else:
            NotImplementedError("BACKWARD shift direction is not yet implemented")

    @cached_property
    def frontier_pos_and_neg_values(self):
        """Extracts the frontier values from the solution.
        These values are in DIMACS code.

        .. warning:: This function returns values of active AND inactive frontiers.

        .. warning:: Assert: solution is sorted by variable code for BACKWARD

        .. note:: This function makes set operations between all values of
            frontiers and the current solution.
            This last one is a list of hundreds of thousands items
            (ex: ~500000 for a solution with 10 steps).
            Thus, the operation is costly and we use a decorator @cached_property
            to put the result in cache.

        .. note:: Used by:
            - self.extract_activated_frontier_values()
            - DimacsFrontierSol.__init__()

        .. note::
            frontiers (fixed size): 3824
            solution (increasing size): 171231, 228314, 285405, 285453, 400091 etc.

        :return: A dimacs code set of the activation state on the frontiers for
            the current solution.
        :rtype: <frozenset <int>>
        """
        # Old API
        # jmax = len(self.unfolder.frontier_values)
        # fsol = []
        # j = 0
        # dec = self.shift_step * self.current_step
        # sol = self.solution
        # for i in range(len(sol)):
        #     # the variable is frontier var:
        #     if abs(sol[i]) == self.unfolder.frontier_values[j]:
        #         if self.shift_direction == "FORWARD":
        #             fsol.append(sol[i])
        #         else:
        #             fsol.append(sol[i+dec])     # look for initial values
        #         j += 1
        #         if j == jmax:
        #             return fsol
        # return fsol # never reach this point

        # Old API v2
        # frontiers = self.unfolder.frontier_values
        # jmax = len(frontiers)
        # fsol = list()
        # j = 0
        # dec = self.shift_step * self.current_step
        # for i, sol in enumerate(self.solution):
        #    # the variable is frontier var:
        #    if abs(sol) == frontiers[j]:
        #        if self.shift_direction == "FORWARD":
        #            fsol.append(sol)
        #        else:
        #            fsol.append(self.solution[i+dec])# look for initial values
        #        j += 1
        #        if j == jmax:
        #            return fsol
        #return fsol # never reach this point

        if self.shift_direction == "FORWARD":
            # frontiers_pos_and_neg:
            # All frontiers and their opposite version Union
            # Set of frontier positive and negative values.
            return self.unfolder.frontiers_pos_and_neg & frozenset(self.solution)
        else:
            # NEVER USED (BACKWARD is partially implemented)
            frontiers = self.unfolder.frontier_values
            jmax = len(frontiers)
            fsol = list()
            j = 0
            dec = self.shift_step * self.current_step
            frontier = frontiers[0]
            for i, var in enumerate(self.solution):
                # the variable is frontier var:
                if abs(var) == frontier:
                    fsol.append(self.solution[i + dec])  # look for initial values
                    j += 1
                    if j == jmax:
                        # all frontiers are found
                        return frozenset(fsol)
                    frontier = frontiers[j]
        return frozenset(fsol)  # never reach this point

    # Useless proposition
    # ps: jmax allows to stop the search when the iteration is made on solution
    # which is increasing over time.
    # without jmax, this proposition is not efficient
    #        frontiers = frozenset(self.unfolder.frontier_values)
    #        dec = self.shift_step * self.current_step
    #        if self.shift_direction == 'FORWARD':
    #            fsol = [sol for sol in self.solution if abs(sol) in frontiers]
    #        else:
    #            fsol = [self.solution[i+dec] for i, sol in enumerate(self.solution) if abs(sol) in frontiers]
    #
    #        assert len(fsol) == len(frontiers)
    #        return fsol

    def extract_act_inputs_clocks(self, state_vector):
        """Extract active *inputs* and *free_clocks* from a state vector.

        Return the intersection of all inputs and free clocks of the system
        with the given state vector.

        PS: unfolder.inputs_and_free_clocks contains only positive values
            so the intersection with state_vector allows to get only activated
            variables.

        Used only by extract_act_input_clock_seq().

        :param state_vector: A state vector. A list of literals.
        :return: Tuple of activated inputs and free_clocks in the given state vector.
        :type state_vector: <list <int>>
        :rtype: <tuple>
        """
        # Old API
        # return [s_varcode for s_varcode in state_vector
        #        if s_varcode > 0
        #        and s_varcode in self.unfolder.inputs_and_free_clocks]
        return tuple(self.unfolder.inputs_and_free_clocks & frozenset(state_vector))

    def extract_act_input_clock_seq(self):
        """Extract the sequence of activated *inputs* and *events/free clocks*
        in the current solution.

        .. note::
            - Each tuple is the state of literals in a step of the solution.
            - Each literal in the tuple is an activated variable in a step.
            - Variables are inputs or events (free clocks) ONLY!

        .. note:: A solution is list of state vectors (list of literals).

        .. note:: This function is called by:
            - FrontierSolution.from_raw()
            - DimacsFrontierSol.ic_sequence

        :return: list of input vector
            (may be empty if data-flow model is without input)
        :rtype: <tuple <tuple <int>>>
        """
        # unflatten() returns a list of state vectors in DIMACS format
        # State vectors are (<list <int>>)
        return (
            tuple()
            if not self.unfolder.inputs_and_free_clocks
            else tuple(
                self.extract_act_inputs_clocks(activated_inputs_and_clocks)
                for activated_inputs_and_clocks in self.unflatten()  # list of lists
            )
        )

    def __len__(self):
        """Length of solution (number of tuples of literals)
        @return: int
        """
        return len(self.solution)

    def __str__(self):
        """For debug: display all variables
        (including inactivated and auxiliary ones)
        """
        unfl = self.unflatten()
        stn = []
        for vect in unfl:
            vect_n = []
            for dcod in vect:
                if dcod > 0:
                    vect_n.append(self.get_var_name(dcod))
                else:
                    vect_n.append("-" + self.get_var_name(dcod))
            stn.append(vect_n)
        return str(stn)

    def display_activ_sol(self):
        """For debug: display only activated variables
        (auxiliary variables are pruned)
        """
        unfl = self.unflatten()
        stn = []
        for vect in unfl:
            vect_n = []
            for dcod in vect:
                if dcod > 0:
                    v_name = self.get_var_name(dcod)
                    if not v_name[0] == "_":
                        # Not auxiliary variable
                        vect_n.append(v_name)
            vect_n.sort()
            stn.append(vect_n)
        print(stn)


class FrontierSolution(object):
    """Class for symbolic (human readable) frontiers and timings representation

    The class FrontierSolution provides is a wrapper for a symbolic
    representation (human readable) of activated frontiers defined in
    RawSolution and DimacsFrontierSol objects.

    Attributes:

        - The main attributes are activated_frontier which is a set of
          (string) names of frontier places which are activated in the solution.

        - The second important attribute is ic_sequence, a list of strings
          which describes the successive activated inputs and free events in
          the solution.

        - current_step is the number of steps used during the unfolding that made
          the solution.

    If events h2, h5 and input in3 are activated at step k in the solution,
    then the kth element of the list is “% h2 h5 in3”.
    This format is understood by the Cadbiom simulator.

    :type activated_frontier: <frozenset <str>>
    :type ic_sequence: <list <str>>
    :type current_step: <int>

    .. TODO::
        - Faire une super classe dont héritent RawSolution et DimacsFrontierSol
          pour éviter la duplication de code et le stockage d'attributs qu'on
          connait déjà dans les types de plus bas niveaux...
        - ... Ou détecter le type d'objet dans le constructeur => ducktyping
        - renommer l'attr activated_frontier en activated_frontiers
    """

    def __init__(self, activated_frontiers, ic_sequence, current_step):
        """Build a symbolic representation of frontier values and timing from
        a raw solution

        :param activated_frontiers: A list of (string) names of frontier places
            which are activated in the solution.
        :param ic_sequence: A list of strings which describes the successive
            activated inputs and free events in the solution.
            (format: % h1 h2)
        :param current_step: Number of steps in the sequence.
            ..note:: This attribute should be deducted with the length of ic_sequence.
        :type activated_frontiers: <frozenset <str>>
        :type ic_sequence: <list <str>>
        :type current_step: <int>
        """
        self.activated_frontier = frozenset(activated_frontiers)
        self.ic_sequence = ic_sequence
        self.current_step = current_step

    @classmethod
    def build_input_clock_sequence(cls, get_var_name, ic_sequence):
        """Get strings representing timings of each step in the solution.

        :param get_var_name: Method to call for a conversion of values to names.
            (binding of the method get_var_name() of an unfolder).
        :param ic_sequence:
            - Each tuple is the state of literals in a step of the solution.
            - Each literal in the tuple is an activated variable in a step.
            - Variables are inputs or events (free clocks) ONLY!
        :type get_var_name: <function>
        :type ic_sequence: <tuple <tuple <int>>
        :return: List of strings representing timings of each step in ic_sequence.
        :rtype: <list <str>>
        """
        # Strip used to remove trailing space on empty steps : "% "
        return [
            str("% " + " ".join(get_var_name(value)
            for value in step_literals)).rstrip(" ")
            for step_literals in ic_sequence
        ]

    @classmethod
    def from_raw(cls, raw_sol):
        """Build FrontierSolution object, a symbolic representation of frontier
        values and timings from a RawSolution solution.

        - Extract activated frontiers values (literals)
        - Convert activated frontiers values to places names (strings)
        - Extract inputs and clocks sequence (steps of the whole solution)

        :type raw_sol: <RawSolution>
        """
        # Get names of activated frontier places
        # RawSolution has not activated_frontiers attr we must compute them
        activated_frontier_values = raw_sol.extract_activated_frontier_values()

        activated_frontiers = {
            raw_sol.get_var_name(var_num) for var_num in activated_frontier_values
        }

        # Get raw activated inputs and free clocks (values)
        # and format them so that they are understandable by humans
        ic_sequence = FrontierSolution.build_input_clock_sequence(
            raw_sol.get_var_name,
            raw_sol.extract_act_input_clock_seq()
        )
        # LOGGER.debug("FrontierSolution:from_raw:: ic_sequence %s", ic_sequence)

        return cls(activated_frontiers, ic_sequence, raw_sol.current_step)

    @classmethod
    def from_dimacs_front_sol(cls, dimacs_front_sol):
        """Build FrontierSolution object, a symbolic representation of frontier
        values and timings from a DimacsFrontierSolution solution.

        - Convert activated frontiers values to places names (strings)
        - Extract inputs and clocks sequence (steps of the whole solution)

        :type dimacs_front_sol: <DimacsFrontierSol>
        """
        # Get names of activated frontier places
        # DimacsFrontierSol already has activated_frontiers attr
        activated_frontiers = {
            dimacs_front_sol.get_var_name(var_num)
            for var_num in dimacs_front_sol.activated_frontier_values
        }

        # Get raw activated inputs and free clocks (values)
        # and format them so that they are understandable by humans
        ic_sequence = FrontierSolution.build_input_clock_sequence(
            dimacs_front_sol.get_var_name,
            dimacs_front_sol.ic_sequence
        )
        # LOGGER.debug("FrontierSolution:from_dimacs_front_sol:: ic_sequence %s", ic_sequence)

        return cls(activated_frontiers, ic_sequence, dimacs_front_sol.current_step)

    @classmethod
    def from_file(cls, file_name):
        """Build a symbolic representation of frontier values and timing from
        a DimacsFrontierSolution solution

        ..warning:: This method can only be used if the file contains 1 solution...

        Note: use cadbiom_cmd/tools/solutions.py functions to reload frontiers
        """
        with open(file_name, "r") as f_d:
            # Get first line: frontiers
            act_front = f_d.readline().split()
            # Get steps
            ic_seq = []
            step = f_d.readline()
            current_step = 0
            while step:
                current_step += 1
                ic_seq.append(step[:-1])
                step = f_d.readline()

        LOGGER.debug(
            "FrontierSolution:from_file:: ic_seq: %s; maxsteps: %s",
            ic_seq,
            current_step,
        )
        return cls(act_front, ic_seq, current_step)

    @cached_property
    def sorted_activated_frontier(self):
        """Sort activated places in alphanumeric order.

        Intended to facilitate readability and debugging.

        :return: List of sorted places
        :rtype: <list <str>>
        """
        return sorted(self.activated_frontier, key=lambda s: s.lower())

    def save(self, outfile, only_macs=False):
        """Save a symbolic solution in a file
        The format is readable by the simulator and all Cadbiom tools.

        .. note:: Frontiers are sorted in (lower case) alphabetical order.

        :param outfile: Writable file handler
        :param only_macs: Write only frontiers, and skip timings.
        :type outfile: <open file>
        :type only_macs: <boolean>
        """
        outfile.write(" ".join(self.sorted_activated_frontier) + "\n")
        if not only_macs:
            outfile.write("\n".join(self.ic_sequence) + "\n")
        outfile.flush()

    def __eq__(self, other):
        """Check if two FrontierSolution have same activated frontiers
        Used with __hash__

        ..warning:: We do not test other attributes than activated_frontier.
            ic_sequence might be necessary.

        :type other: <DimacsFrontierSol>
        :rtype: <boolean>
        """
        return self.activated_frontier == other.activated_frontier

    def __ne__(self, other):
        """Python 2 requires this in conjunction to __eq__..."""
        return self.__eq__(other)

    def __hash__(self):
        """Used to test unicity of FrontierSolution in sets;
        Used with __eq__

        ..warning:: We do not test other attributes than activated_frontier.
            ic_sequence might be necessary.
        """
        return hash(self.activated_frontier)

    def __repr__(self):
        """Representation of a FrontierSolution in the console"""
        return "<FrontierSolution %s>" % self.sorted_activated_frontier

    def __str__(self):
        """String representation of a FrontierSolution"""
        stro = "<FrontierSolution - Activated frontiers: "
        stro += str(self.sorted_activated_frontier)
        stro += "\nTimings:\n   "
        stro += "\n   ".join(self.ic_sequence) + ">"
        return stro


class DimacsFrontierSol(object):
    """Class for solution frontier and timings representation

    DimacsFrontierSol is a numerical representation of *frontier values and timings*
    from a raw solution.

    Attributes:

        :param frontier_values: Frontier values from the solution.
            These values are in DIMACS code.
            This attribute is **immutable**.
            Based on the initial RawSolution.
        :param ic_sequence: Sequence of activated inputs and events in the solution.
            Only used in FrontierSolution.from_dimacs_front_sol()
            (at the end of the search process for the cast into FrontierSolution)
            and for tests.
            Based on the initial RawSolution.
        :param current_step: The number of steps allowed in the unfolding;
            the current_step on which the properties must be satisfied (never used)
            Based on the initial RawSolution.
        :param nb_activated_frontiers: Number of activated places in the current
            Dimacs solution.
            This attribute is precomputed because it is used intensively and
            multiple times for each object in:

                - MCLAnalyser.less_activated_solution
                - MCLAnalyser.__prune_frontier_solution
                - MCLAnalyser.__mac_exhaustive_search
        :param activated_frontier_values: Values of activated frontier places
            in the current Dimacs solution.
            Convenient attribute used:

                - by FrontierSolution.from_dimacs_front_sol()
                - to accelerate the call of self.nb_activated_frontiers
                - as a criterion of uniqueness, to do set operations
        :type frontier_values: <frozenset <int>>
        :type ic_sequence: <list <list <int>>>
        :type current_step: <int>
        :type nb_activated_frontiers: <int>
        :type activated_frontier_values: <frozenset <int>>
    """

    def __init__(self, raw_sol):
        """Build a DimacsFrontierSol, a numeric representation of frontier values
        and timings from a raw solution

        :param raw_sol: raw solution
        :type raw_sol: <RawSolution>
        """
        # Frontier places
        # /!\ Most of the time spent in the constructor is due to this line
        self.frontier_values = raw_sol.frontier_pos_and_neg_values

        # Activated input/events (clocks)
        # Callable of raw_sol method (avoid to store raw_sol in this object)
        self._ic_sequence_func = raw_sol.extract_act_input_clock_seq
        self.current_step = raw_sol.current_step

        # CLUnfolder
        self.unfolder = raw_sol.unfolder

        # Values of activated frontier places in the current Dimacs solution
        # Convenient attribute used:
        # - by FrontierSolution.from_dimacs_front_sol()
        # - to accelerate the call of self.nb_activated_frontiers
        # - as a criterion of uniqueness, to do set operations
        # Already a frozenset but this attribute must be immutable for __hash__,
        # cast is a security.
        self.activated_frontier_values = frozenset(
            raw_sol.extract_activated_frontier_values()
        )

        # Pre-compute nb of activated frontiers in the current solution
        # PS: use numpy to accelerate this ? The cast is costly...
        # We could keep a separated function and use lru_cache instead...
        ## TODO: replace by len() call magic method
        self.nb_activated_frontiers = len(self.activated_frontier_values)

    @classmethod
    def get_unique_dimacs_front_sols_from_raw_sols(cls, raw_sols):
        """Get a tuple of DimacsFrontierSols from a list of RawSolutions.

        The conversion extracts keeps only frontier values from RawSolutions.
        This functions eliminates the duplicates.

        Cf TestMCLAnalyser.py:523:
            raw_sols len 6
            tpl len: 6
        TestMCLAnalyser.py:559
            raw_sols len 12:
            tpl len: 7
        TestMCLAnalyser.py:667
            raw_sols len 7:
            tpl len: 1
        TestMCLAnalyser.py:700
            raw_sols len 7
            tpl len: 1

        ..note:: We need to index the result in MCLAnalyser.less_activated_solution()
            thus, this why we return a tuple here.

        ..note:: The tuple of DimacsFrontierSols is not sorted by order of calculation.
            Thus, the first item is not the first solution found.
            TODO: An order could be used to adjust the number of solutions
            asked during the pruning operation in __solve_with_inact_fsolution()

        :param raw_sols: List of raw solutions;
            most of the time obtained with sq_solutions()
        :return: Set of DimacsFrontierSol
        :type raw_sols: <list <RawSolution>>
        :rtype: <tuple <DimacsFrontierSol>>
        """
        return tuple({DimacsFrontierSol(sol) for sol in raw_sols})

    @property
    def ic_sequence(self):
        """Sequence of activated inputs and events (clocks) in the solution.

        (may be empty if data-flow model is without input)

        .. seealso:: RawSolution.extract_act_input_clock_seq()

        .. note:: Only used in FrontierSolution.from_dimacs_front_sol()
            (at the end of the search process for the cast into FrontierSolution)
            and for tests.
            => This step is expensive !
        """
        # Cf constructor
        return self._ic_sequence_func()

    def get_var_name(self, var_num):
        """For translation to symbolic representation
        Return the string that corresponds to he name of the variable value.
        :rtype: <str>
        """
        return self.unfolder.get_var_name(var_num)

    def nb_timed(self):
        """Count the number of events in the current Dimacs solution (not used)
        :rtype: <int>
        """
        # ic_sequence: list of strings which describes the successive activated
        # inputs and free events
        solution_events = (len(ic_act) for ic_act in self.ic_sequence)
        return sum(it.chain(*solution_events))

    def __len__(self):
        """Get the number of activated frontiers in the current DimacsFrontierSol
        :rtype: <int>
        """
        return len(self.activated_frontier_values)

    def __eq__(self, other):
        """Check if two DimacsFrontierSol have same frontiers values
        Used with __hash__

        ..warning:: We do not test other attributes than activated_frontier_values.
            ic_sequence might be necessary.

        :type other: <DimacsFrontierSol>
        :rtype: <boolean>
        """
        return self.activated_frontier_values == other.activated_frontier_values

    def __ne__(self, other):
        """Python 2 requires this in conjunction to __eq__..."""
        return self.__eq__(other)

    def __hash__(self):
        """Used to test unicity of DimacsFrontierSol in sets;
        Used with __eq__

        ..warning:: We do not test other attributes than activated_frontier_values.
            ic_sequence might be necessary.
        """
        return hash(self.activated_frontier_values)

    def __repr__(self):
        return str(self.activated_frontier_values)

    def __str__(self):
        """For tests and debug"""
        return "<DimacsFrontierSol - Activated frontiers values: %s>".format(
            self.activated_frontier_values
        )
