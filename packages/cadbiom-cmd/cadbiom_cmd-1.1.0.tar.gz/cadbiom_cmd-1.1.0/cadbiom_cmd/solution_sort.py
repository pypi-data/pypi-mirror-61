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
"""Handle generated files

This module provides some functions to do some analyzis on the output
files of Cadbiom.

Entry points:

    * :meth:`~cadbiom_cmd.solution_sort.queries_2_json`
    * :meth:`~cadbiom_cmd.solution_sort.solutions_2_graphs`
    * :meth:`~cadbiom_cmd.solution_sort.solutions_2_common_graph`

:Example of the content of a complete solution file:

    .. code::

        Bx  Ax
        % h2 h00
        % h3
        % h0 h1
        % hlast
        Bx  Ax
        % h2
        % h3 h00
        % h0 h1
        %
        % hlast
        Bx  Ax
        % h2
        % h3 h00
        % h0 h1
        % hlast
        %
        %
        Bx  Ax
        % h2 h00
        % h3
        % h0 h1
        % hlast
        %
        %
        %

"""
from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
from collections import defaultdict, Counter
import itertools as it
import json
import os
import glob
import csv

# Library imports

from tools.solutions import get_solutions
from tools.models import get_transitions_from_model_file
from tools.solutions import load_solutions, convert_solutions_to_json, \
    get_query_from_filename, get_mac_lines
from tools.graphs import export_graph, build_graph, merge_graphs, get_solutions_graph_data

import cadbiom.commons as cm

LOGGER = cm.logger()

## Sort functions ##############################################################

def sort_solutions_in_file(filepath):
    """Sort all solutions in the given file in alphabetical order.

    .. warning:: The file is modified in place.

    :param: Filepath to be opened and in which solutions will be sorted.
    :arg: <str>
    """

    solutions = dict()

    with open(filepath, 'r+') as f_d:

        # Get old line as key and ordered line as value
        for line, stripped_line in get_solutions(f_d):
            # Sort in lower case, remove ' ' empty elements
            solutions[line] = \
                " ".join(sorted([place for place in stripped_line.split(' ')
                                 if place != ' '], key=lambda s: s.lower()))

        # Rewind the whole file
        f_d.seek(0)

        # Load all the content
        file_text = f_d.read()

        # Replace old sols with the new ones
        for original_sol, sorted_sol in solutions.items():
            file_text = file_text.replace(original_sol, sorted_sol)

        # Rewind the whole file
        f_d.seek(0)

        # Write all text in the current opened file
        f_d.write(file_text)


def solutions_sort(path):
    """Entry point for sorting solutions.

    Read a solution(s) file(s) (\*mac\* files) and sort all
    frontier places/boundaries in alphabetical order.

    This functions tests if the given path is a directory or a file.

    .. warning:: The files will be modified in place.

    :param: Filepath or directory path containing Cadbiom solutions.
    :type: <str>
    """

    # Check valid input file/directory
    assert os.path.isfile(path) or os.path.isdir(path)

    if os.path.isdir(path):
        # Recursive search of *mac* files
        # (mac.txt, mac_complete.txt, mac_step.txt)
        path = path if path[-1] == '/' else path + '/'
        [sort_solutions_in_file(file) for file in glob.glob(path + '*mac*')]
    else:
        sort_solutions_in_file(path)

## Conversion functions ########################################################

def write_json(output_dir, file_path, file_suffix, data):
    """Write decompiled solutions to a JSON formated file

    Called by :meth:`queries_2_json TODO` and  :meth:`queries_2_common_graph`

    :param output_dir: Output directory
    :param file_path: Filepath of the original solution file.
        We extract the basename in order to name the JSON file.
    :param file_suffix: String added to the solution filename.
        Ex: filename + file_suffix + ".json"
    :param data: Data to be serialized in JSON
    :type output_dir: <str>
    :type file_path: <str>
    :type file_suffix: <str>
    :type data: <list> or <dict> or <whatever>
    """
    # Add file_suffix to the solution filename
    filename = os.path.basename(os.path.splitext(file_path)[0])

    with open(output_dir + filename + file_suffix + '.json', 'w') as f_d:
        json.dump(data, f_d, sort_keys=True, indent=2)

