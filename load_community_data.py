"""
    either loads from source or loads from database, the necessary datasets to be processed
    to find succession pathways for NVC communities
"""

# pylint: disable=line-too-long

import sqlite3
import csv
import pandas as pd

NVC_DATABASE_NAME = "nvc.db"

# here's the query to load communities data from the nvc sqlite database
LOAD_COMMUNITIES_QUERY = """
SELECT
  communities.community_level_code,
  communities.community_code,
  communities.community_name
FROM
  communities
"""

LOAD_COMMUNITY_NODES_QUERY = """
SELECT DISTINCT
  communities.community_level_code,
  communities.community_name
FROM
  communities
"""

LOAD_SHORT_COMMUNITY_NODES_QUERY = """
SELECT DISTINCT
  communities.community_level_code
FROM
  communities
"""

# column names to zip up with returned database columns to make them into dictionaries
COLUMN_NAMES = ['community', 'code', 'name', 'list', 'succession']
NODE_COLUMN_NAMES = ['id', 'name']
SHORT_NODE_COLUMN_NAMES = ['id']


def load_communities_table_from_database(database_name, query_string):
    """loads the communities list from the communities database, 
    using the suppled database_name and SQL query_string"""
    load_communities = []
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    for row in cur.execute(query_string):
        # print(row[0], row[1], row[2])
        current_row_list = list(row)
        current_row_list.append([])  # placeholder for names list
        current_row_list.append([])  # placeholder for succession pathways
        current_row = dict(zip(COLUMN_NAMES, current_row_list))

        community_name = current_row['name']
        community_name_list = community_name.lower().split(" ")
        current_row['list'] = community_name_list
        # print(current_row)
        load_communities.append(current_row)

    con.close()
    return load_communities


def _load_communities_nodes_from_database(database_name, query_string, verbose=False):
    """loads the communities list from the communities database, 
    using the suppled database_name and SQL query_string"""
    load_communities = []
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    for row in cur.execute(query_string):
        # print(row[0], row[1], row[2])
        current_row_list = list(row)
        current_row = dict(zip(SHORT_NODE_COLUMN_NAMES, current_row_list))
        if verbose:
            print(current_row)
        if current_row['id'] not in load_communities:
            load_communities.append(current_row)

    con.close()
    return load_communities


def remove_carriage_returns(text_to_clean):
    """strips carriage_returns and asterisks from text string 
    and replaces with spaces and nothing"""
    cleaned_text = text_to_clean.replace("*", " ").replace("  ", " ").replace("\n", "").replace("\n", "")
    # cleaned_text_2 = cleaned_text_1.replace("\n", "")
    return cleaned_text


def load_succession_text_from_csv(csv_filename):
    """read zonation and succession text from CSV file"""
    succession_texts = {}
    with open(csv_filename, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # print(', '.join(row))
            succession_texts[row[0]] = row[1]
    return succession_texts


def load_communities_graph_nodes(verbose=False):
    """load up the communities data into a pandas dataframe"""
    if verbose:
        print("\nLoad Communities Nodes\n")
    cmnty = _load_communities_nodes_from_database(NVC_DATABASE_NAME, LOAD_SHORT_COMMUNITY_NODES_QUERY, verbose=False)
    cmnty_node_df = pd.DataFrame(cmnty)
    if verbose:
        print(cmnty_node_df)
    return cmnty_node_df


# SUCCESSION_TEXTS = load_succession_text_from_csv("succession_text.csv")
# for k, t in SUCCESSION_TEXTS.items():
#     print("**", k, "**", t)
#     print()

if __name__ == "__main__":
    load_communities_graph_nodes(True)
