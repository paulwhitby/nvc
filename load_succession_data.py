"""load computed succession data from the nvc database into a graph"""

# pylint: disable=line-too-long

import sqlite3


LOAD_SUCCESSION_QUERY = """
SELECT
    succession.succession_key, 
    succession.from_community_key, 
    succession.to_community_key, 
    succession.probability 
FROM succession
"""

LOAD_SUCCESSION_QUERY_ORDER_BY_FROM = """
SELECT
    succession.succession_key, 
    succession.from_community_key, 
    succession.to_community_key, 
    succession.probability 
FROM succession
ORDER BY succession.from_community_key
"""

LOAD_SUCCESSION_QUERY_ORDER_BY_TO = """
SELECT
    succession.succession_key, 
    succession.from_community_key, 
    succession.to_community_key, 
    succession.probability 
FROM succession
ORDER BY succession.to_community_key
"""

# column names to zip up with returned database columns to make them into dictionaries
SUCCESSION_COLUMN_NAMES = ('succession_key', 'from_community_key', 'to_community_key', 'probability')

GRAPH_NODES = {}

DATABASE_NAME = "nvc.db"

# table created with
# "CREATE TABLE succession(succession_key, from_community_key, to_community_key, probability)"



def _load_succession_into_list(database_name, query_string, column_names, verbose) -> list:
    """private function to load succession database table into a list()"""
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    load_succession_list = []

    for row in cur.execute(query_string):
        d = dict(zip(column_names, list(row)))
        if verbose:
            print(row, d)
        load_succession_list.append(d)

    con.close()
    return load_succession_list


def _load_succession_into_reverse_dict(database_name=DATABASE_NAME, query_string=LOAD_SUCCESSION_QUERY_ORDER_BY_TO, column_names=SUCCESSION_COLUMN_NAMES, verbose=False) -> dict:
    """private function to load REVERSE succession database table into a graph()"""
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    load_succession_model = {}
    current_community = ""
    previous_community = ""
    current_from_list = []

    for row in cur.execute(query_string):
        d = dict(zip(column_names, list(row)))
        current_community = d['to_community_key']

        if verbose:
            print("C", current_community, "P", previous_community, "L", current_from_list)
            print("R", d)

        if current_community != previous_community:
            if previous_community != "":
                load_succession_model[previous_community] = current_from_list
            current_from_list = []
            previous_community = current_community

        current_from_list.append(d['from_community_key'])

    con.close()

    if verbose:
        print("\nmodel\n", load_succession_model)

    return load_succession_model


def _load_succession_into_forward_dict(database_name=DATABASE_NAME, query_string=LOAD_SUCCESSION_QUERY_ORDER_BY_FROM, column_names=SUCCESSION_COLUMN_NAMES, verbose=False) -> dict:
    """private function to load FORWARD succession database table into a graph()"""
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    load_succession_model = {}
    current_community = ""
    previous_community = ""
    current_from_list = []

    for row in cur.execute(query_string):
        d = dict(zip(column_names, list(row)))
        current_community = d['from_community_key']

        if verbose:
            print("C", current_community, "P", previous_community, "L", current_from_list)
            print("R", d)

        if current_community != previous_community:
            if previous_community != "":
                load_succession_model[previous_community] = current_from_list
            current_from_list = []
            previous_community = current_community

        current_from_list.append(d['to_community_key'])

    con.close()

    if verbose:
        print("\nmodel\n", load_succession_model)

    return load_succession_model


def _make_graph_nodes(forward_dict, reverse_dict, verbose=False) -> dict:
    """private function to build graph nodes from the forward and reverse succession dictionaries"""
    graph = {}

    # process forward list and find all those in forward list with reverse entries
    for community_key, fwd_list in forward_dict.items():
        if community_key in reverse_dict:
            rev_list = reverse_dict[community_key]
        else:
            if verbose:
                print(community_key, "not in reverse list")
            rev_list = []
        new_node = {"fwd": fwd_list, "rev": rev_list}
        graph[community_key] = new_node
        if verbose:
            print(community_key, graph[community_key])

    #  process reverse list to catch any entries with no forward entry
    for community_key, rev_list in reverse_dict.items():
        if community_key in forward_dict:
            fwd_list = forward_dict[community_key]
        else:
            if verbose:
                print(community_key, "not in forward list")
            fwd_list = []
        new_node = {"fwd": fwd_list, "rev": rev_list}
        graph[community_key] = new_node
        if verbose:
            print(community_key, graph[community_key])

    return graph


def load_succession_into_list(verbose=False):
    """public function to load succession database table into a list()"""
    return _load_succession_into_list(DATABASE_NAME, LOAD_SUCCESSION_QUERY_ORDER_BY_FROM, SUCCESSION_COLUMN_NAMES, verbose)


def load_succession_into_reverse_dict(verbose=False):
    """public function to load inverse succession database table into a list"""
    return _load_succession_into_reverse_dict(DATABASE_NAME, LOAD_SUCCESSION_QUERY_ORDER_BY_TO, SUCCESSION_COLUMN_NAMES, verbose)


def load_succession_into_forward_dict(verbose=False):
    """public function to load forward succession database table into a list"""
    return _load_succession_into_forward_dict(DATABASE_NAME, LOAD_SUCCESSION_QUERY_ORDER_BY_FROM, SUCCESSION_COLUMN_NAMES, verbose)


def make_graph_nodes(forward_dict, reverse_dict, verbose=False) -> dict:
    """public function to create graph nodes from forward and reverse succession lists"""
    return _make_graph_nodes(forward_dict, reverse_dict, verbose)


DEBUG_FLAG_1 = False
DEBUG_FLAG_2 = True

reverse_sl = load_succession_into_reverse_dict(False)
if DEBUG_FLAG_1:
    print("\nReverse Succession Dictionary\n")
    for k, v in reverse_sl.items():
        print(k, "succeeds FROM", v)

forward_sl = load_succession_into_forward_dict(False)
if DEBUG_FLAG_1:
    print("\nForward Succession Dictionary\n")
    for k, v in forward_sl.items():
        print(k, "succeeds TO", v)

GRAPH_NODES = make_graph_nodes(forward_sl, reverse_sl, False)
if DEBUG_FLAG_2:
    print("\nGraph nodes\n")
    for k, v in GRAPH_NODES.items():
        print(k, "-->", v['fwd'], "& <--", v['rev'])