## query - json
def queries_2_json(output_dir, model_file, path, conditions=True):
    """Entry point for queries_2_json

    Create a JSON formated file containing all data from complete MAC files
    (\*mac_complete files). The file will contain frontier places/boundaries
    and decompiled steps with their respective events for each solution.

    This is a function to quickly search all transition attributes involved
    in a solution.

    This functions tests if the given path is a directory or a file.

    :param output_dir: Output path.
    :param model_file: Filepath of the model.
    :param path: Filepath/directory of a complete solution file.
    :param conditions: (Optional) If False, conditions of transitions will not
        be present in the JSON file. This allows to have only places/entities
        used inside trajectories; thus, inhibitors are avoided.
    :type output_dir: <str>
    :type model_file: <str>
    :type path: <str>
    :type conditions: <boolean>
    """
    # Check valid input file/directory
    assert os.path.isfile(path) or os.path.isdir(path)

    # Get transitions from the model
    model_transitions, _ = get_transitions_from_model_file(model_file)

    if os.path.isfile(path):
        # The given path is a solution file
        decomp_solutions = convert_solutions_to_json(
            load_solutions(path),
            model_transitions,
            conditions=conditions,
        )
        write_json(output_dir, path, "_decomp", decomp_solutions)

    elif os.path.isdir(path):
        # The given path is a directory
        path = path if path[-1] == '/' else path + '/'

        # Decompilation of all files in the directory
        file_number = 0
        for file_number, solution_file in \
            enumerate(glob.glob(path + '*mac_complete.txt'), 1):

            decomp_solutions = convert_solutions_to_json(
                load_solutions(solution_file),
                model_transitions,
                conditions=conditions,
            )
            write_json(solution_file, path, "_decomp", decomp_solutions)

        LOGGER.info("Files processed: %s", file_number)
        assert file_number != 0, "No *mac_complete.txt files found!"

################################################################################

def solutions_2_graphs(output_dir, model_file, path):
    """Entry point for solutions_2_graphs

    Create GraphML formated files containing a representation of the
    trajectories for each solution in complete MAC files (\*mac_complete files).

    This is a function to visualize paths taken by the solver from the boundaries
    to the entities of interest.

    This functions tests if the given path is a directory or a file.

    :param output_dir: Output path.
    :param model_file: Filepath of the model.
    :param path: Filepath/directory of a/many complete solutions files.
    :type output_dir: <str>
    :type model_file: <str>
    :type path: <str>
    """

    # Check valid input file/directory
    assert os.path.isfile(path) or os.path.isdir(path)

    # Get transitions from the model
    model_transitions, _ = get_transitions_from_model_file(model_file)

    if os.path.isfile(path):
        # The given path is a solution file
        save_solutions_to_graphs(
            output_dir,
            load_solutions(path),
            model_transitions
        )

    elif os.path.isdir(path):
        # The given path is a directory
        path = path if path[-1] == '/' else path + '/'

        # Decompilation of all files in the directory
        file_number = 0
        for file_number, solution_file in \
            enumerate(glob.glob(path + '*mac_complete.txt'), 1):

            save_solutions_to_graphs(
                output_dir,
                load_solutions(solution_file),
                model_transitions
            )

        LOGGER.info("Files processed: %s", file_number)
        assert file_number != 0, "No *mac_complete.txt files found!"


