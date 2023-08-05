# -*- coding: utf-8 -*-
# Copyright (C) 2017  IRISA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
"""
Display, compare, and query a model


"""

from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
import datetime as dt
import networkx as nx
import networkx.algorithms.isomorphism as iso
import json
import csv
from urllib import quote as urllib_quote
# Remove matplotlib dependency
# It is used on demand during the drawing of a graph
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

# Library imports
from cadbiom.models.biosignal.sig_expr import *
from cadbiom.models.guard_transitions.translators.chart_xml \
    import MakeModelFromXmlFile
from cadbiom.models.guard_transitions.analyser.static_analysis import StaticAnalyzer

from tools.models import Reporter
from tools.models import get_transitions, \
                         get_frontier_places, \
                         get_model_identifier_mapping
from tools.models import get_places_data
from tools.graphs import build_graph, get_json_graph, export_graph, get_solutions_graph_data

import cadbiom.commons as cm

LOGGER = cm.logger()


def draw_graph(output_dir, solution, solution_index, G,
               transition_nodes, all_nodes,
               edges_in_cond, edges):
    """Draw graph with colors and export it svg file format.

    .. note:: Legend:

        - red: frontier places (in solution variable),
        - white: middle edges,
        - blue: transition edges

    :param output_dir: Output directory for GraphML files.
    :param solution: Solution string (mostly a set of frontier places).
    :param solution_index: Index of the solution in the Cadbiom result file
        (used to distinguish exported filenames).
    :param G: Networkx graph object.
    :param transition_nodes: Nodes corresponding to transitions with conditions.
        List of tuples: event, node
    :param all_nodes: All nodes in the model.
    :param edges_in_cond: Edges between transition node and nodes in condition
    :param edges: Normal transitions without condition.
    :type output_dir: <str>
    :type solution: <str>
    :type solution_index: <int> or <str>
    :type G: <networkx.classes.digraph.DiGraph>
    :type transition_nodes: <list>
    :type all_nodes: <list>
    :type edges_in_cond: <list>
    :type edges: <list>
    """

    creation_date = dt.datetime.now().strftime("%H-%M-%S")
    filename = "{}{}_{}_{}".format(
        output_dir, creation_date, solution_index, solution[:75]
    )

    # Drawing ##################################################################
    # draw_circular(G, **kwargs) On a circle.
    # draw_random(G, **kwargs)   Uniformly at random in the unit square.
    # draw_spectral(G, **kwargs) Eigenvectors of the graph Laplacian.
    # draw_spring(G, **kwargs)   Fruchterman-Reingold force-directed algorithm.
    # draw_shell(G, **kwargs)    Concentric circles.
    # draw_graphviz(G[, prog])   Draw networkx graph with graphviz layout.

    # Get a list of transition nodes (without dictionnary of attributes)
    transition_nodes_names = [node[0] for node in transition_nodes]

    pos = nx.circular_layout(G)

    # Legend of conditions in transition nodes
    f = plt.figure(1)
    ax = f.add_subplot(1,1,1)
    text = '\n'.join(transition_nodes_names)
    ax.text(0, 0, text, style='italic', fontsize=10,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

    # Draw nodes:
    # - red: frontier places (in solution variable),
    # - white: middle edges,
    # - blue: transition edges
    frontier_places  = set(solution.split(' '))
    def color_map(node):
        # print("color for:", node)
        if node in frontier_places: # Test first (see cond below)
            return 'red'
        if node in unziped_transition_nodes:
            return 'blue'
        if node in all_nodes: # some /all frontier places are in this set
            return 'grey'
        else:
            return 'white'

    # Color nodes
    colors = [color_map(node) for node in G.nodes_iter()]
    nx.draw(G, pos=pos, with_labels=True,
            node_color=colors, node_size=1000, alpha=0.5,
            ax=ax)

    # Draw edges involved in transitions with conditions
    edges_colors = [edge[2]['color'] for edge in edges_in_cond]
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_cond,
                           edge_color=edges_colors, width=2, alpha=0.5)

    # Draw labels for normal transitions (move pos to the end of the arrow)
    # ex: [('Ax', 'n1', {u'condition': u'', u'label': u'h00[]'}),]
    edges_labels = {(edge[0], edge[1]): edge[2]['label'] for edge in edges}
    nx.draw_networkx_edge_labels(G, pos, edges_labels, label_pos=0.3)

    # Save & show
    plt.legend()
    plt.savefig(filename + ".svg", format="svg")
    plt.show()


