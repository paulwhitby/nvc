import sqlite3
import csv

# open database
con = sqlite3.connect("nvc.db")

# create cursor
cur = con.cursor()

# open community csv
with open('community.csv') as community_file:
    reader = csv.reader(community_file)
    # iterate over community file
    #    read row
    for row in reader:
        print(', '.join(row))
        #    write row to database
        res = cur.execute("INSERT INTO community(?, ?, ?, ?)", row)
        con.commit()


# do same for other 2 files / tables

