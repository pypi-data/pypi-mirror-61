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
"""Entry point and argument parser for cadbiom_cmd package"""
from __future__ import print_function

# Standard imports
import argparse
import os
import sys
from functools import wraps

# Custom imports
import cadbiom.commons as cm

LOGGER = cm.logger()
parser = None


def check_output_dir(function):
    """Decorator used process some arguments from argparse"""
    # Expose the docstring of the wrapped function instead of that of the decorator
    @wraps(function)
    def modified_func(*args, **kwargs):
        """Fix paths in arguments (add trailing '/')"""
        output_dir = args[0]['output']
        output_dir = output_dir if output_dir[-1] == '/' else output_dir + '/'

        # Compatibility for output and output_dir
        args[0]['output'] = output_dir
        args[0]['output_dir'] = output_dir

        return function(*args, **kwargs)

    return modified_func


@check_output_dir
def solutions_search(args):
    """Launch the search for Minimum Activation Conditions (MAC) for entities
    of interest.
    """

    # Module import
    import solution_search
    # Temporary fix: all_macs is always activated in the new API
    args["all_macs"] = True
    solution_search.solutions_search(args) # !


def solutions_sort(args):
    """Read a solution file or a directory containing MAC solutions files
    (*mac* files), and sort all frontier places/boundaries in alphabetical order.
    """

    # Module import
    import solution_sort
    solution_sort.solutions_sort(args['path'])


@check_output_dir
def solutions_2_graphs(args):
    """Create GraphML formated files containing a representation of the
    trajectories for each solution in complete MAC files (*mac_complete files).

    This is a function to visualize paths taken by the solver from the boundaries
    to the entities of interest.
    """

    # Module import
    import solution_sort
    solution_sort.solutions_2_graphs(
        args['output'],
        args['model_file'],
        args['path']
    )


@check_output_dir
def queries_2_json(args):
    """Create a JSON formated file containing all data from complete MAC files
    (*mac_complete files). The file will contain frontier places/boundaries
    and decompiled steps with their respective events for each solution.

    This is a function to quickly search all transition attributes involved
    in a solution.
    """

    # Module import
    import solution_sort
    solution_sort.queries_2_json(
        args['output'],
        args['model_file'],
        args['path'],
        conditions=not args['no_conditions'], # Reverse the param...
    )


@check_output_dir
def json_2_interaction_graph(args):
    """Make an interaction weighted graph based on the searched molecule of interest.

    Read decompiled solutions files (*.json* files produced by the
    directive 'queries_2_json') and make a graph of the relationships
    between one or more molecules of interest, the genes and other
    frontier places/boundaries found among all the solutions.
    """

    # Module import
    import interaction_graph
    interaction_graph.json_2_interaction_graph(
        args['output'],
        args['molecules_of_interest'],
        args['path'],
    )


@check_output_dir
def queries_2_common_graph(args):
    """Create a GraphML formated file containing a unique representation of **all**
    trajectories corresponding to all solutions in each complete MAC files
    (*mac_complete files).

    This is a function to visualize paths taken by the solver from the boundaries
    to the entities of interest.
    """

    # Module import
    import solution_sort
    if not any((args["graphs"], args["csv"], args["json"])):
        parser.error("at least one flag is required")
    solution_sort.queries_2_common_graph(**args)


@check_output_dir
def queries_2_occcurrence_matrix(args):
    """Create a matrix of occurrences counting entities in the solutions found in
    *mac.txt files in the given path.
    """

    # Module import
    import solution_sort
    solution_sort.queries_2_occcurrence_matrix(
        args['output'],
        args['model_file'],
        args['path'],
        transposed=args['transpose_csv']
    )


def model_identifier_mapping(args):
    """Mapping of identifiers from external databases.

    This function exports a CSV formated file presenting the list of known
    Cadbiom identifiers for each given external identifier.
    """

    # Module import
    import models
    models.model_identifier_mapping(**args)


@check_output_dir
def model_comparison(args):
    """Isomorphism test.

    Check if the graphs based on the two given models have  the same topology,
    nodes & edges attributes/roles.
    """

    # Module import
    import models
    models.graph_isomorph_test(
        args['model_file_1'],
        args['model_file_2'],
        args['output'],
        args['graphs'],
        args['json'],
    )