def test_main():
    """Test"""

    # chart_model.py
    # chart_xml.py
    parser = MakeModelFromXmlFile(BIO_MOLDELS_DIR + "mini_test_publi.bcx")
    print(type(parser.parser))
    print(dir(parser))
    print("HANDLER")
    print(dir(parser.handler))
    print(dir(parser.parser))
    print(dir(parser.model))
    print("ICI")
#    print(parser.model.get_simple_node())
    print(parser.handler.node_dict)
    print(parser.handler.top_pile)
    print(parser.handler.pile_dict)
    print(parser.handler.transition.event)
    print(type(parser.handler.top_pile))

    transitions = dict()
    for transition in parser.handler.top_pile.transitions:
        # print(type(transition)) => list
        for trans in transition:
            # 'action', 'activated', 'clean', 'clock', 'condition', 'event',
            # 'ext', 'ext_coord', 'fact_ids', 'get_influencing_places',
            # 'get_key', 'is_me', 'macro_node', 'name', 'note', 'ori',
            # 'ori_coord', 'remove', 'search_mark', 'selected', 'set_action',
            # 'set_condition', 'set_event', 'set_name', 'set_note'

# {'name': '', 'clock': None, 'selected': False, 'activated': False,
# 'search_mark': False, 'note': '', 'ext': <cadbiom.models.guard_transitions.chart_model.CSimpleNode object at 0x7f391c7406d0>,
# 'ext_coord': 0.0, 'ori': <cadbiom.models.guard_transitions.chart_model.CSimpleNode object at 0x7f391c740650>,
# 'action': u'', 'macro_node': <cadbiom.models.guard_transitions.chart_model.CTopNode object at 0x7f391c7db490>,
# 'ori_coord': 0.0, 'event': u'h5', 'condition': u'', 'fact_ids': []}
            # print(dir(trans))
            print("NEW trans", trans.event)
#            print(trans.__dict__)
#            print(trans.name, trans.clock, trans.selected, trans.activated,
#                  trans.search_mark, trans.note, trans.ext, trans.ext_coord,
#                  trans.ori, trans.action, trans.macro_node, trans.ori_coord,
#                  trans.event, trans.condition, trans.fact_ids
#                  )

            transitions[trans.event] = trans.condition

#print("ORI", trans.ori.__dict__)
#{'name': 'n4', 'yloc': 0.906099768906, 'selected': False,
#'father': <cadbiom.models.guard_transitions.chart_model.CTopNode object at 0x7f09eed91490>,
#'xloc': 0.292715433748, 'search_mark': False, 'was_activated': False,
#'incoming_trans': [<cadbiom.models.guard_transitions.chart_model.CTransition object at 0x7f09eecf67d0>],
#'model': <cadbiom.models.guard_transitions.chart_model.ChartModel object at 0x7f09ef2cf3d0>,
#'outgoing_trans': [<cadbiom.models.guard_transitions.chart_model.CTransition object at 0x7f09eecf6850>],
#'activated': False, 'hloc': 1.0}
            print("ORI", trans.ori.name)
            try:
                print("ori INCO", [(tr.event, tr.condition) for tr in trans.ori.incoming_trans])
            except: pass
            try:
                print("ori OUTGO", [(tr.event, tr.condition) for tr in trans.ori.outgoing_trans])
            except: pass
            print("EXT", trans.ext.name)
            try:
                print("ext INCO", [(tr.event, tr.condition) for tr in trans.ext.incoming_trans])
            except: pass
            try:
                print("ext OUTGO", [(tr.event, tr.condition) for tr in trans.ext.outgoing_trans])
            except: pass
    print(transitions)








