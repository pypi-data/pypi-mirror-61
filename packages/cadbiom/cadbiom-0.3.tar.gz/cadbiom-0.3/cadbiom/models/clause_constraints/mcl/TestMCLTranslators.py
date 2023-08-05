# -*- coding: utf-8 -*-
## Filename    : TestMCLTranslators.py
## Author(s)   : Michel Le Borgne
## Created     : 9 mars 2012
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
## Contributor(s):
##
"""
Unitary tests for the translators
"""
from __future__ import print_function
import pkg_resources
import unittest

from cadbiom.models.clause_constraints.CLDynSys import CLDynSys
from cadbiom.models.clause_constraints.mcl.MCLTranslators import (
    MCLSigExprVisitor,
    gen_transition_clock,
    gen_transition_list_clock,
    gen_simple_evolution,
    GT2Clauses,
)
from cadbiom.models.biosignal.sig_expr import (
    SigIdentExpr,
    SigSyncBinExpr,
    SigWhenExpr,
    SigDefaultExpr,
)
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.clause_constraints.mcl.MCLAnalyser import MCLAnalyser


class ErrorRep(object):
    """Simple error reporter"""

    def __init__(self):
        self.mess = ""
        self.error = False

    def display(self, mess):
        """
        set error and print
        """
        self.error = True
        self.mess += ">> " + mess
        print(" DISPLAY CALL>> " + mess)


