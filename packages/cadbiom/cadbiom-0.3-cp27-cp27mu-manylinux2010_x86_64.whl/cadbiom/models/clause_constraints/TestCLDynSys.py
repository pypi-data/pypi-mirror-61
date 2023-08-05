# -*- coding: utf-8 -*-
"""Unit tests for CLDynSys"""

from __future__ import unicode_literals
from __future__ import print_function
import pytest

from cadbiom.models.clause_constraints.CLDynSys import Literal, Clause

@pytest.fixture()
def feed_literals():

    l1 = Literal("A", True)
    l2 = Literal("A", False)
    l3 = Literal("B", False)
    l4 = Literal("B", False)

    return l1, l2, l3, l4

@pytest.fixture()
def feed_clauses(feed_literals):

    l1, l2, l3, l4 = feed_literals

    clause1 = Clause([l1, l2, l3])
    clause2 = Clause([l1, l3, l2])
    clause3 = Clause([l1, l2])

    return clause1, clause2, clause3


def test_literals(feed_literals):

    l1, l2, l3, l4 = feed_literals

    # Assignment and representation
    expected = "A"
    assert str(l1) == expected

    expected = "not A"
    assert str(l2) == expected

    expected = "_A"
    assert l2.code_name() == expected

    # Equality
    assert l1 != l2
    found = l1 == l2
    assert found == False

    assert l3 == l4
    found = (l3 != l4)
    print((l3 != l4), (l3 == l4))
    assert found == False

    expected = True
    assert l1.opposite(l2) == expected


def test_clauses(feed_literals, feed_clauses):

    l1, l2, l3, l4 = feed_literals

    clause1, clause2, clause3 = feed_clauses

    # Equality
    assert clause1 == clause2
    found = (clause1 != clause2)
    assert found == False

    # Length
    assert clause1 != clause3
    assert clause1 > clause3
    #assert clause1 >= clause3
    found = clause1 < clause3
    assert found == False

