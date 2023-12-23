"""
explore succession graph

work backwards from field survey community results to possible starting positions
"""

# from jaal import Jaal
# import pandas as pd
import load_succession_data
import load_community_data

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
    new_community_list = []
    for i in community_list:
        if i != current_community_name:
            if i[-1] not in "abcdefghij":
                new_community_list.append(i)
    return new_community_list


def recursive_graph_traverse(node, g, p, verbose=False):
    """find all the nodes in the reverse succession path for node in the graph g
    and call recursive_graph_traverse() for each
    stop when rev_count == 0 for a node
    return with list of nodes touched"""
    if verbose:
        print("\nrecursive graph traverse of node", node)
   
    if node not in p:
        if g[node]["rev_count"] > 0:
            rev_list = remove_subcommunities(node, g[node]["rev"])
            for rev in rev_list:
                found_in_subnode = recursive_graph_traverse(rev, g, p, verbose)
                if verbose:
                    print("For", rev, "found", found_in_subnode)
                p += found_in_subnode
            return p
        # else:
        #     return []

    return []


def find_all_child_nodes(nodes, g, verbose=False):
    """return a concatenated list of all the child nodes of the nodes in nodes"""
    found = []
    for n in nodes:
        found += remove_subcommunities(n, g[n]["rev"], verbose)
    if verbose:
        print("\nfor", nodes, "found", found)
    return found


def breadth_first_recursive_search(nodes, g, p, verbose=False):
    """shallow, breadth-first graph traversal to ensure elimination of infinite recursion 
    due to circular dependencies between NVC successions"""
    size_of_p = len(p)
    if verbose:
        print("\nbreadth first recursive search")
    for n in nodes:
        if verbose:
            print("searching", n)
        if g[n]["rev_count"] > 0:
            reduced_revs = remove_subcommunities(n, g[n]["rev"], verbose)
            p += reduced_revs
            if verbose:
                print(n, "revs", reduced_revs)
                print("accumulated path", p)
        else:
            if verbose:
                print(n, "has no reverse succession")
            else:
                pass
    return (len(p)-size_of_p)   # number of new communities in list PATHS (p)


def remove_duplicates(child_nodes, p, verbose=False):
    """remove entries from child_nodes already in p"""
    new_kids = []
    for c in child_nodes:
        if c not in p:
            new_kids.append(c)
    return new_kids


if __name__ == "__main__":
    EXPLORE_DEBUG_FLAG = True
    LOAD_DEBUG_FLAG = False
    FD = load_succession_data.load_succession_into_forward_dict(LOAD_DEBUG_FLAG)
    RD = load_succession_data.load_succession_into_reverse_dict(LOAD_DEBUG_FLAG)
    GRAPH = load_succession_data.make_graph_nodes(FD, RD, LOAD_DEBUG_FLAG)

    MAVIS_GRAPH_NODES = {}

    if EXPLORE_DEBUG_FLAG:
        print("\nMAVIS output\n")


    nodelist = []
    for mavis_community, mavis_probability in MODIFIED_MAVIS_OUTPUT.items():
        nodelist.append(mavis_community)
        # P = recursive_graph_traverse(mavis_community, GRAPH, PATHS, True)
        # PATHS.append(P)
        # if EXPLORE_DEBUG_FLAG:
        #     print("\n", mavis_community, mavis_probability)
        #     print(GRAPH[mavis_community])
        
        # if GRAPH[mavis_community]['rev_count'] > 0:
            # rev_list = remove_subcommunities(GRAPH[mavis_community]["rev"])
            # if EXPLORE_DEBUG_FLAG:
            #     print("\nFor", mavis_community, "%", mavis_probability, "following reverse paths", rev_list)
            # for r in rev_list:
            #     if r not in PATHS:
            #         PATHS.append(r)
    
    PATHS += nodelist
    children = find_all_child_nodes(nodelist, GRAPH, True)
    # print("\nchildren of", nodelist, "are", children)
    PATHS += children
    while len(children) > 0:
        children = find_all_child_nodes(children, GRAPH, True)
        children = remove_duplicates(children, PATHS, True)
        PATHS += children
    

    # grandchildren = find_all_child_nodes(children, GRAPH, True)
    # PATHS += grandchildren


    # cmnties_found = breadth_first_recursive_search(nodelist, GRAPH, PATHS, True)

    # while cmnties_found > 0:
    #     cmnties_found = breadth_first_recursive_search(PATHS, GRAPH, PATHS, True)
        
    pathset = set(PATHS)
    new_paths = list(pathset)

    print("\n\nThere are", len(pathset), "nodes")
    print("\n\nPaths\n\n", pathset)
    # print("\nPaths")
    # for p in PATHS:
    #     print(p)
