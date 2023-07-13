import sqlite3

def create_database():
    con = sqlite3.connect("nvc.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE communities(community_key, community_code, community_name, community_level_code)")
    cur.execute("CREATE TABLE species(species_key, species_name)")
    cur.execute("CREATE TABLE community_species(community_key, species_key, abundance, frequency, special)")
    con.commit()
    con.close()