@check_output_dir
def model_info(args):
    """Provide several levels of information about the structure of the model
    and its places/entities.
    """

    # Module import
    import models
    models.model_info(**args)


@check_output_dir
def model_graph(args):
    """Information about the graph based on the model.

    Get centralities (degree).
    Forge a GraphML file.
    """

    # Module import
    import models
    models.model_graph(**args)


@check_output_dir
def merge_macs(args):
    """Merge solutions to a csv file."""

    # Module import
    import solution_merge
    solution_merge.merge_macs_to_csv(args['solutions_directory'],
                                     args['output'])


def analytics(params):
    from urllib import urlopen, urlencode
    from uuid import getnode
    import re
    from sys import platform
    import json

    white_list = (
        "subcommand", "model_file", "start_prop", "final_prop", "inv_prop",
        "limit",
        "molecules_of_interest",
        "model_file_1", "model_file_2", "graphs", "json",
        "default", "boundaries", "all_entities", "genes",
        "centralities", "graph", "json",
    )

    # {"1":["key","val"],}
    cvar = {str(i): [key, val] for i, (key, val) in enumerate(params.items(), 1)
            if val is not None and key in white_list}
    data = {
        "url": "http://cadbiom.genouest.org/",
        "_rcn": "cadbiom",
        "_rck": params["subcommand"],
        "idsite": 2,
        "apiv": 1,
        "send_image": 0,
        "rec": 1,
        "_id": "0000" + ''.join(re.findall('..', '%0012x' % getnode()))[:16],
        "_cvar": json.dumps(cvar).encode("utf8"),
        "ua": platform,
    }
    data = urlencode(data).encode("ascii")
    page = urlopen("http://cadbiom.genouest.org/lytic.html", data=data).read()
    m = re.search(".*URL=(.*)\">", page)
    if m:
        urlopen(m.group(1), data=data)


def args_to_param(args):
    """Return argparse namespace as a dict {variable name: value}"""
    return {k: v for k, v in vars(args).items() if k != 'func'}


def ensure_dir_presence(path):
    """Test write mode and eventually create the given directory"""

    if not os.path.dirname(path):
        # Current directory
        path = "."

    if not os.path.isfile(path) and not os.path.isdir(path):
        LOGGER.info("Creation of the directory <{}>".format(path))
        os.mkdir(path)

    if not os.access(path, os.W_OK):
        LOGGER.error("<{}> is not writable".format(path))
        exit()


class ReadableFile(argparse.Action):
    """
    http://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
    """

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_file = values

        if not os.path.isfile(prospective_file):
            LOGGER.error("readable_file:<{}> is not a valid file".format(prospective_file))
            exit()

        if os.access(prospective_file, os.R_OK):
            setattr(namespace, self.dest, prospective_file)
        else:
            LOGGER.error("readable_file:<{}> is not a readable file".format(prospective_file))
            exit()


class ReadableDir(argparse.Action):
    """
    http://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
    """

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not os.path.isdir(prospective_dir):
            LOGGER.error("readable_dir:<{}> is not a valid path".format(prospective_dir))
            exit()

        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            LOGGER.error("readable_dir:<{}> is not a readable dir".format(prospective_dir))
            exit()