class TestTransitionClauses(unittest.TestCase):
    """
    Test of transitions into clauses
    """

    def test_no_cond(self):  # OK
        """
        n1 --> n2; []
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        trans = root.add_transition(nn1, nn2)

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit, reporter)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "n1"
        assert cl_ds.clauses == []

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == []

        print("reporter:", reporter.mess)
        assert reporter.mess == ""

    def test_cond(self):  # OK
        """
        n1 --> n2; [not n3]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("n3", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n3")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit0"

        expected = ["$n1, not _lit0$", "$not n3, not _lit0$", "$not n1, n3, _lit0$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == []

        print("reporter:", reporter.mess)
        assert reporter.mess == ""

    def test_no_cond_event(self):  # OK
        """
        n1 --> n2; h[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_event("h")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit0"

        expected = ["$not _lit0, h$", "$not _lit0, n1$", "$not h, not n1, _lit0$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

        print("---------- opti ----------------")
        sed = dict()
        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        event_literal = gen_transition_clock(trans, cl_ds, sed, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit0"

        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_cond_event(self):  # OK
        """
        n1 --> n2; h[not n3]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("n3", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n3")
        trans.set_event("h")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit1"

        expected = [
            "$n1, not _lit0$",
            "$not n3, not _lit0$",
            "$not n1, n3, _lit0$",
            "$not _lit1, h$",
            "$not _lit1, _lit0$",
            "$not h, not _lit0, _lit1$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

        print("---------- opti ----------------")
        sed = dict()
        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        event_literal = gen_transition_clock(trans, cl_ds, sed, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit1"

        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_perm_no_cond_event(self):  # OK
        """
        n1/p --> n2; h[];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_perm_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_event("h")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit0"

        expected = ["$not _lit0, h$", "$not _lit0, n1$", "$not h, not n1, _lit0$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_perm_cond_event(self):  # OK
        """
        n4;
        n1/p --> n2; h[n4];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_perm_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("n4")
        trans.set_event("h")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit0"

        expected = ["$not _lit0, h$", "$not _lit0, n4$", "$not h, not n4, _lit0$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_input_cond_event(self):  # OK
        """
        n4/i;
        n1/i --> n2; h[n4];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_input_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_input_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("n4")
        trans.set_event("h")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit1"

        expected = [
            "$n1, not _lit0$",
            "$n4, not _lit0$",
            "$not n1, not n4, _lit0$",
            "$not _lit1, h$",
            "$not _lit1, _lit0$",
            "$not h, not _lit0, _lit1$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    # complex events
    def test_no_cond_event_when1(self):  # OK
        """
        n1 --> n2; h when n3[]
        n3;
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("n3", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_event("h when n3")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        event_literal = gen_transition_clock(trans, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit1"

        expected = [
            "$not h, not n3, _lit0$",
            "$not _lit0, h$",
            "$not _lit0, n3$",
            "$not _lit1, _lit0$",
            "$not _lit1, n1$",
            "$not _lit0, not n1, _lit1$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("place_clocks", cl_ds.place_clocks)
        assert cl_ds.place_clocks == {"_lit0": ["n1"]}

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_no_cond_event_when2(self):  # OK
        """
        n1 --> n2; h when n3[]
        n3 --> n1 ; h2 when h[]
        Error h is not a state
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        tr1 = root.add_transition(nn1, nn2)
        tr1.set_event("h when n3")
        tr2 = root.add_transition(nn3, nn1)
        tr2.set_event("h2 when h")

        reporter = ErrorRep()
        tvisit = TableVisitor(reporter)  # no error display
        model.accept(tvisit)

        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        event_literal = gen_transition_clock(tr1, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit1"
        event_literal = gen_transition_clock(tr2, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit3"

        expected = [
            "$not h, not n3, _lit0$",
            "$not _lit0, h$",
            "$not _lit0, n3$",
            "$not _lit1, _lit0$",
            "$not _lit1, n1$",
            "$not _lit0, not n1, _lit1$",
            "$not h2, not h, _lit2$",
            "$not _lit2, h2$",
            "$not _lit2, h$",
            "$not _lit3, _lit2$",
            "$not _lit3, n3$",
            "$not _lit2, not n3, _lit3$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h", "h2"]

        print("place_clocks", cl_ds.place_clocks)
        assert cl_ds.place_clocks == {"_lit2": ["n3"], "_lit0": ["n1"]}

        print("reporter: ", reporter.mess)
        assert reporter.mess == ">> type error -> h is not a state (clock)"

    def test_no_cond_event_when3(self):  # OK
        """
        n1 --> n2; h when n3[]
        n3 --> n1 ; n2 when n1[]
        Error n2 is not a clock
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        tr1 = root.add_transition(nn1, nn2)
        tr1.set_event("h when n3")
        tr2 = root.add_transition(nn3, nn1)
        tr2.set_event("n2 when n1")

        reporter = ErrorRep()
        tvisit = TableVisitor(reporter)  # no error display
        model.accept(tvisit)

        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        event_literal = gen_transition_clock(tr1, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit1"
        event_literal = gen_transition_clock(tr2, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit3"

        expected = [
            "$not h, not n3, _lit0$",
            "$not _lit0, h$",
            "$not _lit0, n3$",
            "$not _lit1, _lit0$",
            "$not _lit1, n1$",
            "$not _lit0, not n1, _lit1$",
            "$not _lit3, _lit2$",
            "$not _lit3, n3$",
            "$not _lit2, not n3, _lit3$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h"]

        print("place_clocks", cl_ds.place_clocks)
        assert cl_ds.place_clocks == {"_lit2": ["n3"], "_lit0": ["n1"]}

        print("reporter: ", reporter.mess)
        assert reporter.mess == ">> Default signal:(n2 when n1) is not a clock"

    def test_no_cond_event_default(self):  # OK
        """testNoCondEventWhen1
        n1 --> n2; h1 when c1 default h2[c3]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("c1", 0, 0)
        root.add_simple_node("c3", 0, 0)
        tr1 = root.add_transition(nn1, nn2)
        tr1.set_event("h when c1 default h2")
        tr1.set_condition("c3")

        reporter = ErrorRep()
        tvisit = TableVisitor(reporter)  # no error display
        model.accept(tvisit)

        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        event_literal = gen_transition_clock(tr1, cl_ds, None, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit3"

        expected = [
            "$n1, not _lit0$",
            "$c3, not _lit0$",
            "$not n1, not c3, _lit0$",
            "$not h, not c1, _lit2$",
            "$not _lit2, h$",
            "$not _lit2, c1$",
            "$not _lit1, _lit2, h2$",
            "$not _lit2, _lit1$",
            "$not h2, _lit1$",
            "$not _lit3, _lit1$",
            "$not _lit3, _lit0$",
            "$not _lit1, not _lit0, _lit3$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h", "h2"]

        print("place_clocks", cl_ds.place_clocks)
        assert cl_ds.place_clocks == {"_lit1": ["n1"]}

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""


class TestTransitionList(unittest.TestCase):
    """
    As it says
    """

    def test_no_cond_on_out2events(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        n4 --> n1; h3[]
        gen_transition_list_clock tested
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        nn4 = root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event("h1")
        trans = root.add_transition(nn1, nn3)
        trans.set_event("h2")
        trans = root.add_transition(nn4, nn1)
        trans.set_event("h3")

        tvisit = TableVisitor(None)  # no error display/ might crash
        model.accept(tvisit)

        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)
        trl = nn1.outgoing_trans
        sed = dict()
        event_literal = gen_transition_list_clock(trl, cl_ds, sed, reporter)
        print("Transition clock:", str(event_literal))
        assert str(event_literal) == "_lit3"

        expected = [
            "$n1, not _lit0$",
            "$not n4, not _lit0$",
            "$not n1, n4, _lit0$",
            "$not _lit1, h1$",
            "$not _lit1, _lit0$",
            "$not h1, not _lit0, _lit1$",
            "$not _lit2, h2$",
            "$not _lit2, n1$",
            "$not h2, not n1, _lit2$",
            "$_lit3, not _lit1$",
            "$_lit3, not _lit2$",
            "$_lit1, _lit2, not _lit3$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h1", "h2"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_very_simple(self):  # OK to optimize
        """
        n1 --> n2; []
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_transition(nn1, nn2)

        model.clean_code()
        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        gen_simple_evolution(nn1, cl_ds, None, reporter)

        expected = ["$not n1`, n1$", "$not n1`, not n1$", "$n1`, not n1, n1$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == []

        model.clean_code()

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_simple(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        nn4 = root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event("h1")
        trans = root.add_transition(nn1, nn3)
        trans.set_event("h2")
        trans = root.add_transition(nn4, nn1)
        trans.set_event("h3")

        model.clean_code()
        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        sed = dict()
        gen_simple_evolution(nn1, cl_ds, sed, reporter)

        expected = [
            "$not _lit0, h3$",
            "$not _lit0, n4$",
            "$not h3, not n4, _lit0$",
            "$n1, not _lit1$",
            "$not n4, not _lit1$",
            "$not n1, n4, _lit1$",
            "$not _lit2, h1$",
            "$not _lit2, _lit1$",
            "$not h1, not _lit1, _lit2$",
            "$not _lit3, h2$",
            "$not _lit3, n1$",
            "$not h2, not n1, _lit3$",
            "$_lit4, not _lit2$",
            "$_lit4, not _lit3$",
            "$_lit2, _lit3, not _lit4$",
            "$not n1`, _lit0, n1$",
            "$not n1`, _lit0, not _lit4$",
            "$n1`, not _lit0$",
            "$n1`, not n1, _lit4$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h3", "h1", "h2"]

        model.clean_code()

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_simple_in_no_out(self):
        """
        n2 --> n1; h1[not n4]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("n3", 0, 0)
        nn4 = root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn2, nn1)
        trans.set_condition("not n4")
        trans.set_event("h1")
        trans = root.add_transition(nn4, nn1)
        trans.set_event("h3")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        gen_simple_evolution(nn1, cl_ds, None, reporter)

        expected = [
            "$n2, not _lit0$",
            "$not n4, not _lit0$",
            "$not n2, n4, _lit0$",
            "$not _lit1, h1$",
            "$not _lit1, _lit0$",
            "$not h1, not _lit0, _lit1$",
            "$not _lit2, h3$",
            "$not _lit2, n4$",
            "$not h3, not n4, _lit2$",
            "$_lit3, not _lit1$",
            "$_lit3, not _lit2$",
            "$_lit1, _lit2, not _lit3$",
            "$not n1`, _lit3, n1$",
            "$n1`, not _lit3$",
            "$n1`, not n1$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h1", "h3"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_simple_out_no_in(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event("h1")
        trans = root.add_transition(nn1, nn3)
        trans.set_event("h2")

        model.clean_code()
        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        gen_simple_evolution(nn1, cl_ds, None, reporter)

        expected = [
            "$n1, not _lit0$",
            "$not n4, not _lit0$",
            "$not n1, n4, _lit0$",
            "$not _lit1, h1$",
            "$not _lit1, _lit0$",
            "$not h1, not _lit0, _lit1$",
            "$not _lit2, h2$",
            "$not _lit2, n1$",
            "$not h2, not n1, _lit2$",
            "$_lit3, not _lit1$",
            "$_lit3, not _lit2$",
            "$_lit1, _lit2, not _lit3$",
            "$not n1`, n1$",
            "$not n1`, not _lit3$",
            "$n1`, not n1, _lit3$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == ["h1", "h2"]

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""

    def test_simple_no_trans(self):  # OK
        """
        n1;
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        gen_simple_evolution(nn1, cl_ds, None, reporter)

        expected = ["$not n1`, n1$", "$n1`, not n1$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("free clocks registered:", cl_ds.free_clocks)
        assert cl_ds.free_clocks == []

        print("reporter: ", reporter.mess)
        assert reporter.mess == ""


class TestFull(unittest.TestCase):
    """
    test full models
    """

    def test_model1(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        nn4 = root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event("h1")
        trans = root.add_transition(nn1, nn3)
        trans.set_event("h2")
        trans = root.add_transition(nn4, nn1)
        trans.set_event("h3")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        gt2clauses = GT2Clauses(cl_ds, False, reporter)
        model.accept(gt2clauses)
        expected = [
            "$not _lit0, h3$",
            "$not _lit0, n4$",
            "$not h3, not n4, _lit0$",
            "$n1, not _lit1$",
            "$not n4, not _lit1$",
            "$not n1, n4, _lit1$",
            "$not _lit2, h1$",
            "$not _lit2, _lit1$",
            "$not h1, not _lit1, _lit2$",
            "$not _lit3, h2$",
            "$not _lit3, n1$",
            "$not h2, not n1, _lit3$",
            "$_lit4, not _lit2$",
            "$_lit4, not _lit3$",
            "$_lit2, _lit3, not _lit4$",
            "$not n1`, _lit0, n1$",
            "$not n1`, _lit0, not _lit4$",
            "$n1`, not _lit0$",
            "$n1`, not n1, _lit4$",
            "$not n2`, _lit2, n2$",
            "$n2`, not _lit2$",
            "$n2`, not n2$",
            "$not n3`, _lit3, n3$",
            "$n3`, not _lit3$",
            "$n3`, not n3$",
            "$not n4`, n4$",
            "$not n4`, not _lit0$",
            "$n4`, not n4, _lit0$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("variables:", cl_ds.base_var_set)
        print("free clocks registered:", cl_ds.free_clocks)
        print("place_clocks:", cl_ds.place_clocks)
        print("inputs:", cl_ds.inputs)

        expected = {
            "n3", "h2", "h3", "h1", "_lit2", "_lit3", "n1", "_lit1", "_lit0",
            "n4", "n2", "_lit4",
        }
        assert cl_ds.base_var_set == expected
        assert cl_ds.free_clocks == ["h3", "h1", "h2"]
        assert cl_ds.place_clocks == {"h2": ["n1"], "h3": ["n4"], "h1": ["n1"]}
        assert cl_ds.inputs == []

    def test_model2(self):  # OK
        """
        n1 --> n2; h1 when n2 default h2[not n4]
        n1 --> n3; h2 when n4[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        nn3 = root.add_simple_node("n3", 0, 0)
        nn4 = root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event("h1 when n2 default h2")
        trans = root.add_transition(nn1, nn3)
        trans.set_event("h2 when n4")
        trans = root.add_transition(nn4, nn1)
        trans.set_event("h3")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        gt2clauses = GT2Clauses(cl_ds, reporter, False)
        model.accept(gt2clauses)

        expected = [
            "$not _lit0, h3$",
            "$not _lit0, n4$",
            "$not h3, not n4, _lit0$",
            "$n1, not _lit1$",
            "$not n4, not _lit1$",
            "$not n1, n4, _lit1$",
            "$not h1, not n2, _lit3$",
            "$not _lit3, h1$",
            "$not _lit3, n2$",
            "$not _lit2, _lit3, h2$",
            "$not _lit3, _lit2$",
            "$not h2, _lit2$",
            "$not _lit4, _lit2$",
            "$not _lit4, _lit1$",
            "$not _lit2, not _lit1, _lit4$",
            "$not h2, not n4, _lit5$",
            "$not _lit5, h2$",
            "$not _lit5, n4$",
            "$not _lit6, _lit5$",
            "$not _lit6, n1$",
            "$not _lit5, not n1, _lit6$",
            "$_lit7, not _lit4$",
            "$_lit7, not _lit6$",
            "$_lit4, _lit6, not _lit7$",
            "$not n1`, _lit0, n1$",
            "$not n1`, _lit0, not _lit7$",
            "$n1`, not _lit0$",
            "$n1`, not n1, _lit7$",
            "$not n2`, _lit4, n2$",
            "$n2`, not _lit4$",
            "$n2`, not n2$",
            "$not n3`, _lit6, n3$",
            "$n3`, not _lit6$",
            "$n3`, not n3$",
            "$not n4`, n4$",
            "$not n4`, not _lit0$",
            "$n4`, not n4, _lit0$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("variables:", cl_ds.base_var_set)
        print("free clocks registered:", cl_ds.free_clocks)
        print("place_clocks:", cl_ds.place_clocks)
        print("inputs:", cl_ds.inputs)

        expected = {
            "n3", "h2", "h3", "h1", "_lit6", "_lit7", "_lit2", "_lit3", "n1",
            "_lit1", "_lit0", "n4", "n2", "_lit5", "_lit4",
        }
        assert cl_ds.base_var_set == expected
        assert cl_ds.free_clocks == ["h3", "h1", "h2"]
        assert cl_ds.place_clocks == {"h3": ["n4"], "_lit5": ["n1"], "_lit2": ["n1"]}
        assert cl_ds.inputs == []

    def test_model3(self):  # OK
        """testInputCondEvent
        n4;
        n1/p --> n2; h[n4];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_perm_node("n1", 0, 0)
        nn2 = root.add_simple_node("n2", 0, 0)
        root.add_simple_node("n4", 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("n4")
        trans.set_event("h")

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, None)

        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)

        gt2clauses = GT2Clauses(cl_ds, reporter, False)
        model.accept(gt2clauses)

        expected = [
            "$not _lit0, h$",
            "$not _lit0, n4$",
            "$not h, not n4, _lit0$",
            "$not n2`, _lit0, n2$",
            "$n2`, not _lit0$",
            "$n2`, not n2$",
            "$not n4`, n4$",
            "$n4`, not n4$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("variables:", cl_ds.base_var_set)
        print("free clocks registered:", cl_ds.free_clocks)
        print("place_clocks:", cl_ds.place_clocks)
        print("inputs:", cl_ds.inputs)

        expected = {"h", "n2", "_lit0", "n4"}
        assert cl_ds.base_var_set == expected
        assert cl_ds.free_clocks == ["h"]
        assert cl_ds.place_clocks == {}
        assert cl_ds.inputs == []

    def test_constraints(self):
        """
        As it says
        """
        model = ChartModel("Test")
        root = model.get_root()
        aaa = root.add_simple_node("A", 0, 0)
        bbb = root.add_simple_node("B", 0, 0)
        ccc = root.add_simple_node("C", 0, 0)
        ddd = root.add_simple_node("D", 0, 0)
        trans = root.add_transition(aaa, bbb)
        trans.set_event("h1 default h2")
        trans = root.add_transition(ccc, ddd)
        trans.set_event("h3")
        cont = "synchro(h1, h3);exclus(h1, h2);included(h3, h2);"
        model.constraints = cont
        tvisit = TableVisitor(None)  # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        gt2clauses = GT2Clauses(cl_ds, reporter, False)
        model.accept(gt2clauses)

        expected = [
            "$not _lit0, h1, h2$",
            "$not h1, _lit0$",
            "$not h2, _lit0$",
            "$not _lit1, _lit0$",
            "$not _lit1, A$",
            "$not _lit0, not A, _lit1$",
            "$not A`, A$",
            "$not A`, not _lit1$",
            "$A`, not A, _lit1$",
            "$not B`, _lit1, B$",
            "$B`, not _lit1$",
            "$B`, not B$",
            "$not _lit2, h3$",
            "$not _lit2, C$",
            "$not h3, not C, _lit2$",
            "$not C`, C$",
            "$not C`, not _lit2$",
            "$C`, not C, _lit2$",
            "$not D`, _lit2, D$",
            "$D`, not _lit2$",
            "$D`, not D$",
            "$not h1, h3$",
            "$h1, not h3$",
            "$not h1, not h2$",
            "$not h3, h2$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

        print("variables:", cl_ds.base_var_set)
        print("free clocks registered:", cl_ds.free_clocks)
        print("place_clocks:", cl_ds.place_clocks)
        print("inputs:", cl_ds.inputs)

        expected = {"A", "C", "B", "D", "h2", "h3", "h1", "_lit2", "_lit1", "_lit0"}
        assert cl_ds.base_var_set == expected
        assert cl_ds.free_clocks == ["h1", "h2", "h3"]
        assert cl_ds.place_clocks == {"h3": ["C"], "_lit0": ["A"]}
        assert cl_ds.inputs == []

    def test_antlr_optimization(self):
        """Optimization gain comparison when using MCLTranslator optimizations
        for ANTLR translation (subexpression elimination)

        .. note:: Use test file instead of not provided:
            "../ucl/examples/test_tgfb_ref_300511.bcx"
        """
        rep = ErrorRep()

        mcla = MCLAnalyser(rep)
        mcla.translator_opti = False
        filename = pkg_resources.resource_filename(
            __name__,  # package name
            "../../guard_transitions/translators/tests/tgf_cano_noclock_cmp.cal",
        )
        mcla.build_from_cadlang(filename)
        nb_clauses_without_opti = len(mcla.dynamic_system.clauses)
        print("NB Clauses without opti:", nb_clauses_without_opti)

        mcla = MCLAnalyser(rep)
        filename = pkg_resources.resource_filename(
            __name__,  # package name
            "../../guard_transitions/translators/tests/tgf_cano_noclock_cmp.cal",
        )
        mcla.build_from_cadlang(filename)
        nb_clauses_with_opti = len(mcla.dynamic_system.clauses)
        print("NB Clauses with opti:", nb_clauses_with_opti)

        assert nb_clauses_with_opti < nb_clauses_without_opti
        assert nb_clauses_with_opti == 1573
        assert nb_clauses_without_opti == 1909


class TestMCLSigExprVisitor(unittest.TestCase):
    """
    Test of signal expression
    """

    def test_ident1(self):
        """
        sigexp = xx
        """
        sexpr = SigIdentExpr("xx")
        cl_ds = CLDynSys(None, None)
        sexpv = MCLSigExprVisitor(cl_ds, "Y", None)

        # Formula
        assert str(sexpr) == "xx"

        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "xx"
        # Clauses
        assert [str(clause) for clause in cl_ds.clauses] == []

    def test_bin1(self):
        """
        X or Y
        """
        sexpr1 = SigIdentExpr("x")
        sexpr2 = SigIdentExpr("y")
        sexpr = SigSyncBinExpr("or", sexpr1, sexpr2)

        # Formula
        assert str(sexpr) == "(x or y)"

        cl_ds = CLDynSys(None, None)
        sexpv = MCLSigExprVisitor(cl_ds, "Z", dict())
        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "Z"
        # Clauses
        expected = ["$not x, Z$", "$not y, Z$", "$x, y, not Z$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

    def test_bin2(self):
        """
        X and Y
        """
        sexpr1 = SigIdentExpr("x")
        sexpr2 = SigIdentExpr("y")
        sexpr = SigSyncBinExpr("and", sexpr1, sexpr2)

        # Formula
        assert str(sexpr) == "(x and y)"

        cl_ds = CLDynSys(None, None)
        sexpv = MCLSigExprVisitor(cl_ds, "Z", dict())
        sexpv.output_lit = None  # for output var generation
        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "_lit0"
        # Clauses
        expected = ["$x, not _lit0$", "$y, not _lit0$", "$not x, not y, _lit0$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

    def test_bin3(self):
        """
        h1 default h2
        """
        sexpr1 = SigIdentExpr("h1")
        sexpr2 = SigIdentExpr("h2")
        sexpr = SigDefaultExpr(sexpr1, sexpr2)

        # Formula
        assert str(sexpr) == "(h1 default h2)"

        symb_tab = dict()
        symb_tab["h1"] = ("clock", -1)
        symb_tab["h2"] = ("clock", -1)
        cl_ds = CLDynSys(symb_tab, None)
        sexpv = MCLSigExprVisitor(cl_ds, None)
        # sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "_lit0"
        # Clauses
        expected = ["$not _lit0, h1, h2$", "$not h1, _lit0$", "$not h2, _lit0$"]
        assert [str(clause) for clause in cl_ds.clauses] == expected

    def test_bin4(self):
        """
        h1 when (a or b)
        """
        sexpr1 = SigIdentExpr("h1")
        sexpr3 = SigIdentExpr("a")
        sexpr4 = SigIdentExpr("b")
        sexpr = SigSyncBinExpr("or", sexpr3, sexpr4)
        sexpr = SigWhenExpr(sexpr1, sexpr)

        # Formula
        assert str(sexpr) == "(h1 when (a or b))"

        symb_tab = dict()
        symb_tab["h1"] = ("clock", -1)
        cl_ds = CLDynSys(symb_tab, None)
        sexpv = MCLSigExprVisitor(cl_ds, None)
        # sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "_lit0"
        # Clauses
        expected = [
            "$not a, _lit1$",
            "$not b, _lit1$",
            "$a, b, not _lit1$",
            "$not h1, not _lit1, _lit0$",
            "$not _lit0, h1$",
            "$not _lit0, _lit1$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

    def test_cse1(self):
        """
        common subexpression elimination
        h1 when (a or b) default h2 when (b or a)
        """
        sexpr1 = SigIdentExpr("h1")
        sexpr2 = SigIdentExpr("h2")
        sexpr3 = SigIdentExpr("a")
        sexpr4 = SigIdentExpr("b")
        a_or_b1 = SigSyncBinExpr("and", sexpr3, sexpr4)
        a_or_b2 = SigSyncBinExpr("and", sexpr4, sexpr3)
        hh1 = SigWhenExpr(sexpr1, a_or_b1)
        hh2 = SigWhenExpr(sexpr2, a_or_b2)
        sexpr = SigDefaultExpr(hh1, hh2)

        # Formula
        assert str(sexpr) == "((h1 when (a and b)) default (h2 when (b and a)))"

        symb_tab = dict()
        symb_tab["h1"] = ("clock", -1)
        symb_tab["h2"] = ("clock", -1)
        cl_ds = CLDynSys(symb_tab, None)
        sub_exp = dict()
        sexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
        # sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "_lit0"
        # Clauses
        expected = [
            "$a, not _lit2$",
            "$b, not _lit2$",
            "$not a, not b, _lit2$",
            "$not h1, not _lit2, _lit1$",
            "$not _lit1, h1$",
            "$not _lit1, _lit2$",
            "$not h2, not _lit2, _lit3$",
            "$not _lit3, h2$",
            "$not _lit3, _lit2$",
            "$not _lit0, _lit1, _lit3$",
            "$not _lit1, _lit0$",
            "$not _lit3, _lit0$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected

    def test_cse2(self):
        """
        common subexpression elimination
        h1 when (a or b) default h2 when (b or a)
        """
        hh1 = SigIdentExpr("h1")
        hh2 = SigIdentExpr("h2")
        h12 = SigDefaultExpr(hh1, hh2)
        h21 = SigDefaultExpr(hh2, hh1)
        sexpr = SigDefaultExpr(h12, h21)

        # Formula
        assert str(sexpr) == "((h1 default h2) default (h2 default h1))"

        symb_tab = dict()
        symb_tab["h1"] = ("clock", -1)
        symb_tab["h2"] = ("clock", -1)
        cl_ds = CLDynSys(symb_tab, None)
        sub_exp = dict()
        sexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
        # sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)

        # Return aux var
        assert str(var) == "_lit0"
        # Clauses
        expected = [
            "$not _lit1, h1, h2$",
            "$not h1, _lit1$",
            "$not h2, _lit1$",
            "$not _lit0, _lit1, _lit1$",
            "$not _lit1, _lit0$",
            "$not _lit1, _lit0$",
        ]
        assert [str(clause) for clause in cl_ds.clauses] == expected
