import sqlite3
import csv
import nvc_database_create
import nvc_database_load

nvc_database_create.create_database()
nvc_database_load.load_database()
