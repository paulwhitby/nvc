import sqlite3
import csv

# communities(community_key, community_code, community_name, community_level_code)
# species(species_key, species_name)
# community_species(community_key, species_key, abundance, frequency, special)


def load_table(database_name, csv_file_name, query_string, check_string):
    # open database
    con = sqlite3.connect(database_name)

    # create cursor
    cur = con.cursor()

    # open csv
    print("Loading ", csv_file_name)
    with open(csv_file_name) as csv_file:
        reader = csv.reader(csv_file)
        # iterate over community file
        for row in reader:
            # print(', '.join(row))
            cur.execute(query_string, row)
            con.commit()
    for row in cur.execute(check_string):
        print(row, "records")
    
    con.close()


def load_database_old():
    # open database
    con = sqlite3.connect("nvc.db")

    # create cursor
    cur = con.cursor()


    # open community_csv
    print("Loading community_csv")
    with open('community_csv.csv') as community_file:
        reader = csv.reader(community_file)
        # iterate over community file
        for row in reader:
            # print(', '.join(row))
            cur.execute("INSERT INTO communities VALUES(?, ?, ?, ?)", row)
            con.commit()
    for row in cur.execute("select count(*) from communities"):
        print(row, "records")


    # open species_csv
    print("Loading species_csv")
    with open('species_csv.csv') as species_file:
        reader = csv.reader(species_file)
        # iterate over species file
        for row in reader:
            # print(', '.join(row))
            cur.execute("INSERT INTO species VALUES(?, ?)", row)
            con.commit()
    for row in cur.execute("select count(*) from species"):
        print(row, "records")


    # open community_species_csv
    print("Loading community_species_csv")
    with open('community_species_csv.csv') as community_species_file:
        reader = csv.reader(community_species_file)
        # iterate over community_species file
        for row in reader:
            # print(', '.join(row))
            cur.execute("INSERT INTO community_species VALUES(?, ?, ?, ?, ?)", row)
            con.commit()
    for row in cur.execute("select count(*) from community_species"):
        print(row, "records")


    con.commit()
    con.close()


def load_database():
    load_table("nvc.db", "community_csv.csv", "INSERT INTO communities VALUES(?, ?, ?, ?)", "select count(*) from communities")
    load_table("nvc.db", "Loading species_csv", "INSERT INTO species VALUES(?, ?)", "select count(*) from species")
    load_table("nvc.db", "Loading community_species_csv", "INSERT INTO community_species VALUES(?, ?, ?, ?, ?)", "select count(*) from community_species")
