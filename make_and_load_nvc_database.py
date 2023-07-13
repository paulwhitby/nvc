import sqlite3
import csv
import nvc_database_create
import nvc_database_load

nvc_database_create.create_nvc_database()
nvc_database_load.load_database()
print("nvc database created and loaded")