def save_solutions_to_graphs(output_dir, sol_steps, transitions):
    """Build and export graphs based on the given solutions

    Each solution is composed of a set of frontier places and steps,
    themselves composed of events.
    We construct a graph based on the transitions that occur in the composition
    of the events of the given solution.

    :param output_dir: Output path.
    :param sol_steps: A generator of tuples of "frontier places" and a list of
        events in each step.

        :Example:

            .. code-block:: python

                ("Bx Ax", [['h2', 'h00'], ['h3'], ['h0', 'h1'], ['hlast']])

    :param transitions: A dictionnary of events as keys, and transitions as values.
        Since many transitions can define an event, values are lists.
        Each transition is a tuple with: origin node, final node, attributes
        like label and condition.

        :Example:

            .. code-block:: python

                {'h00': [('Ax', 'n1', {'label': 'h00[]'}),]

    :type output_dir: <str>
    :type sol_steps: <tuple <str>, <list>>
    :type transitions: <dict <list <tuple <str>, <str>, <dict <str>: <str>>>>
    """

    for sol_index, (sol, steps) in enumerate(sol_steps):

        # build_graph() returns :
        # G, transition_nodes, all_nodes, edges_in_cond, edges
        # sol_index is used to order files according to the order of appearance
        # in the file
        export_graph(output_dir, sol, sol_index,
                     build_graph(sol, steps, transitions)[0])

################################################################################

def get_solution_graphs(sol_steps, transitions):
    """Generator that yields the graphs of the given solutions.

    .. note:: See the doc of a similar function
        :meth:`~cadbiom_cmd.solution_sort.save_solutions_to_graphs`.
    """
    for sol, steps in sol_steps:
        # build_graph() returns :
        # G, transition_nodes, all_nodes, edges_in_cond, edges
        # Python 3: partial unpacking: G, *_
        yield build_graph(sol, steps, transitions)[0]


