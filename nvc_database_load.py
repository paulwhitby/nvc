import sqlite3
import csv

# communities(community_key, community_code, community_name, community_level_code)
# species(species_key, species_name)
# community_species(community_key, species_key, abundance, frequency, special)

def database_load():
    # open database
    con = sqlite3.connect("nvc.db")

    # create cursor
    cur = con.cursor()

    # open community_csv
    with open('community_csv.csv') as community_file:
        reader = csv.reader(community_file)
        # iterate over community file
        #    read row
        for row in reader:
            # print(', '.join(row))
            #    write row to database
            res = cur.execute("INSERT INTO communities(?, ?, ?, ?)", row)
            con.commit()


    # open species_csv
    with open('species_csv.csv') as species_file:
        reader = csv.reader(species_file)
        # iterate over community file
        #    read row
        for row in reader:
            # print(', '.join(row))
            #    write row to database
            res = cur.execute("INSERT INTO community_species(?, ?)", row)
            con.commit()


    # open community_species_csv
    with open('community_species_csv.csv') as community_species_file:
        reader = csv.reader(community_species_file)
        # iterate over community file
        #    read row
        for row in reader:
            # print(', '.join(row))
            #    write row to database
            res = cur.execute("INSERT INTO species(?, ?, ?, ?, ?)", row)
            con.commit()
    
    con.commit()
    con.close()

