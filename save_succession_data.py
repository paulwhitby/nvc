"""write computed succession data to the nvc database"""

import sqlite3


QUERY_INSERT_STRING = "INSERT INTO succession VALUES(?, ?, ?, ?)"
QUERY_CHECK_STRING = "select count(*) from succession"
DATABASE_NAME = "nvc.db"


# table created with
# "CREATE TABLE succession(succession_key, from_community_key, to_community_key, probability)"

"""{
    'community': 'W9', 
    'code': 'W9b', 
    'name': 'Fraxinus excelsior-Sorbus aucuparia-Mercurialis perennis woodland, Crepis paludosa sub-community', 
    'list': ['fraxinus', 'excelsior-sorbus', 'aucuparia-mercurialis', 'perennis', 'woodland,', 'crepis', 'paludosa', 'sub-community'], 
    'succession': ['W9', 'W11', 'W17', 'W7', 'W8', 'CG10', 'CG9', 'CG13', 'M10', 'MG3']
    }"""

def _save_succession_data(database_name, query_string, communities, check_string):
    """write succession data from communities list to nvc database"""
    # open database
    con = sqlite3.connect(database_name)

    # create cursor
    cur = con.cursor()

    for community in communities:
        # iterate over communities list
        if community['succession'] != []:
            for community_succession in community['succession']:
                # print(', '.join(row))
                succession_key = community['community'].upper()+community['code'].upper()+community_succession.upper()
                insert_row = (succession_key, community['code'], community_succession, '0.5')
                print(insert_row)
                cur.execute(query_string, insert_row)
                con.commit()
    for row in cur.execute(check_string):
        print(row, "records")

    con.close()


def save_succession_data(communities):
    """external interface to _save_succession_data()"""
    _save_succession_data(DATABASE_NAME, QUERY_INSERT_STRING, communities, QUERY_CHECK_STRING)
