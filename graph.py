"""display graph of community nodes"""

# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import, wildcard-import
# pylint: disable=trailing-whitespace
# pylint: disable=unused-import
# pylint: disable=pointless-string-statement

from jaal import Jaal
import pandas as pd
import load_succession_data
import load_community_data


if __name__ == "__main__":
    node_df = pd.DataFrame()
    edge_df = pd.DataFrame()

    DEBUG_ON = False

    # succession_drivers_list = load_succession_data.load_distinct_succession_drivers()
    community_succession = load_succession_data.load_succession_drivers_into_list()

    edge_df = load_succession_data.load_succession_graph_edges(False)
    # edge_df["explore"] = 0

    # add a column in the dataframe for each succession driver
    # for sd in succession_drivers_list:
    #     edge_df[sd] = 0
    
    # print("\n\nSuccession drivers", succession_drivers_list, "\n\n")
    # for d in community_succession:
    #     for edge in edge_df:
    #         if edge['from'] == d['community_key']:
    #             edge[d['succession_reason']] = 1

    # node_df = load_community_data.load_communities_graph_nodes(DEBUG_ON)
    node_df = load_succession_data.make_df_from_graph_nodes(load_succession_data.load_succession_into_forward_dict(verbose=DEBUG_ON), load_succession_data.load_succession_into_reverse_dict(verbose=DEBUG_ON), verbose=DEBUG_ON)

    print(edge_df)
    print(node_df)
    Jaal(edge_df, node_df).plot(directed=True, vis_opts={'height': '4000px', 'interaction':{'hover': False},
                                      'physics':{'stabilization':{'iterations': 100}}})
    # Jaal(edge_df).plot(directed=True)

"""
to=='MG6' or to=='CG10' or to=='CG14' or to=='OV40' or to=='W20' or to=='M11' or to=='U16' or to=='W17' or to=='H8'

fwd_count>0 and rev_count==0

"""