def graph_isomorph_test(model_file_1, model_file_2, output_dir='graphs/',
                        make_graphs=False, make_json=False):
    """Entry point for model consistency checking.

    This functions checks if the graphs based on the two given models have
    the same topology, nodes & edges attributes/roles.

    .. todo:: This function should not write any file, and should be exported
        to the module tools.

    .. note:: Cf graphmatcher
        https://networkx.github.io/documentation/development/reference/generated/networkx.algorithms.isomorphism.categorical_edge_match.html

    :Use in scripts:

        .. code-block:: python

            >>> from cadbiom_cmd.models import graph_isomorph_test
            >>> print(graph_isomorph_test('model_1.bcx', 'model_2.bcx'))
            INFO: 3 transitions loaded
            INFO: 3 transitions loaded
            INFO: Build graph for the solution: Connexin_32_0 Connexin_26_0
            INFO: Build graph for the solution: Connexin_32_0 Connexin_26_0
            INFO: Topology checking: True
            INFO: Nodes checking: True
            INFO: Edges checking: True
            {'nodes': True, 'edges': True, 'topology': True}


    :param model_file_1: Filepath of the first model.
    :param model_file_2: Filepath of the second model.
    :key output_dir: Output path.
    :key make_graphs: If True, make a GraphML file in output path.
    :key make_json: If True, make a JSON dump of results in output path.
    :type model_file_1: <str>
    :type model_file_2: <str>
    :type output_dir: <str>
    :type make_graphs: <boolean>
    :type make_json: <boolean>
    :return: Dictionary with the results of tests.
        keys: 'topology', 'nodes', 'edges'; values: booleans
    :rtype: <dict <str>: <boolean>>
    """

    # Load transitions in the models
    # Transitions structure format:
    # {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    parser_1 = MakeModelFromXmlFile(model_file_1)
    parser_2 = MakeModelFromXmlFile(model_file_2)
    transitions_1 = get_transitions(parser_1)
    transitions_2 = get_transitions(parser_2)

    # Get all nodes
    all_places_1 = parser_1.handler.node_dict.keys()
    all_places_2 = parser_2.handler.node_dict.keys()

    # Get all frontier places in the models
    # (places that are never in output position in all transitions)
    # EDIT: why we use all_places from the model instead of
    # (input_places - output_places) to get frontier places ?
    # Because some nodes are only in conditions and not in transitions.
    # If we don't do that, these nodes are missing when we compute
    # valid paths from conditions.
    front_places_1 = " ".join(get_frontier_places(transitions_1, all_places_1))
    front_places_2 = " ".join(get_frontier_places(transitions_2, all_places_2))
    LOGGER.debug("Frontier places 1: " + str(front_places_1))
    LOGGER.debug("Frontier places 2: " + str(front_places_2))

    # Build graphs & get networkx object
    # We give all events in the model as a list of steps
    # So we simulate a cadbiom solution (with all events in the model).
    res_1 = build_graph(front_places_1, [transitions_1.keys()], transitions_1)
    G1 = res_1[0]
    res_2 = build_graph(front_places_2, [transitions_2.keys()], transitions_2)
    G2 = res_2[0]

    # Checking
    nm = iso.categorical_node_match('color', 'grey')
    em = iso.categorical_edge_match('color', '')

    check_state = \
    {
        'topology': nx.is_isomorphic(G1, G2),
        'nodes': nx.is_isomorphic(G1, G2, node_match=nm),
        'edges': nx.is_isomorphic(G1, G2, edge_match=em),
    }

    LOGGER.info("Topology checking: " + str(check_state['topology']))
    LOGGER.info("Nodes checking: " + str(check_state['nodes']))
    LOGGER.info("Edges checking: " + str(check_state['edges']))

    # Draw graph
    if make_graphs:
        export_graph(output_dir, front_places_1, "first", *res_1)
        export_graph(output_dir, front_places_2, "second", *res_2)

    # Export to JSON file
    if make_json:
        with open(output_dir + "graph_isomorphic_test.json", 'w') as fd:
            fd.write(json.dumps(check_state, sort_keys=True, indent=4) + '\n')

    return check_state


