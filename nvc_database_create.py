"""Create nvc database tables"""
import sqlite3

def create_nvc_database():
    con = sqlite3.connect("nvc.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE communities(community_key, community_code, community_name, community_level_code)")
    cur.execute("CREATE TABLE species(species_key, species_name)")
    cur.execute("CREATE TABLE community_species(community_key, species_key, abundance, frequency, special)")
    con.commit()
    for row in cur.execute("SELECT * from sqlite_master"):
        print(row)
    con.close()

def create_succession_database():
    con = sqlite3.connect("nvc.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE succession(succession_key, from_community_key, to_community_key, probability)")
    cur.execute("CREATE TABLE conditions(condition_key, condition_name)")
    cur.execute("CREATE TABLE succession_conditions(succession_key, condition_key)")
    con.commit()
    for row in cur.execute("SELECT * from sqlite_master"):
        print(row)
    con.close()

