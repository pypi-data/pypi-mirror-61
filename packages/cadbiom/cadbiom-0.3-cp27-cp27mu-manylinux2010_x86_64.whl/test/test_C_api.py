# -*- coding: utf-8 -*-
"""Unit tests for C API"""

from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
import pytest

def test_shift_clause():

    from _cadbiom import shift_clause

    found = shift_clause([42198], 47633)
    assert found == [89831]

    found = shift_clause([66035, 66037, -66036], 47633)
    assert found == [113668, 113670, -113669]

    found = shift_clause([66036, -66037], 47633)
    assert found == [113669, -113670]

    found = shift_clause([55515, 58893, 48355, -48352], 47633)
    assert found == [103148, 106526, 95988, -95985]


def test_shift_dimacs_clauses():

    from _cadbiom import shift_dimacs_clauses

    found = shift_dimacs_clauses([[66035, 66037, -66036],
                           [66036, -66037],
                           [55515, 58893, 48355, -48352]], 47633)
    assert found == [[113668, 113670, -113669],
                     [113669, -113670],
                     [103148, 106526, 95988, -95985]]

################################################################################

def test_get_unshift_code():

    from _cadbiom import get_unshift_code

    found = get_unshift_code(-1, 47633)
    assert found == -1

    found = get_unshift_code(50, 47633)
    assert found == 50

    found = get_unshift_code(50, 2)
    assert found == 2


def test_unflatten():

    from _cadbiom import unflatten

    found = unflatten(
                [66035, 66037, -66036, 55515, 58893, 48355, -48352],
                2, # CLUnfolder.shift_step_init
                1, # CLUnfolder.shift_step_init
            )
    assert found == [[1, 1], [1, -1], [-1, 1], [1, 1], [1, 1], [1, -1]]

    found = unflatten(
                [66035, 66037, -66036, 55515, 58893, 48355, -48352],
                1, # CLUnfolder.shift_step_init
                1, # CLUnfolder.shift_step_init
            )
    assert found == [[1], [1], [-1], [1], [1], [1]]

################################################################################

@pytest.fixture()
def feed_forward_code():

    class Clause():
        def __init__(self, lits):
            self.literals = lits

    class Literal():
        def __init__(self, name, sign):
            self.name = name # string
            self.sign = sign # bool
        def __repr__(self):
            return "name:{}; sign:{}".format(self.name, self.sign)

    # Make a Clause with Literals objects
    literal_defs = [('Hsp90', True), ('not _lit2', False), ('Hsp90`', False)]
    literals = [Literal(name, sign) for name, sign in literal_defs]
    #print(literals)
    clause = Clause(literals)

    var_code_table = \
        {'Hsp90': 10,
         'not _lit2': 11,
         #'Hsp90`': 12, # volontary removed
         'NRAMP1_gene': 1,
         'PDK1_active_p': 42583,
         'EGFR_EGFR_EGF_EGF_GRB2_PAK1_active_intToMb': 2,
         'CCL26_exCellRegion_gene': 3,
         '_lit3093': 34992,
         '_lit25839': 4,
         '_lit25838': 5,
         '_lit25837': 6,
         '_lit25836': 7,
         '_lit25835': 8,
         }

    # Optimization: for forward_init_dynamic() and forward_code() (mostly
    # implemented in C.
    # Precompute __var_code_table with the literal names in "future" format;
    # i.e with a last char '`' at the end.
    # Thus it is easy to search them directly in the dict (in O(1)),
    # instead of slicing them.
    # See CLUnfolder constructor.
    temp_var_code_table = \
        {var_name + "`": var_num for var_name, var_num in var_code_table.iteritems()}
    var_code_table.update(temp_var_code_table)

    shift_step = 1

    return clause, var_code_table, shift_step


def test_forward_code(feed_forward_code):

    from _cadbiom import forward_code

    found = forward_code(feed_forward_code[0], # clause
                         feed_forward_code[1], # var_code_table
                         feed_forward_code[2]) # shift_step
    assert found == [10, -11, -11]


def test_forward_init_dynamic(feed_forward_code):

    from _cadbiom import forward_init_dynamic

    found = forward_init_dynamic([feed_forward_code[0], feed_forward_code[0]], # clause
                                 feed_forward_code[1], # var_code_table
                                 feed_forward_code[2]) # shift_step
    assert found == [[[10, -11, -11], [10, -11, -11]]]

