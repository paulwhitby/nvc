"""display graph of community nodes"""

# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import, wildcard-import
# pylint: disable=trailing-whitespace
# pylint: disable=unused-import
# pylint: disable=pointless-string-statement
# pylint: disable=invalid-name

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
    edge_df = edge_df.fillna(value=0)
    # add edge labels
    edge_df.loc[:, 'fr'] = edge_df.loc[:, 'from']
    edge_df.loc[:, 'sum'] = edge_df.loc[:, 'grazing']+edge_df.loc[:, 'grazingstopped']+edge_df.loc[:, 'flooding']+edge_df.loc[:, 'wetting']+edge_df.loc[:, 'drying']+edge_df.loc[:, 'myxomatosis']+edge_df.loc[:, 'fire']+edge_df.loc[:, 'ploughingstarted']+edge_df.loc[:, 'ploughingstopped']+edge_df.loc[:, 'mowing']+edge_df.loc[:, 'mowingstopped']+edge_df.loc[:, 'clearance']+edge_df.loc[:, 'abandonment']
    edge_df.loc[:, 'label'] = edge_df.loc[:, 'sum'].astype(str)

    node_df = load_succession_data.make_df_from_graph_nodes(load_succession_data.load_succession_into_forward_dict(verbose=DEBUG_ON), load_succession_data.load_succession_into_reverse_dict(verbose=DEBUG_ON), verbose=DEBUG_ON)
    node_df = node_df.fillna(0)

    print(edge_df)
    print(node_df)
    Jaal(edge_df, node_df).plot(directed=True, vis_opts={'height': '1500px', 'width':'1500px', 'interaction':{'hover': False},
                                      'physics':{'stabilization':{'iterations': 100}}})
    # Jaal(edge_df).plot(directed=True)
