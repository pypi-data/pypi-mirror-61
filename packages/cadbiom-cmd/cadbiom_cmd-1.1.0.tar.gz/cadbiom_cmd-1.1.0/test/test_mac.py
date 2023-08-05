# -*- coding: utf-8 -*-
"""Unit tests for solver results"""

#from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
import pytest
import tempfile
import os

# Custom imports
from cadbiom_cmd import solution_search

@pytest.yield_fixture()
def raw_feed_output():

    # setup
    # Create the file model in /tmp/
    # Note: prevent the deletion of the file after the close() call
    fd_model = tempfile.NamedTemporaryFile(suffix='.bcx', delete=False)
    fd_model.write(
        """<model xmlns="http://cadbiom" name="bicluster">
    <CSimpleNode name="Ax" xloc="0.156748911466" yloc="0.673568818514"/>
    <CSimpleNode name="n1" xloc="0.291727140784" yloc="0.673568818514"/>
    <CSimpleNode name="C1" xloc="0.404208998548" yloc="0.618757612668"/>
    <CSimpleNode name="n2" xloc="0.405660377359" yloc="0.722289890377"/>
    <CSimpleNode name="Px" xloc="0.577083086261" yloc="0.722140333368"/>
    <CSimpleNode name="Bx" xloc="0.157474600871" yloc="0.83922046285"/>
    <CSimpleNode name="n3" xloc="0.290570367401" yloc="0.803822907245"/>
    <CSimpleNode name="n4" xloc="0.292715433748" yloc="0.906099768906"/>
    <CSimpleNode name="C2" xloc="0.409124108889" yloc="0.803710739487"/>
    <CSimpleNode name="C3" xloc="0.408336298212" yloc="0.906099768906"/>
    <transition name="" ori="Ax" ext="n1" event="h00" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n1" ext="C1" event="h0" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n1" ext="n2" event="h1" condition="C2" action="" fact_ids="[]"/>
    <transition name="" ori="n2" ext="Px" event="hlast" condition="C1 and not C3" action="" fact_ids="[]"/>
    <transition name="" ori="Bx" ext="n3" event="h2" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="Bx" ext="n4" event="h4" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n3" ext="C2" event="h3" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n4" ext="C3" event="h5" condition="" action="" fact_ids="[]"/>
    </model>"""
    )
    fd_model.close()

    # fixture parameter
    yield (fd_model.name,
        (
            ['Ax Bx\n'],
            ['Ax Bx\n', '% h2\n', '% h00 h3\n', '% h0 h1\n', '% hlast\n'],
            ['4\n']
        )
    )

    # teardown
    # Delete temp files
    os.remove(fd_model.name)

@pytest.yield_fixture()
def simulate_mac_file():

    # setup
    mac_file = tempfile.NamedTemporaryFile(suffix='_mac.txt', delete=False)
    # Just frontier places
    mac_file.write("Ax Bx\nCx Dx\n")
    mac_file.close()

    # fixture parameter
    yield mac_file.name # Filename + path

    # teardown
    # Delete temp files
    os.remove(mac_file.name)

@pytest.yield_fixture()
def simulate_mac_complete_file():

    # setup
    mac_complete_file = tempfile.NamedTemporaryFile(suffix='_mac_complete.txt', delete=False)
    # 2 solutions: frontier places, then timings
    mac_complete_file.write("Ax Bx\n% h2\n% h00 h3\n% h0 h1\n% hlast\n")
    mac_complete_file.write("Cx Dx\n% h2\n% h00 h3\n")
    mac_complete_file.close()

    # fixture parameter
    yield mac_complete_file.name # Filename + path

    # teardown
    # Delete temp files
    os.remove(mac_complete_file.name)


