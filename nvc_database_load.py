import sqlite3
import csv

# communities(community_key, community_code, community_name, community_level_code)
# species(species_key, species_name)
# community_species(community_key, species_key, abundance, frequency, special)

def load_database():
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
            print(', '.join(row))
            cur.execute("INSERT INTO communities VALUES(?, ?, ?, ?)", row)
            con.commit()


    # open species_csv
    print("Loading species_csv")
    with open('species_csv.csv') as species_file:
        reader = csv.reader(species_file)
        # iterate over species file
        for row in reader:
            print(', '.join(row))
            cur.execute("INSERT INTO species VALUES(?, ?)", row)
            con.commit()


    # open community_species_csv
    print("Loading community_species_csv")
    with open('community_species_csv.csv') as community_species_file:
        reader = csv.reader(community_species_file)
        # iterate over community_species file
        for row in reader:
            print(', '.join(row))
            cur.execute("INSERT INTO community_species VALUES(?, ?, ?, ?, ?)", row)
            con.commit()
    
    con.commit()
    con.close()