def queries_2_common_graph(output_dir, model_file, path,
                           make_graphs=True, make_csv=False, make_json=False,
                           *args, **kwargs):
    """Entry point for solutions_2_common_graph

    Create a GraphML formated file containing a unique representation of **all**
    trajectories corresponding to all solutions in each complete MAC files
    (\*mac_complete files).

    This is a function to visualize paths taken by the solver from the boundaries
    to the entities of interest.

    CSV fields::

        - query
        - solutions: nb trajectories/solutions
        - boundaries
        - events
        - genes
        - Protein
        - Complex
        - influencing_places
        - graph_nodes
        - graph_nodes_places
        - graph_edges
        - strongly_connected
        - max_degree
        - min_degree
        - average_degree

    .. note:: This functions tests if the given path is a directory or a file.

    :param output_dir: Output path.
    :param model_file: Filepath of the model.
    :param path: Filepath/directory of a/many complete solutions files.
    :key make_graphs: (optional) Make a GraphML for each query results in path.
        default: True
    :key make_csv: (optional) Make a **global** CSV for all query results in path.
        default: False
    :key make_json: (optional) Make a JSON dump of each query results in path.
        default: False
    :type output_dir: <str>
    :type model_file: <str>
    :type path: <str>
    :type make_graphs: <boolean>
    :type make_csv: <boolean>
    :type make_json: <boolean>
    """

    def write_csv(data):
        """Write given data in CSV file; then flush the file descriptor

        .. note:: data is modified in place.

        :param data: Data to be serialized in JSON.
        """
        # Handle nested dictionaries by flattening them
        data.update({
            sub_key: sub_val
            for key, val in data.items() if isinstance(val, dict)
            for sub_key, sub_val in val.items()
        })

        writer.writerow(data)
        f_d.flush()


    def do_magic(solution_file):
        # Get query string from the name of the solution file
        query = get_query_from_filename(model_file, solution_file)

        LOGGER.info("Processing %s query...", query)

        # generator of ("Ax Bx", [['h2', 'h00'], ['h3'], ['h0', 'h1'], ['hlast']])
        solutions = tuple(load_solutions(solution_file))
        graphs = get_solution_graphs(
            solutions,
            model_transitions
        )
        # Get common graph
        graph = merge_graphs(graphs)

        if make_graphs:
            # Write graph
            export_graph(output_dir, query, '', graph)

        if make_json or make_csv:
            # Export to json file (similaire à model_graph_info() ...)

            # Get 2 lists: 1: frontiers; 2: events
            unzipped_solutions = list(zip(*solutions))
            # Frontiers
            frontiers = set(it.chain(*[sol.split() for sol in unzipped_solutions[0]]))
            # Events
            events = set(it.chain(*it.chain(*unzipped_solutions[1])))
            # Genes
            # brutal but effective as long as the nodes of a model do not have
            # the information in hard in one of their attributes
            genes = {name for name in frontiers if "_gene" in name}

            # Influencing frontier places
            g = (trans.get_influencing_places() for trans in parser.model.transition_list if trans.event in events)
            influencing_places = frontiers & set(it.chain(*g))

            # Get frontier types
            # Do not count genes entities that are "virtual" types
            g = (parser.model.node_dict[name] for name in frontiers - genes)
            # Remove nodes with empty notes
            frontier_types = Counter([
                json.loads(node.note).get("entityType", "UKN") for node in g
                if node.note
            ])

            solutions_info = {
                'modelFile': model_file,
                'query': query,
                'solutions': len(solutions),  # nb trajectories/solutions
                'boundaries': len(frontiers),
                'events': len(events),
                'genes': len(genes),
                'influencing_places': len(influencing_places),
                'entityTypes': frontier_types,
            }
            # Advanced metrics
            get_solutions_graph_data(graph, solutions_info, True)
            LOGGER.debug("%s", solutions_info)

            if make_json:
                # Save to <solution_filename>_graph_summary.json
                write_json(output_dir, solution_file, "_graph_summary", solutions_info)

            if make_csv:
                # Export to csv graphs_summary.csv
                write_csv(solutions_info)


    # Check valid input file/directory
    assert os.path.isfile(path) or os.path.isdir(path)

    # Bind arguments to avoid overwriting previous imports
    make_graphs = kwargs['graphs']
    make_json = kwargs['json']
    make_csv = kwargs['csv']

    # Get transitions from the model
    model_transitions, parser = get_transitions_from_model_file(model_file)


    if make_csv:
        # Init the CSV file now
        f_d = open(output_dir + 'graphs_summary.csv', 'w')
        # Get a subset of solutions_info keys as fieldnames
        writer = csv.DictWriter(
            f_d,
            [
                "query", "solutions", "boundaries", "events", "genes",
                "Protein", "Complex", "influencing_places",
                "graph_nodes", "graph_nodes_places", "graph_edges",
                "strongly_connected",
                "max_degree", "min_degree", "average_degree",
            ],
            extrasaction="ignore",  # Ignore unknown fieldnames
            restval=0,  # Value for missing fieldnames
            delimiter=str(';'),
        )
        writer.writeheader()


    # File management...
    if os.path.isfile(path):
        # The given path is a solution file
        do_magic(path)

    elif os.path.isdir(path):
        # The given path is a directory
        path = path if path[-1] == '/' else path + '/'

        # Decompilation of all files in the directory
        file_number = 0
        for file_number, solution_file in \
                enumerate(glob.glob(path + '*mac_complete.txt'), 1):

            do_magic(solution_file)

        LOGGER.info("Files processed: %s", file_number)
        assert file_number != 0, "No *mac_complete.txt files found!"


    if make_csv:
        # Close the CSV file descriptor
        f_d.close()

## Matrices of occurrences #####################################################

def queries_2_occcurrence_matrix(output_dir, model_file, path,
                                    transposed=False, normalized=False):
    """Entry point for queries_2_occcurrence_matrix

    See :meth:`~cadbiom_cmd.solution_sort.occurrence_matrix`.

    :param output_dir: Output path.
    :param model_file: Filepath of the model.
    :param path: Directory of many complete solutions files.
    :param transposed: (Optional) Transpose the final matrix (switch columns and rows).
    :type output_dir: <str>
    :type model_file: <str>
    :type path: <str>
    :type transposed: <boolean>
    """

    # Check valid input directory
    assert os.path.isdir(path)

    path = path if path[-1] == '/' else path + '/'

    # Make matrix
    occurrence_matrix(output_dir, model_file, path)

    if transposed:
        transpose_csv(input_file=output_dir + 'occurrence_matrix.csv',
                      output_file=output_dir + 'occurrence_matrix_t.csv')