def test_minigraph1(raw_feed_output):
    """Test the obtention of frontier places & timings on Minigraph 1

    Output must be:

        mac:
            Ax   Bx
        mac complete:
            Ax Bx
            % h2 h00  or h2
            % h3 or % h00 h3 ??
            % h0 h1
            % hlast
        mac step:
            4

    .. note:: Order of trajectories may change. (h2 h00, h3 vs h2, h3 h00)

    .. note:: This test is the equivalent of the following command line:

        cadbiom_cmd -vv debug compute_macs mini_test_publi.bcx Px --steps 10

    .. note:: The test directory is the temporary sytem folder.
    """

    fd_model_name = raw_feed_output[0]
    data = raw_feed_output[1]

    # Build params
    # See the docstring for the normal command line in shell context
    params = {
        'all_macs': False,
        'model_file': fd_model_name, # Filename + path
        'combinations': False,
        'continue': False,
        'final_prop': 'Px',
        'input_file': None,
        'inv_prop': None,
        'output': tempfile.gettempdir() + '/',
        'start_prop': None,
        'steps': 10,
        'verbose': 'debug',
        'limit': 400,
    }

    # Launch the search of the minimal accessibility condition
    solution_search.solutions_search(params)


    with open(fd_model_name[:-4] + "_Px_mac.txt", 'r') as file:
        found = [line for line in file]
        print("found mac:", found)
        assert found == data[0]

    with open(fd_model_name[:-4] + "_Px_mac_complete.txt", 'r') as file:
        found = [line for line in file]
        print("found mac_complete:", found)
        assert found == data[1]

    # Deprecated (mac_step.txt is no longer produced)
    #with open(fd_model.name[:-4] + "_Px_mac_step.txt", 'r') as file:
    #    print("found mac_step:", found)
    #    found = [line for line in file]
    #    assert found == data[2]


    # Delete temp files
    os.remove(fd_model_name[:-4] + "_Px_mac.txt")
    os.remove(fd_model_name[:-4] + "_Px_mac_complete.txt")
    #os.remove(fd_model_name[:-4] + "_Px_mac_step.txt")


def test_load_solutions(simulate_mac_file, simulate_mac_complete_file):

    from cadbiom_cmd.tools.solutions import load_solutions

    # Test solutions files parser
    # Note: this parser is not made for mac_files
    solutions = list(load_solutions(simulate_mac_file))
    expected = [('Ax Bx', []), ('Cx Dx', [])]
    print("found load_solutions mac_file", solutions)
    assert solutions == expected

    # Test solutions files parser
    solutions = list(load_solutions(simulate_mac_complete_file))
    print("found load_solutions mac_complete_file", solutions)
    expected = [
        ('Ax Bx', [['h2'], ['h00', 'h3'], ['h0', 'h1'], ['hlast']]),
        ('Cx Dx', [['h2'], ['h00', 'h3']])
    ]
    assert solutions == expected


def test_convert_solutions_to_json(raw_feed_output, simulate_mac_complete_file):

    from cadbiom_cmd.tools.solutions import load_solutions, convert_solutions_to_json
    from cadbiom_cmd.tools.models import get_transitions_from_model_file

    fd_model_name = raw_feed_output[0]

    # Get transitions from the model
    model_transitions, _ = get_transitions_from_model_file(fd_model_name)
    decomp_solutions = convert_solutions_to_json(
        load_solutions(simulate_mac_complete_file),
        model_transitions,
        conditions=True,
    )

    expected = [
        {'steps': [[{'transitions': [{'ext': 'n3', 'condition': u'', 'ori': 'Bx'}], 'event': 'h2'}],
        [{'transitions': [{'ext': 'n1', 'condition': u'', 'ori': 'Ax'}], 'event': 'h00'},
        {'transitions': [{'ext': 'C2', 'condition': u'', 'ori': 'n3'}], 'event': 'h3'}],
        [{'transitions': [{'ext': 'C1', 'condition': u'', 'ori': 'n1'}], 'event': 'h0'},
        {'transitions': [{'ext': 'n2', 'condition': u'', 'ori': 'n1'}], 'event': 'h1'}],
        [{'transitions': [{'ext': 'Px', 'condition': u'', 'ori': 'n2'}], 'event': 'hlast'}]],
        'solution': 'Ax Bx'},

        {'steps': [[{'transitions': [{'ext': 'n3', 'condition': u'', 'ori': 'Bx'}], 'event': 'h2'}],
        [{'transitions': [{'ext': 'n1', 'condition': u'', 'ori': 'Ax'}], 'event': 'h00'},
        {'transitions': [{'ext': 'C2', 'condition': u'', 'ori': 'n3'}], 'event': 'h3'}]],
        'solution': 'Cx Dx'}]

    print("found convert_solutions_to_json", decomp_solutions)
    assert decomp_solutions == expected


def test_get_all_macs(simulate_mac_file):

    from cadbiom_cmd.tools.solutions import get_mac_lines

    mac_lines = get_mac_lines(simulate_mac_file)
    print("found get_mac_lines", mac_lines)

    expected = {'Cx Dx', 'Ax Bx'}
    assert mac_lines == expected