def low_graph_info(model_file, centralities):
    """Low level function for :meth:`~cadbiom_cmd.models.model_graph`.

    Get JSON data with information about the graph based on the model.

    .. seealso:: :meth:`tools.graphs.get_solutions_graph_data`.

    :param model_file: File for the model.
    :param centralities: If True with, compute centralities
        (degree, closeness, betweenness).
    :type model_file: <str>
    :type centralities: <boolean>
    :return: Dictionary with the results of measures on the given graph.
        keys: measure's name; values: measure's value

        :Example:

            .. code-block:: javascript

                {
                    'modelFile': 'string',
                    'modelName': 'string',
                    'events': int,
                    'entities': int,
                    'transitions': int,
                    'graph_nodes': int,
                    'graph_edges': int,
                    'centralities': {
                        'degree': {
                            'entity_1': float,
                            'entity_2': float
                        },
                        'strongly_connected': boolean,
                        'weakly_connected': boolean,
                        'max_degree': int,
                        'min_degree': int,
                        'average_degree': float,
                        'connected_components_number': int,
                        'connected_components': list,
                        'average_shortest_paths': int,
                    }
                }

    :rtype: <dict>, <tuple>, <str>
    """

    # Load transitions in the model
    # Transitions structure format:
    # {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    parser_1 = MakeModelFromXmlFile(model_file)
    transitions_1 = get_transitions(parser_1)
    # Get all nodes
    all_places_1 = parser_1.handler.node_dict.keys()
    # Get the model
    model = parser_1.handler.model

    # Get all frontier places in the models
    # (places that are never in output position in all transitions)
    # EDIT: why we use all_places from the model instead of
    # (input_places - output_places) to get frontier places ?
    # Because some nodes are only in conditions and not in transitions.
    # If we don't do that, these nodes are missing when we compute
    # valid paths from conditions.
    front_places = get_frontier_places(transitions_1, all_places_1)
    front_places_str = " ".join(front_places)
    LOGGER.debug("Frontier places 1: " + front_places_str)

    # Build graphs & get networkx object
    # We give all events in the model as a list of steps
    # So we simulate a cadbiom solution (with all events in the model).
    res_1 = build_graph(front_places_str, [transitions_1.keys()], transitions_1)
    G = res_1[0]

    info = {
        'modelFile': model_file,
        'modelName': model.name,
        'events:': len(transitions_1), # One event can have multiple transitions
        'entities': len(all_places_1), # places
        'boundaries': len(front_places), # frontier places
        'transitions': len(model.transition_list),
    }

    get_solutions_graph_data(G, info, centralities)

    LOGGER.info("%s", info)

    return info, res_1, front_places_str


