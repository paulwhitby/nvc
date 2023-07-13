import sqlite3
import time

# communities(community_key, community_code, community_name, community_level_code)
# species(species_key, species_name)
# community_species(community_key, species_key, abundance, frequency, special)

list_all = """ 
                           
        SELECT
            community_key,
            species_name,
            abundance,
            frequency
        FROM
        community_species
        INNER JOIN species USING(species_key);
                           
        """

list_all_h1 = """ 
                           
        SELECT
            community_level_code,
            species_name,
            abundance,
            frequency
        FROM
        community_species
        INNER JOIN species USING(species_key)
        INNER JOIN communities USING(community_key);
                           
        """

list_three_table_join = """
SELECT
  community_species.community_key AS commkey,
  communities.community_name AS commname,
  communities.community_level_code AS levelcode,
  community_species.species_key AS speckey,
  species.species_name AS specname,
  community_species.abundance AS abund,
  community_species.frequency AS freq
FROM 
  community_species 
  LEFT JOIN communities ON community_species.community_key = communities.community_key
  LEFT JOIN species ON community_species.species_key = species.species_key;
"""

list_three_table_join_where = """
SELECT
  community_species.community_key AS commkey,
  communities.community_name AS commname,
  communities.community_level_code AS levelcode,
  communities.community_code AS commcode,
  community_species.species_key AS speckey,
  species.species_name AS specname,
  community_species.abundance AS abund,
  community_species.frequency AS freq
FROM 
  community_species 
  LEFT JOIN communities ON community_species.community_key = communities.community_key
  LEFT JOIN species ON community_species.species_key = species.species_key
WHERE commcode = 'W16a';
"""

list_communities_species_join = """
SELECT
  community_species.community_key AS commkey,
  communities.community_name AS commname,
  communities.community_level_code AS levelcode,
  community_species.species_key AS speckey,
  community_species.abundance AS abund,
  community_species.frequency AS freq
FROM 
  community_species 
  LEFT JOIN communities ON community_species.community_key = communities.community_key;
"""

list_communities = """
SELECT
  communities.community_key,
  communities.community_name,
  communities.community_level_code,
  communities.community_code
FROM 
  communities
"""

list_community_keys = """
SELECT
  communities.community_key
FROM 
  communities
"""

list_community_names = """
SELECT
  communities.community_name
FROM 
  communities
"""

list_community_species = """
SELECT
  community_species.community_key,
  community_species.species_key
 FROM 
  community_species
"""

list_row_counts = """ select count(*) from species"""

def query_join():
    con = sqlite3.connect("nvc.db")
    cur = con.cursor()

    for row in cur.execute(list_three_table_join_where):
        print(' | '.join(row))
        # time.sleep(0.2)
    
    con.close()

query_join()
