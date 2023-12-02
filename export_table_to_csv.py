"""helper function to export any table to any csv file using the supplied SQL query"""
import sqlite3
import csv

# communities(community_key, community_code, community_name, community_level_code)
# species(species_key, species_name)
# community_species(community_key, species_key, abundance, frequency, special)

# succession(succession_key, from_community_key, to_community_key)")
# conditions(condition_key, condition_name)")
# succession_conditions(succession_key, condition_key)")

# https://docs.python.org/3/library/sqlite3.html#sqlite3-howtos
# https://docs.python.org/3/library/csv.html?highlight=csv



def export_table_from_database(database_name, export_file_name, export_query):
    """helper function to export any table from any database to any csv file using the supplied SQL query"""
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    with open(export_file_name, 'w', newline='') as csvfile:
        dumpwriter = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        for row in cur.execute(export_query):
            print(' | '.join(row))
            dumpwriter.writerow(row)

    con.close()


# def export_community_species_database():
#     export_table_to_csv.export_table_from_database("nvc.db", "dumptest_community_species.csv", export_community_species)