def main():
    """Argument parser"""

    # parser configuration
    global parser
    parser = argparse.ArgumentParser(description=__doc__)
    # Default log level: debug
    parser.add_argument('-vv', '--verbose', nargs='?', default='info')
    # Subparsers
    subparsers = parser.add_subparsers(title='subcommands', dest="subcommand")

    # PS: nargs='?' = optional
    # subparser: Compute macs
    #    steps      = 10
    #    final_prop = "P"
    #    start_prop = None
    #    inv_prop   = None
    parser_input_file = subparsers.add_parser(
        'solutions_search',
        help=solutions_search.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_input_file.add_argument('model_file')
    # Get final_property alone OR an input_file containing multiple properties
    group = parser_input_file.add_mutually_exclusive_group(required=True)
    group.add_argument('final_prop', nargs='?',
        help="Final property that will occur at the end of the simulation.")
    group.add_argument('--input_file', action=ReadableFile, nargs='?',
        help="Without input file, there will be only one process. "
             "While there will be 1 process per line (per logical formula "
             "on each line)")
    parser_input_file.add_argument('--output', action=ReadableDir, nargs='?',
                                   default='result/', help="Output directory.")

    # default: False
    parser_input_file.add_argument('--combinations', action='store_true',
        help="If input_file is set, we can compute all combinations of "
             "given elements on each line")
    parser_input_file.add_argument('--steps', type=int, nargs='?', default=7,
        help="Maximum of allowed steps to find macs")
    parser_input_file.add_argument('--limit', type=int, nargs='?', default=400,
        help="Limit the number of solutions.")
    # https://docs.python.org/dev/library/argparse.html#action
    # all_macs to False by default
    #parser_input_file.add_argument('--all_macs', action='store_true',
    #    help="Solver will try to search all macs from 0 to the maximum of "
    #         "allowed steps.")
    # continue to False by default
    parser_input_file.add_argument('--continue', action='store_true',
        help="Resume previous computations; if there is a mac file from a "
             "previous work, last frontier places/boundaries will be reloaded.")
    parser_input_file.add_argument('--start_prop', nargs='?', default=None,
        help="Property that will be part of the initial state of the model. "
             "In concrete terms, some entities can be activated by this "
             "mechanism without modifying the model.")
    parser_input_file.add_argument('--inv_prop', nargs='?', default=None,
        help="Invariant property that will always occur during the simulation. "
             "The given logical formula will be checked at each step of the simulation.")

    parser_input_file.set_defaults(func=solutions_search)

    ## Solutions-related commands ##############################################

    # subparser: Sort solutions in alphabetical order in place
    # Solution file (complete or not)
    parser_solutions_sort = subparsers.add_parser('solutions_sort',
                                                  help=solutions_sort.__doc__)
    parser_solutions_sort.add_argument('path',
        help="Solution file or directory with MAC solutions files "
             "(*mac* files) generated with the 'solutions_search' command.")
    parser_solutions_sort.set_defaults(func=solutions_sort)


    # subparser: Representation of the trajectories of MACs in a complete file.
    # Model file (xml : cadbiom language)
    # Solution file (mac_complete)
    parser_trajectories = subparsers.add_parser(
        'solutions_2_graphs',
        help=solutions_2_graphs.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_trajectories.add_argument('model_file',
        help="bcx model file.")
    parser_trajectories.add_argument('path',
        help="Complete solution file or directory with MAC solutions files "
             "(*mac_complete.txt files) generated with the 'compute_macs' command.")
    parser_trajectories.add_argument('--output', action=ReadableDir,
        nargs='?', default='graphs/',
        help="Output directory for GraphML files.")
    parser_trajectories.set_defaults(func=solutions_2_graphs)


    # subparser: Decompilation of trajectories of MACs in a complete file/dir.
    # Model file (xml : cadbiom language)
    # Solution file (mac_complete)
    parser_queries_2_json = subparsers.add_parser(
        'queries_2_json',
        help=queries_2_json.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_queries_2_json.add_argument('model_file',
        help="bcx model file.")
    parser_queries_2_json.add_argument('path',
        help="Complete solution file or directory with MAC solutions files "
             "(*mac_complete.txt files) generated with the 'compute_macs' command.")
    parser_queries_2_json.add_argument('--output', action=ReadableDir,
        nargs='?', default='decompiled_solutions/',
        help="Directory for newly created files.")
    parser_queries_2_json.add_argument('--no_conditions', action='store_true',
        help="Don't export conditions of transitions. This allows "
             "to have only places/entities that are used inside trajectories; "
             "thus, inhibitors nodes are not present in the json file")
    parser_queries_2_json.set_defaults(func=queries_2_json)


    # subparser: Make an interaction weighted graph based on the searched
    # molecule of interest
    # Require JSON decompilated solutions files
    parser_json_2_interaction_graph = subparsers.add_parser(
        'json_2_interaction_graph',
        help=json_2_interaction_graph.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_json_2_interaction_graph.add_argument('molecules_of_interest', nargs='+',
        help="One or multiple molecule of interest to search in the trajectories"
             " of every solutions")
    parser_json_2_interaction_graph.add_argument('--path',
        nargs='?', default='decompiled_solutions/',
        help="JSON formated file containing all data from complete MAC files"
             "(*mac_complete files) generated with the 'queries_2_json' command.")
    parser_json_2_interaction_graph.add_argument('--output', action=ReadableDir,
        nargs='?', default='graphs/',
        help="Directory for the newly created file.")
    parser_json_2_interaction_graph.set_defaults(func=json_2_interaction_graph)


    # subparser: Common representation of the trajectories of MACs in a complete file.
    # Model file (xml : cadbiom language)
    # Solution file (mac_complete)
    parser_trajectories = subparsers.add_parser(
        'queries_2_common_graph',
        help=queries_2_common_graph.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_trajectories.add_argument('model_file',
        help="bcx model file.")
    parser_trajectories.add_argument('path',
        help="Complete solution file or directory with MAC solutions files "
             "(*mac_complete.txt files) generated with the 'compute_macs' command.")
    # Outputs
    parser_trajectories.add_argument('--graphs', action='store_true',
        help="Create a GraphML file for each MAC file.")
    parser_trajectories.add_argument('--csv', action='store_true',
        help="Create a CSV file containing a summary about places/entities "
             "of the solutions.")
    parser_trajectories.add_argument('--json', action='store_true',
        help="Create a JSON formated file containing a summary about "
             "places/entities of the solutions.")
    parser_trajectories.add_argument('--output', action=ReadableDir,
        nargs='?', default='graphs/',
        help="Output directory for GraphML files.")
    parser_trajectories.set_defaults(func=queries_2_common_graph)


    # subparser: Create a matrix of occurrences counting entities in the solutions.
    # Model file (xml : cadbiom language)
    # Solution file (mac.txt)
    parser_occurrences_matrix = subparsers.add_parser(
        'queries_2_occcurrence_matrix',
        help=queries_2_occcurrence_matrix.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_occurrences_matrix.add_argument('model_file',
        help="bcx model file.")
    parser_occurrences_matrix.add_argument('path',
        help="Directory with MAC solutions files "
             "(*mac.txt files) generated with the 'compute_macs' command.")
    parser_occurrences_matrix.add_argument('--output', action=ReadableDir,
        nargs='?', default='./',
        help="Output directory for CSV files.")
    parser_occurrences_matrix.add_argument('--transpose_csv', action='store_true',
        help="Transpose the final matrix (switch columns and rows).")
    parser_occurrences_matrix.set_defaults(func=queries_2_occcurrence_matrix)


    # subparser: Merge solutions to a csv file
    # Solution file (mac)
    # Output (csv)
    parser_merge_macs = subparsers.add_parser(
        'merge_macs',
        help=merge_macs.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_merge_macs.add_argument('solutions_directory', nargs='?',
        default='result/')
    parser_merge_macs.add_argument('--output', nargs='?',
        default='result/',
        help="Directory for the CSV file merged_macs.csv; "
             "Structure: <Final property formula>;<mac>")
    parser_merge_macs.set_defaults(func=merge_macs)

    ## Model-related commands ##################################################

    # subparser: Mapping of identifiers
    # output: CSV file
    parser_model_identifier_mapping = subparsers.add_parser(
        'model_identifier_mapping',
        help=model_identifier_mapping.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_model_identifier_mapping.add_argument('model_file',
        help="bcx model file.")
    group = parser_model_identifier_mapping.add_mutually_exclusive_group(required=True)
    group.add_argument('--external_file',
        help="File with 1 external identifiers to be mapped per line."
    )
    group.add_argument('--external_identifiers', nargs='+',
        help="Multiple external identifiers to be mapped."
    )
    parser_model_identifier_mapping.set_defaults(func=model_identifier_mapping)


    # subparser: Model comparison
    # 2 models
    parser_model_comparison = subparsers.add_parser(
        'model_comparison',
        help=model_comparison.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_model_comparison.add_argument('model_file_1',
        help="bcx model file.")
    parser_model_comparison.add_argument('model_file_2',
        help="bcx model file.")
    # Export graphs for the 2 models; default: false
    parser_model_comparison.add_argument('--graphs', action='store_true',
        help="Create two GraphML files from the given models.")
    parser_model_comparison.add_argument('--json', action='store_true',
        help="Create a summary dumped into a json file.")
    parser_model_comparison.add_argument('--output', action=ReadableDir,
        nargs='?', default='graphs/',
        help="Directory for created graphs files.")
    parser_model_comparison.set_defaults(func=model_comparison)


    # subparser: Model info
    # 1 model
    parser_model_info = subparsers.add_parser(
        'model_info',
        help=model_info.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_model_info.add_argument('model_file')
    # Filters
    group = parser_model_info.add_mutually_exclusive_group(required=True)
    # PS: Argparse doesn't allow to select a default value here
    group.add_argument('--default', action='store_true',
        help="Display quick description of the model "
             "(Number of places/entities, transitions, entity types, locations)")
    group.add_argument('--all_entities', action='store_true',
        help="Retrieve data for all places/entities of the model.")
    group.add_argument('--boundaries', action='store_true',
        help="Retrieve data only for the frontier places/boundaries of the model.")
    group.add_argument('--genes', action='store_true',
        help="Retrieve data only for the genes in the model.")
    group.add_argument('--smallmolecules', action='store_true',
        help="Retrieve data only for the smallmolecules in the model.")
    # Outputs
    parser_model_info.add_argument('--csv', action='store_true',
        help="Create a CSV file containing data about previously filtered "
             "places/entities of the model.")
    parser_model_info.add_argument('--json', action='store_true',
        help="Create a JSON formated file containing data about previously "
             "filtered places/entities of the model, and a full summary about the "
             "model itself (boundaries, transitions, events, entities locations,"
             " entities types).")
    parser_model_info.add_argument('--output', action=ReadableDir,
        nargs='?', default='./',
        help="Directory for newly created files.")
    parser_model_info.set_defaults(func=model_info)


    # subparser: Model graph
    parser_model_graph = subparsers.add_parser(
        'model_graph',
        help=model_graph.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser_model_graph.add_argument('model_file')
    # Additional data
    parser_model_graph.add_argument('--centralities', action='store_true',
        help="Get centralities for each node of the graph "
             "(degree, in_degree, out_degree, closeness, betweenness). "
             "Works in conjunction with the ``--json`` option.")
    # Outputs
    parser_model_graph.add_argument('--graph', action='store_true',
        help="Translate the model into a GraphML formated file which can "
             "be opened in Cytoscape.")
    parser_model_graph.add_argument('--json', action='store_true',
        help="Create a JSON formated file containing a summary of the graph "
             "based on the model.")
    parser_model_graph.add_argument('--json_graph', action='store_true',
        help="Create a JSON formated file containing the graph based on the "
             "model, which can be opened by Web applications.")
    parser_model_graph.add_argument('--output', action=ReadableDir,
        nargs='?', default='graphs/',
        help="Directory for newly created files.")
    parser_model_graph.set_defaults(func=model_graph)


    # Workaround for sphinx-argparse module that require the object parser
    # before the call of parse_args()
    if 'html' in sys.argv:
        return parser

    # get program args and launch associated command
    args = parser.parse_args()

    # Set log level
    cm.log_level(vars(args)['verbose'])

    # Take argparse arguments and put them in a standard dict
    params = args_to_param(args)

    # Ultimate check of the presence of the directories
    know_directory_variables = ("output", "path", "solutions_directory")
    [ensure_dir_presence(params[var]) for var in know_directory_variables
     if params.get(var, None)]

    # Analytics
    def anal():
        try:
            analytics(params)
        except:
            pass

    from threading import Thread
    thread = Thread(target=anal)
    thread.start()

    # Launch associated command
    args.func(params)

    thread.join()
