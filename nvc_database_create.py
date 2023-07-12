import sqlite3

con = sqlite3.connect("nvc.db")
cur = con.cursor()
cur.execute("CREATE TABLE community(key, community, community_code, community_name)")
cur.execute("CREATE TABLE species(species_name)")
cur.execute("CREATE TABLE community_species(community_code, species, abundance, frequency)")
con.commit()
con.close()