def occurrence_matrix(output_dir, model_file, path,
                     matrix_filename='occurrence_matrix.csv'):
    """Make a matrix of occurrences for the solutions in the given path.

    - Compute occurrences of each place in all `mac.txt` files.
    - Save the matrix in csv format with the following columns:
        Fieldnames: "patterns (number)/places (number);mac_number;frontier places"
        Each request (pattern) is accompanied by the number of solutions found.

    .. todo:: Split the creation and writing of the matrix in 2 functions.

    :param output_dir: Output path.
    :param model_file: Filepath of the model.
    :param path: Directory of many complete solutions files.
    :param matrix_filename: (Optional) Filename of the matrix file.
    :type output_dir: <str>
    :type model_file: <str>
    :type path: <str>
    :type matrix_filename: <str>
    :return: A dictionnary with the matrix object.
        keys: queries, values: occurrences of frontier places
    :rtype: <dict>
    """

    # Key: Logical formula as input of Cadbiom
    # Value: Number of each place in all solutions of the current file
    matrix = defaultdict(Counter)
    # All frontier places in all mac files
    all_frontier_places = set()

    # Compute occurrences of each place in all mac files
    file_number = 0
    for file_number, filepath in enumerate(glob.glob(path + '*mac.txt'), 1):

        # gene pattern
#        pattern = {gene for gene in genes if gene in mac}

        # Get query string from the name of the solution file
        # From: 'MODEL_NAME_PLACE1 and not PLACE2 and not PLACE3_mac.txt'
        # Get: 'PLACE1 and not PLACE2 and not PLACE3'
        query = get_query_from_filename(model_file, filepath)

        mac_number = 0
        for mac_number, mac_line in enumerate(get_mac_lines(filepath), 1):

            frontier_places = set(mac_line.split(' '))
            # Update set of all frontier places
            all_frontier_places.update(frontier_places)
            # Update counter of places => compute frequencies
            matrix[query] += Counter(frontier_places)

        # Set the mac_number for future standardization
        matrix[query]["mac_number"] = mac_number

    LOGGER.info("Files processed: %s", file_number)
    assert file_number != 0, "No *mac.txt files found!"

    # Save the matrix
    # columns: "patterns (number)/places (number);mac_number;frontier places"
    with open(output_dir + matrix_filename, 'w') as f_d:

        # Forge header
        header = "patterns ({})/places ({})".format(
            len(matrix),
            len(all_frontier_places),
        )
        writer = csv.DictWriter(
            f_d,
            delimiter=str(';'),
            restval=0, # default value for frequency
            fieldnames=[header, "mac_number"] + list(all_frontier_places))
        writer.writeheader()

        # Add a last line in the csv: total of occurrences for each place
        global_frontier_counter = Counter()
        # The first column is composed of the query + the number of solutions for it
        for query, row in matrix.iteritems():
            global_frontier_counter += row
            # PS: THIS modifies the matrix by adding a new key ('header')
            row[header] = "{} ({})".format(query, row["mac_number"])
            writer.writerow(row)

        # Total of occurrences at the end of the file
        global_frontier_counter[header] = "Total of occurrences"
        writer.writerow(global_frontier_counter)

    return matrix


def transpose_csv(input_file='occurrence_matrix.csv',
                  output_file='occurrence_matrix_t.csv'):
    """Useful function to transpose a csv file x,y => y,x

    .. note:: The csv file must be semicolon ';' separated.

    :param input_file: Input file.
    :param output_file: Output file transposed.
    :type input_file: <str>
    :type output_file: <str>
    """

    # Transpose file
    # PS: izip('ABCD', 'xy') --> Ax By
    data = it.izip(*csv.reader(open(input_file, "r"), delimiter=str(';')))
    csv.writer(open(output_file, "w"), delimiter=str(';')).writerows(data)
