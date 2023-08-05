# -*- coding: utf-8 -*-
"""Unit tests for Python API"""

from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
import os
import tempfile
import pytest


@pytest.yield_fixture()
def feed_SCC_model():
    """Fixture for a Cadbiom model with 4 Strongly Connected Components

    :return: A list of SCC, the corrected model with start nodes inserted
        and the original model with SCC.
    :rtype: <tuple <list>, <str>, <NamedTemporaryFile>>
    """

    scc = [["I", "K", "J", "L"], ["Y", "X", "Z"]]
    model_without_scc = """<?xml version = "1.0" encoding="ASCII" standalone="yes" ?>
<model xmlns="http://cadbiom" name="">
  <CSimpleNode name="A"/>
  <CSimpleNode name="B"/>
  <CSimpleNode name="E"/>
  <CSimpleNode name="D"/>
  <CSimpleNode name="C"/>
  <CSimpleNode name="Y"/>
  <CSimpleNode name="X"/>
  <CSimpleNode name="Z"/>
  <CSimpleNode name="I"/>
  <CSimpleNode name="K"/>
  <CSimpleNode name="J"/>
  <CSimpleNode name="L"/>
  <CStartNode name="__start__0"/>
  <CStartNode name="__start__1"/>
  <CMacroNode name="default_name_1" xloc="0.548920863309" yloc="0.589680589681" wloc="0.3" hloc="0.3">
    <CSimpleNode name="A_1" xloc="0.0458033573137" yloc="0.364864864865"/>
    <CSimpleNode name="B_1" xloc="0.30071942446" yloc="0.623259623259"/>
    <transition ori="A_1" ext="B_1" event="h_1" condition=""/>
  </CMacroNode>
  <transition ori="I" ext="J" event="" condition=""/>
  <transition ori="L" ext="I" event="" condition=""/>
  <transition ori="K" ext="L" event="" condition=""/>
  <transition ori="X" ext="Z" event="" condition=""/>
  <transition ori="__start__1" ext="X" event="" condition=""/>
  <transition ori="J" ext="K" event="" condition=""/>
  <transition ori="B" ext="D" event="" condition=""/>
  <transition ori="A" ext="B" event="" condition="C"/>
  <transition ori="X" ext="C" event="" condition=""/>
  <transition ori="C" ext="B" event="" condition="A"/>
  <transition ori="I" ext="K" event="" condition=""/>
  <transition ori="D" ext="C" event="" condition=""/>
  <transition ori="J" ext="B" event="" condition=""/>
  <transition ori="__start__0" ext="I" event="" condition=""/>
  <transition ori="Y" ext="X" event="" condition=""/>
  <transition ori="Z" ext="Y" event="" condition=""/>
  <transition ori="D" ext="E" event="" condition=""/>
</model>
"""

    # Create the original file model in /tmp/
    # Note: prevent the deletion of the file after the close() call
    fd_model = tempfile.NamedTemporaryFile(suffix=".bcx", delete=False)
    fd_model.write(
        """<model xmlns="http://cadbiom" name="">
    <CSimpleNode name="A"/>
    <CSimpleNode name="B"/>
    <CSimpleNode name="E"/>
    <CSimpleNode name="D"/>
    <CSimpleNode name="C"/>
    <CSimpleNode name="Y"/>
    <CSimpleNode name="X"/>
    <CSimpleNode name="Z"/>
    <CSimpleNode name="I"/>
    <CSimpleNode name="K"/>
    <CSimpleNode name="J"/>
    <CSimpleNode name="L"/>
    <CMacroNode yloc="0.589680589681" hloc="0.3" wloc="0.3" name="default_name_1" xloc="0.548920863309">
      <CSimpleNode yloc="0.364864864865" name="A_1" xloc="0.0458033573137"/>
      <CSimpleNode yloc="0.623259623259" name="B_1" xloc="0.30071942446"/>
      <transition ext="B_1" ori="A_1" action="" event="h_1" condition=""/>
    </CMacroNode>
    <transition name="" ori="A" ext="B" event="" condition="C"/>
    <transition name="" ori="B" ext="D" event="" condition=""/>
    <transition name="" ori="C" ext="B" event="" condition="A"/>
    <transition name="" ori="D" ext="C" event="" condition=""/>
    <transition name="" ori="D" ext="E" event="" condition=""/>
    <transition name="" ori="Z" ext="Y" event="" condition=""/>
    <transition name="" ori="Y" ext="X" event="" condition=""/>
    <transition name="" ori="X" ext="Z" event="" condition=""/>
    <transition name="" ori="X" ext="C" event="" condition=""/>
    <transition name="" ori="I" ext="J" event="" condition=""/>
    <transition name="" ori="L" ext="I" event="" condition=""/>
    <transition name="" ori="K" ext="L" event="" condition=""/>
    <transition name="" ori="J" ext="K" event="" condition=""/>
    <transition name="" ori="J" ext="B" event="" condition=""/>
    <transition name="" ori="I" ext="K" event="" condition=""/>
    </model>"""
    )
    fd_model.close()

    yield scc, model_without_scc, fd_model

    # Tear down
    os.remove(fd_model.name)


def test_SCC_search(feed_SCC_model):
    """Test the correction of a model by removing Strongly Connected Components

    - We add a start node for every SCC
    - We add a transition between the start node and the smallest node of every
    SCC (sorted in lexicogrpahic order)

    Moreover, we:
    - Add xml preamble in the model,
    - Check the order of attributes of xml elements,
    - Check import/export of a model with a macro node.

    Keep in mind that by testing the result of the export of a model, we also
    test its content...
    """

    import cadbiom.models.guard_transitions.analyser.model_corrections as mc

    _, model_without_scc, model_with_scc = feed_SCC_model

    # Make a new model file (with "_without_scc" suffix in filename)
    mc.add_start_nodes(model_with_scc.name)  # Filename + path

    expected_lines = set(model_without_scc.split("\n"))

    filepath = model_with_scc.name[:-4] + "_without_scc.bcx"
    with open(filepath, "r") as file:
        found_lines = set(file.read().split("\n"))
        assert found_lines == expected_lines

    os.remove(filepath)
