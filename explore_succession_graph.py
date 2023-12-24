"""
explore succession graph

work backwards from field survey community results to possible starting positions
"""

# from jaal import Jaal
# import pandas as pd
import load_succession_data
# import load_community_data

MAVIS_TEXT = """
Report dated Sun Oct 08 18:26:36 2023

Plot 16: MW 8-10-23 TM2648646815 St4 R5 S16
CVS: class 30
ELL: Light 7.0; Wetness 5.8; pH 6.1; Fertility 5.1
CSR: 1 species with no data: Artemisia [spp]
CSR: C: 3.20  S: 2.77  R: 2.80
BIO: 1 species with no data: Artemisia [spp]
BIO: Eurosiberian Boreo-temperate 25%
BIO: European Temperate 12%
BIO: Eurosiberian Temperate 12%
BIO: Eurasian Temperate 12%
BIO: European Southern-temperate 12%
BIO: Eurosiberian Southern-temperate 25%

Group 4: MW Stands 2,3,4
NVC:  MG1c 39.94
NVC:  MG1b 39.92
NVC: OV23c 39.25
NVC: OV23b 38.67
NVC:   MG1 38.49
NVC:  OV23 38.46
NVC:  MG9a 36.54
NVC:  MG10 36.46
NVC: OV10d 36.43
NVC:  MG1a 35.65
"""

# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import, wildcard-import
# pylint: disable=trailing-whitespace
# pylint: disable=unused-import
# pylint: disable=pointless-string-statement
# pylint: disable=invalid-name


EXPLORE_DEBUG_FLAG = False
FD = {}
RD = {}
GRAPH = {}
PATHS = []

MAVIS_OUTPUT = {
    "MG1c": 39.94,
    "MG1b": 39.92,
    "OV23c": 39.25,
    "OV23b": 38.67,
    "MG1": 38.49,
    "OV23": 38.46,
    "MG9a": 36.54,
    "MG10": 36.46,
    "OV10d": 36.43,
    "MG1a": 35.65
}

MODIFIED_MAVIS_OUTPUT = {
    "MG1": ((39.94 + 39.92 + 38.49 + 35.65) / 4),
    "OV23": ((39.25 + 38.67 + 38.46) / 3),
    "MG9": 36.54,
    "MG10": 36.46,
    "OV10": 36.43
}


def remove_subcommunities(current_community_name, community_list, verbose=False):
    """process list of community names and remove subcommunities, leaving only main communities"""
    if verbose:
        print("remove subcommunities")
    new_community_list = []
    for i in community_list:
        if i != current_community_name:
            if i[-1] not in "abcdefghij":
                new_community_list.append(i)
    return new_community_list


def find_all_child_nodes(nodes, g, verbose=False):
    """return a concatenated list of all the child nodes of the nodes in nodes"""
    found = []
    for n in nodes:
        found += remove_subcommunities(n, g[n]["rev"], verbose)
    if verbose:
        print("\nfor", nodes, "found", found)
    return found


def dedupe_list(a_list):
    """de-dupe list entries by converting to a set and back again"""
    return (list(set(a_list)))


def remove_duplicates(child_nodes, p, verbose=False):
    """remove entries from child_nodes already in p"""
    if verbose:
        print("remove duplicates")
    new_kids = []
    for c in child_nodes:
        if c not in p:
            new_kids.append(c)
    new_kids_set = set(new_kids)
    return list(new_kids_set)


if __name__ == "__main__":
    EXPLORE_DEBUG_FLAG = True
    LOAD_DEBUG_FLAG = False
    FD = load_succession_data.load_succession_into_forward_dict(LOAD_DEBUG_FLAG)
    RD = load_succession_data.load_succession_into_reverse_dict(LOAD_DEBUG_FLAG)
    GRAPH = load_succession_data.make_graph_nodes(FD, RD, LOAD_DEBUG_FLAG)

    MAVIS_GRAPH_NODES = {}

    if EXPLORE_DEBUG_FLAG:
        print("\nExplore MAVIS output\n")
        print(len(GRAPH), "nodes in entire graph")


    nodelist = []
    for mavis_community, mavis_probability in MODIFIED_MAVIS_OUTPUT.items():
        nodelist.append(mavis_community)
    
    PATHS = nodelist
    children = find_all_child_nodes(nodelist, GRAPH, True)
    children = dedupe_list(children)
    print("\nchildren of", nodelist, "are", children)

    PATHS += children

    while len(children) > 0:
        children = find_all_child_nodes(children, GRAPH, True)
        children = remove_duplicates(children, PATHS, True)
        PATHS += children
        
    new_paths = dedupe_list(PATHS)

    print("\n\nThere are", len(new_paths), "nodes")
    print("\n\nPaths\n\n", new_paths)