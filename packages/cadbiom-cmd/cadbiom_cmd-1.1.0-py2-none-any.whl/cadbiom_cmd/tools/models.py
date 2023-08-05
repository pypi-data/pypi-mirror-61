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
This module groups functions directly related to the management and the
extraction of data of a Cadbiom model.

Here we find high-level functions to manage the logical formulas of the events
and conditions defining the transitions; as well as useful functions to manage
the entities, like to obtain their metadata or the frontier places of the model.
"""
from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
from collections import defaultdict
import re
import json
import itertools as it
from logging import DEBUG

# Library imports
from cadbiom.models.guard_transitions.translators.chart_xml import MakeModelFromXmlFile
from cadbiom.models.biosignal.translators.gt_visitors import compile_event, compile_cond
from cadbiom.models.biosignal.sig_expr import *
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor

import cadbiom.commons as cm

LOGGER = cm.logger()


class Reporter(object):
    """Error reporter.

    .. note:: Link the lexer to the model allows to avoid error in Reporter
        like:  "-> dec -> Undeclared event or state"
        In practice this is time consuming and useless for what we want to do.
        See parse_condition()
    """

    def __init__(self):
        self.error = False
        self.mess = ""

    def display(self, err):
        """Display the error in the logger"""
        self.error = True
        if "Undeclared event or state" not in err:
            LOGGER.error("\t" + self.mess + " -> " + err)


def get_transitions_from_model_file(model_file):
    """Get all transitions and parser from a model file (bcx format).

    :param: bcx file.
    :type: <str>
    :return: Transitions (see get_transitions()) and the Parser for the model.
    :rtype: <dict>, <MakeModelFromXmlFile>
    """

    parser = MakeModelFromXmlFile(model_file)
    return get_transitions(parser), parser


def get_transitions(parser):
    """Get all transitions in the given parser.

    There are two methods to access the transitions of a model.

    :Example:

        .. code-block:: python

            >>> print(dir(parser))
            ['handler', 'model', 'parser']
            >>> # Direct access
            >>> events = list()
            >>> for transition in parser.model.transition_list:
            ...     events.append(transition.event)
            >>>
            >>> # Indirect access via a handler
            >>> events = list()
            >>> for transitions in parser.handler.top_pile.transitions:
            ...     # transitions is a list of CTransition objects
            ...     for transition in transitions:
            ...         events.append(transition.event)

    :param: Parser opened on a bcx file.
    :type: <MakeModelFromXmlFile>
    :return: A dictionnary of events as keys, and transitions as values.
        Since many transitions can define an event, values are lists.
        Each transition is a tuple with: origin node, final node, attributes
        like label and condition.
        ``{'h00': [('Ax', 'n1', {'label': 'h00[]'}),]``
    :rtype: <dict <list <tuple <str>, <str>, <dict <str>: <str>>>>
    """

    # NOTE: je devrais parler d'events au lieu de transitions...
    # voir si on peut retourner le parser pour faire tourner le static analysis ?
    # ou faire 1 fonction séparée qui parle plus du modèle lui meme que du graphe...
    # (ce que fait get_statistics d'ailleurs...)
    transitions = defaultdict(list)

    for trans in parser.model.transition_list:

        # Get the names of clocks
        # Some event have many clocks (like _h_2755) for the same
        # ori/ext entities, so we have to extract them and their respective
        # conditions
        if trans.event == "":
            # null event without clock => StartNodes
            # These nodes are used to resolve the problem of
            # Strongly Connected Components (inactivated cycles in the graph)
            # The nodes
            # Avoids having SigConstExpr as event type in parse_event()
            # I create a transition (SCC-__start__?),
            # and a node (__start__?) for this case.
            trans.event = "SCC-" + trans.ori.name
            events = {trans.event: trans.condition}
        elif re.match("_h[\w]+", trans.event):
            # 1 event (with 1 clock)
            events = {trans.event: trans.condition}
        else:
            # Many events (with many clocks with condition(s))
            events = parse_event(trans.event)

        for event, condition in events.iteritems():
            # LOGGER.debug("NEW trans", event)

            # Handle multiple transitions for 1 event
            transitions[event].append(
                (
                    trans.ori.name, trans.ext.name,
                    {
                        "label": event,  # + '[' + trans.condition + ']',
                        "condition": condition,
                    },
                )
            )

    LOGGER.info("%s transitions loaded", len(transitions))
    # Return a dict instead of defaultdict to avoid later confusions
    # (masked errors) by searching a transition that was not in the model...

    assert transitions, (
        "No transitions found in the model ! "
        "Please check the names of events (_h_xxx)"
    )

    # Forge return value
    return dict(transitions)


def get_frontier_places(transitions, all_places):
    """Return frontier places of a model (deducted from its transitions and
    from all places of the model).

    .. note:: why we use all_places from the model instead of
        (input_places - output_places) to get frontier places ?
        Because some nodes are only in conditions and not in transitions.
        If we don't do that, these nodes are missing when we compute
        valid paths from conditions.

    :param arg1: Model's transitions.
        {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    :type arg1: <dict>
        keys: names of events
        values: list of transitions as tuples (with in/output, and label).
    :return: Set of frontier places.
    :rtype: <set>
    """

    # Get transitions in events
    g = tuple(trans for event in transitions.values() for trans in event)

    # Get input nodes & output nodes
#    input_places = {trans[0] for trans in g}
    output_places = {trans[1] for trans in g}

    # Get all places that are not in transitions in the "output" place
    return set(all_places) - output_places


################################################################################

def get_places_from_condition(condition):
    """Parse condition string and return all places, regardless of operators.

    .. note:: This function is only used to get all nodes in a condition when
        we know they are all inhibitors nodes.

    .. todo:: See the workaround in the code, without using very time consuming
        and badly coded functions.

    :param: Condition string.
    :type: <str>
    :return: Set of places.
    :rtype: <set>
    """

    # Valid but very time consuming like any other things in Cadbiom library
#    err = Reporter()
#    tvi = TableVisitor(err)
#    symb_tab = tvi.tab_symb
#    cond_sexpr = compile_cond(condition, symb_tab, err)
#    inhibitors_nodes = set()
#    possible_paths = rec(cond_sexpr, inhibitors_nodes)
#    return set(it.chain(*possible_paths))

    # Replace parentheses first to make spaces in the string
    # As operators are followed or preceded by parentheses, we can detect them
    # without false positives (operator string inside an entity name)
    replacement = ["(", ")", " and ", " or ", " not "]

    for operator in replacement:
        condition = condition.replace(operator, " ")

    # Must be exempt of unauthorized chars
    return {elem for elem in condition.split(" ") if elem != ""}


def parse_event(event):
    """Decompile logical formula in event's name.

    :param: Event string.
    :type: <event string>
    :return: A dict of events and their conditions.
    :rtype: <dict>
        keys: event's names; values: logical formula attached (condition)
    """

    def treeToExprDefaultsList(tree):
        if isinstance(tree, SigDefaultExpr):
            return treeToExprDefaultsList(tree.left_h) + \
                treeToExprDefaultsList(tree.right_h)

        # Here, some tree are from classes SigConstExpr or SigIdentExpr
        # Ex: for the clock "_h_5231":
        #    ... default (_h_5231)" => No condition for this event
        # Other examples:
        # _h_2018 _h_820 _h_4939 _h_5231 _h_3301 _h_4967 _h_2303 _h_3301
        return [tree]

    def filterSigExpression(expr):
        """
        .. note:: No SigConstExpr here => filtered in get_transitions()
            by checking null events (event="") in the model.
        """

        if isinstance(expr, SigWhenExpr):
            # right : SigSyncBinExpr (logical formula), BUT
            # sometimes SigConstExpr (just a True boolean) when clock is empty
            # Ex: "when ()"
            # So, we replace this boolean with an empty condition
            right = "" if isinstance(expr.right_h, SigConstExpr) else str(expr.right_h)

            return expr.left_h.name, right

        if isinstance(expr, SigIdentExpr):
            return expr.name, ""

        raise AssertionError(
            "You should never have been there ! "
            "Your expression type is not yet supported..."
        )

#    def filterSigExpression(listOfExpr):
#        return [filterSigExpression(expr) for expr in listOfExpr]

    # Error Reporter
    err = Reporter()
    tvi = TableVisitor(err)
    symb_tab = tvi.tab_symb

    # Get tree object from event string
    event_sexpr = compile_event(event, symb_tab, True, err)[0]

    # Filter when events
    g = (filterSigExpression(expr) for expr in treeToExprDefaultsList(event_sexpr))
    eventToCondStr = {event_name: event_cond for event_name, event_cond in g}

    LOGGER.debug("Clocks from event parsing: %s", eventToCondStr)

    return eventToCondStr


def parse_condition(condition, all_nodes, inhibitors_nodes):
    """Return valid paths according the given logical formula and nodes;
    and set inhibitors_nodes

    .. note:: inhibitors_nodes is modified(set) by this function.

    :param condition: Condition string of a transition.
    :param all_nodes: Nodes involved in transitions + frontier places.
    :param inhibitors_nodes: Inactivated nodes in paths of conditions.
    :type condition: <str>
    :type inhibitors_nodes: <set>
    :type all_nodes: <set>
    :return: Set of paths. Each path is a tuple of nodes.
    :rtype: <set>
    """

    LOGGER.debug("CONDITION: %s", condition)
    # Error Reporter
    err = Reporter()
    tvi = TableVisitor(err)
    # Link the lexer to the model allows to avoid error in Reporter
    # like:  "-> dec -> Undeclared event or state"
    # In practice this is time consuming and useless for what we want to do
    # parser = MakeModelFromXmlFile(BIO_MOLDELS_DIR +
    # "Whole NCI-PID database translated into CADBIOM formalism(and).bcx")
    # parser.model.accept(tvi)
    symb_tab = tvi.tab_symb
    # Get tree object from condition string
    cond_sexpr = compile_cond(condition, symb_tab, err)
    # Get all possible paths from the condition
    possible_paths = rec(cond_sexpr, inhibitors_nodes)

    # Prune possible paths according to:
    # - Inhibitor nodes that must be removed because they will never
    # be in the graph.
    # - All nodes in transitions (ori -> ext) because we know all transitions
    # in the graph, so we know which entities can be choosen to validate a path.
    # - All frontier places, that are known entities that can be in conditions
    # (not only in ori/ext) of transitions.
    # So: authorized nodes = frontier_places + transition_nodes - inhibitor nodes
    valid_paths = {
        tuple(path)
        for path in possible_paths
        if (set(path) - inhibitors_nodes).issubset(all_nodes)
    }

    # Debugging only
    if LOGGER.getEffectiveLevel() == DEBUG:
        LOGGER.debug("INHIBIT NODES: %s", inhibitors_nodes)
        LOGGER.debug("ALL NODES: %s", all_nodes)
        LOGGER.debug("POSSIBLE PATHS: %s", possible_paths)
        LOGGER.debug("VALID PATHS: %s", valid_paths)

        if len(valid_paths) > 1:
            LOGGER.debug(
                "Multiple valid paths in the model for: %s:\n%s", condition, valid_paths
            )

        for path in possible_paths:
            pruned_places = set(path) - inhibitors_nodes
            isinsubset = pruned_places.issubset(all_nodes)
            LOGGER.debug("PRUNED PATH: %s, VALID: %s", pruned_places, isinsubset)

    assert valid_paths, "No valid path in the model for: " + str(condition)

    return valid_paths


    from cadbiom.models.guard_transitions.analyser.ana_visitors import SigExpIdCollectVisitor

    # condition expressions contains only node ident
    icv = SigExpIdCollectVisitor()
    lst1 = cond_sexpr.accept(icv)
    print(cond_sexpr)
    print(type(cond_sexpr))
    print(dir(cond_sexpr))
    print("LISTE", lst1)
#    <class 'cadbiom.models.biosignal.sig_expr.SigSyncBinExpr'>
#    'accept', 'get_signals', 'get_ultimate_signals', 'is_bot', 'is_clock',
# 'is_const', 'is_const_false', 'is_ident', 'left_h', 'operator', 'right_h', 'test_equal']

    print(cond_sexpr.get_signals())
#    print(cond_sexpr.get_ultimate_signals())
    print("LEFT", cond_sexpr.left_h)
    print("OPERATOR", cond_sexpr.operator)
    print("RIGHT", cond_sexpr.right_h)


#    ret = treeToTab(cond_sexpr)
#    [set([('((formule', True)])]
#    print("treeToTab", ret)
#    print(type(ret))
#    print(dir(ret))


def rec(tree, inhibitors_nodes):
    """Recursive function to decompile conditions

    :param tree:
        :Example of tree argument:

            .. code-block:: python

                tree = ('H', 'v', (
                    ('F', 'v', 'G'),
                    '^',
                    (
                        ('A', 'v', 'B'),
                        '^',
                        ('C', 'v', ('D', '^', 'E'))
                    )
                ))
    """

#    print("TREE", tree, type(tree), dir(tree))

    if isinstance(tree, str):  # terminal node
        path = [tree]
        solutions = [path]
        return solutions
    if isinstance(tree, SigNotExpr):
        # tree.operand: the entity, type: SigIdentExpr
        LOGGER.debug("NOT OPERAND: %s, %s", tree.operand, type(tree.operand))
        try:
            current_inhibitors = get_places_from_condition(tree.operand.__str__())
            inhibitors_nodes.update(current_inhibitors)
            LOGGER.debug("INHIBITORS found: %s", current_inhibitors)

            path = [tree.operand.name]
            solutions = [path]
            return solutions
        except AttributeError:
            tree = tree.operand

    if isinstance(tree, SigIdentExpr):
        path = [tree.name]
        solutions = [path]
        return solutions



    lch = tree.left_h
    op = tree.operator
    rch = tree.right_h
#    print('OZCJSH:', lch, op, rch, sep='\t\t')
    lpaths = rec(lch, inhibitors_nodes)
    rpaths = rec(rch, inhibitors_nodes)
#    print('VFUENK:', lpaths, rpaths)
    if op == 'or':  # or
#        ret = [*lpaths, *rpaths]
        ret = list(it.chain(lpaths, rpaths))
#        print('RET:', ret)
        return ret
    else:  # and
        assert op == 'and'
#        print(list(it.product(lpaths, rpaths)))
#        raw_input('test')

        ret = list(l + r for l, r in it.product(lpaths, rpaths))
#        print('RET:', ret)
        return ret


################################################################################

def get_places_data(places, model):
    """Get a list of JSON data parsed from each given places in the model.

    .. note:: This function is used by low_model_infos().

    .. note:: v1 models return a dict with only 1 key: 'cadbiomName'

    .. note:: Start nodes (with a name like __start__x) are handled even
        with no JSON data.
        They are counted in the other_types and other_locations fields.

    :Example of JSON data that can be found in the model:

        .. code-block:: python

            {
                "uri": entity.uri,
                "entityType": entity.entityType,
                "names": list(entity.synonyms | set([entity.name])),
                "entityRef": entity.entityRef,
                "location": entity.location.name if entity.location else None,
                "modificationFeatures": dict(entity.modificationFeatures),
                "members": list(entity.members),
                "reactions": [reaction.uri for reaction in entity.reactions],
                "xrefs": entity.xrefs,
            }

    :param arg1: Iterable of name of places.
    :param arg2: Model from handler.
    :type arg1: <set>
    :type arg2: <MakeModelFromXmlFile>
    :return: List of data parsed from each give places.

        .. note:: Here is the list of field retrieved for v2 models:

            - cadbiomName
            - uri
            - entityType
            - entityRef
            - location
            - names
            - xrefs
    :rtype: <list <dict>>
    """

    if model.xml_namespace == "http://cadbiom.genouest.org/v2/":
        # Fixed fields and default types
        json_note_fieldnames = {
            "uri": "",
            "entityType": "",
            "entityRef": "",
            "location": "",
            "names": list(),  # Default type is 'list' for names (not '')
            "xrefs": dict(),
        }
        # Init final dictionary
        data = list()
        for place_name in places:

            try:
                # Model type 2 => We use JSON data in each nodes
                # Get JSON data ('' if the field is not present)
                json_data = json.loads(model.node_dict[place_name].note)
            except ValueError as exc:
                # Handle start nodes (name: __start__x)
                if exc.message == "No JSON object could be decoded":
                    json_data = dict()

            temp = {
                fieldname: json_data.get(fieldname, default_data)
                for fieldname, default_data in json_note_fieldnames.items()
            }

            # Patch: Handle null values that should be avoided in cadbiom_writer.build_json_data()
            temp["names"] = [name for name in temp["names"] if name]
            # Add the cadbiom name (name attribute of xml element
            temp["cadbiomName"] = place_name
            data.append(temp)

        return data

    # v1 model: return only the name of the place
    return [{"cadbiomName": place_name} for place_name in places]


def get_model_identifier_mapping(model_file, external_identifiers):
    """Get Cadbiom names corresponding to the given external identifiers (xrefs)

    .. note:: This function works only on v2 formated models with JSON additional data

    :param model_file: Model file.
    :param external_identifiers: Set of external identifiers to be mapped.
    :type model_file: <str>
    :type external_identifiers: <set>
    :return: Mapping dictionary with external identifiers as keys
        and cadbiom names as values.
    :rtype: <dict <str>:<list>>
    """
    # Get the model
    parser = MakeModelFromXmlFile(model_file)
    model = parser.handler.model

    assert model.xml_namespace == 'http://cadbiom.genouest.org/v2/', \
        "Operation not supported: Only v2 models are supported."

    # Get all nodes
    places_data = get_places_data(parser.handler.node_dict.iterkeys(), model)

    # {'xrefs': {'bdd': [values],}, 'cadbiomName': '',}
    g = {
        place["cadbiomName"]: frozenset(it.chain(*place["xrefs"].itervalues()))
        for place in places_data
    }

    # Mapping: external_identifiers as keys and Cadbiom names as values
    mapping = defaultdict(set)
    for place, identifiers in g.iteritems():

        common_identifiers = identifiers & external_identifiers
        if common_identifiers:
            [mapping[common_id].add(place) for common_id in common_identifiers]

    not_found_identifiers = external_identifiers - set(mapping.keys())
    if not_found_identifiers:
        LOGGER.info(
            "Some identifiers were not found (%s/%s): %s",
            len(not_found_identifiers),
            len(external_identifiers),
            not_found_identifiers,
        )

    return mapping
