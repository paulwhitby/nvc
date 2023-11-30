"""
    either loads from source or loads from database, the necessary datasets to be processed
    to find succession pathways for NVC communities
"""
import sqlite3
import csv

NVC_DATABASE_NAME = "nvc.db"
SUCCESSION_TEXTS = {}
SUCCESSION_TEXTS_FILENAME = "succession_text.csv"


# alternative community names - these need to be added to the communities database in a new column
ALTERNATIVE_NAMES = {
    'mg2':  """Filipendulo-Arrhenatheretum""",
    'mg5':  """Cynosurus-Caltha""",
    'mg6':  """Lolio-Cynosuretum""",
    'mg7':  """Lolio-Plantaginion""",
    'mg10': """Holco-Juncetum""",
    'mg12': """Potentillo-Festucetum"""
}

# reasons why succession might take place. To be extended
SUCCESSION_DRIVERS = ('grazing-stopped', 'grazing-started',
                      'ploughing-stopped', 'ploughing-started',
                      'wetting', 'drying', 'fire')

# here's the query to load communities data from the nvc sqlite database
LOAD_COMMUNITIES_QUERY = """
SELECT
  communities.community_level_code,
  communities.community_code,
  communities.community_name
FROM
  communities
"""

# column names to zip up with returned database columns to make them into dictionaries
COLUMN_NAMES = ['community', 'code', 'name', 'list', 'succession']


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


def remove_carriage_returns(text_to_clean):
    """strips carriage_returns and asterisks from text string 
    and replaces with spaces and nothing"""
    cleaned_text = text_to_clean.replace("*", " ").replace("\n", "")
    # cleaned_text_2 = cleaned_text_1.replace("\n", "")
    return cleaned_text


def load_succession_text_from_csv(csv_filename):
    """read zonation and succession text from CSV file"""
    succession_texts = {}
    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # print(', '.join(row))
            succession_texts[row[0]] = row[1]
    return succession_texts


# SUCCESSION_TEXTS = load_succession_text_from_csv("succession_text.csv")
# for k, t in SUCCESSION_TEXTS.items():
#     print("**", k, "**", t)
#     print()