def low_model_info(model_file,
                   all_entities=False, boundaries=False, genes=False, smallmolecules=False):
    """Low level function for :meth:`~cadbiom_cmd.models.model_info`.

    Get JSON data with information about the model and its entities.

    TODO: add dump of transitions (option)
    .. seealso:: Format de sortie de: :meth:`tools.solutions.convert_solutions_to_json`

    :param model_file: File for the model.
    :key all_entities: If True, data for all places of the model are returned
        (optional).
    :key boundaries: If True, only data for the frontier places of the model
        are returned (optional).
    :key genes: If True, only data for the genes of the model are returned
        (optional).
    :key smallmolecules: If True, only data for the smallmolecules of the model
        are returned (optional).
    :type model_file: <str>
    :type all_entities: <boolean>
    :type boundaries: <boolean>
    :type genes: <boolean>
    :type smallmolecules: <boolean>
    :return: Dictionary with informations about the model and the queried nodes.

        :Example:

            .. code-block:: javascript

                {
                    'modelFile': 'string',
                    'modelName': 'string',
                    'events': int,
                    'entities': int,
                    'boundaries': int,
                    'transitions': int,
                    'entitiesLocations': {
                        'cellular_compartment_a': int,
                        'cellular_compartment_b': int,
                        ...
                    },
                    'entitiesTypes': {
                        'biological_type_a': int,
                        'biological_type_b': int;
                        ...
                    },
                    'entitiesData': {
                        'cadbiomName': 'string',
                        'uri': 'string',
                        'entityType': 'string',
                        'entityRef': 'string',
                        'location': 'string',
                        'names': ['string', ...],
                        'xrefs': {
                            'external_database_a': ['string', ...],
                            'external_database_b': ['string', ...],
                            ...
                        }
                    }
                }

    :rtype: <dict>
    """

    # Load transitions in the model
    # Transitions structure format:
    # {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    parser_1 = MakeModelFromXmlFile(model_file)
    transitions_1 = get_transitions(parser_1)
    # Get all nodes
    all_places_1 = parser_1.handler.node_dict.keys()
    # Get the model
    model = parser_1.handler.model

    # Get all frontier places in the models
    # (places that are never in output position in all transitions)
    # EDIT: why we use all_places from the model instead of
    # (input_places - output_places) to get frontier places ?
    # Because some nodes are only in conditions and not in transitions.
    # If we don't do that, these nodes are missing when we compute
    # valid paths from conditions.
    front_places = get_frontier_places(transitions_1, all_places_1)

    # Basic informations
    info = {
        'modelFile': model_file,
        'modelName': model.name,
        'events:': len(transitions_1), # One event can have multiple transitions
        'entities': len(all_places_1),  # places
        'boundaries': len(front_places), # frontier places
        'transitions': len(model.transition_list),
    }

    # Complete the data with StaticAnalysis
    # Call custom Reporter instead of CompilReporter
    # from cadbiom_gui.gt_gui.utils.reporter import CompilReporter
    static_analyser = StaticAnalyzer(Reporter())
    static_analyser.build_from_chart_model(model)
    info['entitiesLocations'], info['entitiesTypes'] = \
        static_analyser.get_stats_entities_data()

    # Filter places
    if all_entities:
        info['entitiesData'] = get_places_data(all_places_1, model)

    if boundaries:
        info['entitiesData'] = get_places_data(front_places, model)

    if genes:
        g = (place_name for place_name in all_places_1 if '_gene' in place_name)
        info['entitiesData'] = get_places_data(g, model)

    if smallmolecules:
        # Filter on entityTypes
        info['entitiesData'] = \
            [data for data in get_places_data(all_places_1, model)
             if data["entityType"] == "SmallMolecule"]

    return info


