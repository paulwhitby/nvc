"""Create nvc database tables"""

# pylint: disable=line-too-long

import sqlite3


def create_nvc_database():
    """create the database tables for storing nvc data"""
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
    """create the database tables for storing succession data"""
    con = sqlite3.connect("nvc.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE succession(succession_key, from_community_key, to_community_key, probability)")
    cur.execute("CREATE TABLE conditions(condition_key, condition_name)")
    cur.execute("CREATE TABLE succession_conditions(succession_key, succession_reason)")
    cur.execute("CREATE TABLE community_drivers(community_key, succession_reason)")
    con.commit()
    for row in cur.execute("SELECT * from sqlite_master"):
        print(row)
    con.close()
