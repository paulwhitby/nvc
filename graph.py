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

    DEBUG_ON = True

    edge_df = load_succession_data.load_succession_graph_edges(DEBUG_ON)
    # node_df = load_community_data.load_communities_graph_nodes(DEBUG_ON)
    node_df = load_succession_data.make_df_from_graph_nodes(load_succession_data.load_succession_into_forward_dict(verbose=DEBUG_ON), load_succession_data.load_succession_into_reverse_dict(verbose=DEBUG_ON), verbose=DEBUG_ON)

    print(edge_df)
    print(node_df)
    Jaal(edge_df, node_df).plot(directed=True)
    # Jaal(edge_df).plot()

"""
to=='MG6' or to=='CG10' or to=='CG14' or to=='OV40' or to=='W20' or to=='M11' or to=='U16' or to=='W17' or to=='H8'
"""