def model_identifier_mapping(model_file, *args, **kwargs):
    """Entry point for the mapping of identifiers from external databases

    :param model_file: File for the model.
    :key external_file: File with 1 external identifier per line.
    :key external_identifiers: List of external identifiers to be mapped.
    :type model_file: <str>
    :type external_file: <str>
    :type external_identifiers: <list>
    """
    if kwargs.get('external_file', None):
        with open(kwargs['external_file'], 'r') as f_d:
            external_identifiers = set(line.strip('\n').strip('\r') for line in f_d)
    else:
        external_identifiers = set(kwargs['external_identifiers'])

    mapping = get_model_identifier_mapping(model_file, external_identifiers)

    # Make CSV file
    with open("mapping.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(';'))

        # Header
        writer.writerow(["external identifiers", "cadbiom identifiers"])

        # Join multiple Cadbiom names with a |
        g = ((external_id, "|".join(cadbiom_names))
             for external_id, cadbiom_names in mapping.iteritems())
        writer.writerows(g)


def model_graph(model_file, output_dir='./graphs/',
                centralities=False,
                **kwargs):
    """Get quick information and make a graph based on the model.

    :param model_file: File for the '.bcx' model.
    :param output_dir: Output directory.
    :param centralities: If True with ``--json``, compute centralities
        (degree, in_degree, out_degree, closeness, betweenness).

    :keyword graph: If True, make a GraphML file based on the graph maked
        from the model (optional).
    :keyword json: If True, make a JSON dump of results in output path(optional).

    :type model_file: <str>
    :type output_dir: <str>
    :type centralities: <boolean>
    :type graph: <boolean>
    :type json: <boolean>
    """

    # Bind arguments to avoid overwriting previous imports
    make_json = kwargs['json']
    make_graph = kwargs['graph']
    make_json_graph = kwargs['json_graph']

    # If json is not set, remove centralities parameter (time consuming)
    if not make_json:
        centralities = False

    model_graph_info, res_1, front_places_str = low_graph_info(
        model_file, centralities
    )


    # Make json graph
    if make_json_graph:
        # Pass a Networkx graph and get dictionary
        json_data = get_json_graph(res_1[0])
        with open(output_dir + "graph.json", 'w') as f_d:
            f_d.write(json.dumps(json_data, indent=2))

    # Draw graph
    if make_graph:
        export_graph(output_dir, front_places_str,
                   urllib_quote(model_graph_info['modelName'], safe=''),
                   *res_1)

    # Export to json file
    if make_json:
        with open(output_dir + "graph_summary.json", 'w') as f_d:
            f_d.write(
                json.dumps(model_graph_info, sort_keys=True, indent=2) + '\n'
            )


def model_info(model_file, output_dir='./',
               all_entities=False, boundaries=False,
               genes=False, smallmolecules=False, default=True, **kwargs):
    """Get quick and full informations about the model structure and places.

    :param model_file: File for the '.bcx' model.
    :key output_dir: Output directory.
    :key all_entities: If True, data for all places of the model are returned
        (optional).
    :key boundaries: If True, only data for the frontier places of the model
        are returned (optional).
    :key genes: If True, only data for the genes of the model are returned
        (optional).
    :key smallmolecules: If True, only data for the smallmolecules of the model
        are returned (optional).
    :key default: Display quick description of the model
        (Number of places, transitions, entities types, entities locations).

    :key json: If True, make a JSON dump of results in output path(optional).
    :key csv: If True, make a csv dump of informations about filtered places.

    :type model_file: <str>
    :type output_dir: <str>
    :type all_entities: <boolean>
    :type boundaries: <boolean>
    :type genes: <boolean>
    :type smallmolecules: <boolean>
    :type default: <boolean>
    :type json: <boolean>
    :type csv: <boolean>
    """

    # Bind arguments to avoid overwriting previous imports
    make_json = kwargs['json']
    make_csv = kwargs['csv']

    def dump_places_to_csv(places, output_filename):
        """Write informations about places in the model to a csv."""
        with open(output_filename, 'w') as csvfile:
            # Get all database names
            database_names = \
                {db_name for place in places
                 for db_name in place.get('xrefs', dict()).iterkeys()}

            # Write headers
            fieldnames = ("cadbiomName", "names", "uri", "entityType",
                "entityRef", "location") + tuple(database_names)
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                extrasaction='ignore', # Ignore keys not found in fieldnames (xrefs)
            )
            writer.writeheader()

            for place in places:
                # Since we modify places, we need to make a copy in memory
                temp_place = place.copy()
                # Join names with a pipe...
                # Handle escaped unicode characters in model
                # Ex: \u03b2-catenin => β-Catenin
                temp_place['names'] = "|".join(place.get('names', list())).encode("utf-8")
                # Join xrefs ids with a pipe...
                for db_name, db_ids in place.get('xrefs', dict()).iteritems():
                    temp_place[db_name] = "|".join(db_ids).encode("utf-8")

                writer.writerow(temp_place)


    def get_output_filename(filetype="csv"):
        """Return the filename according to the given filters and filetype."""
        if all_entities:
            return "all_entities." + filetype
        if boundaries:
            return "boundaries." + filetype
        if genes:
            return "genes." + filetype
        if smallmolecules:
            return "smallmolecules." + filetype


    if default:
        # Call custom Reporter instead of CompilReporter
        # from cadbiom_gui.gt_gui.utils.reporter import CompilReporter
        static_analyser = StaticAnalyzer(Reporter())
        static_analyser.build_from_chart_file(model_file)
        print(static_analyser.get_statistics())
        return

    model_info = low_model_info(
        model_file,
        all_entities, boundaries, genes, smallmolecules
    )

    # Export to csv file
    if make_csv:
        dump_places_to_csv(model_info['entitiesData'], output_dir + get_output_filename())

    # Export to json file
    if make_json:
        with open(output_dir + "model_summary_" + get_output_filename("json"), 'w') as f_d:
            # Handle escaped unicode characters in model
            # Ex: \u03b2-catenin => β-Catenin
            f_d.write(
                json.dumps(model_info, sort_keys=True, indent=2, ensure_ascii=False).encode('utf8')
            )
