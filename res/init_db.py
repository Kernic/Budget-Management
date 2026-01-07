import os.path
import sqlite3
from sqlite3 import Error
import random
import pandas as pds
import string

if __name__ == "__main__":
    create_table = """CREATE TABLE IF NOT EXISTS raw_data (
    id INTEGER PRIMARY KEY,
    name text NOT NULL,
    operation_type text NOT NULL, 
    operator text NOT NULL,
    operation FLOAT NOT NULL,
    date DATE
);"""
    if os.path.exists(r"./db/main.db"):
        os.remove(r"./db/main.db")
    connection = None
    try:
        connection = sqlite3.connect(r"./db/main.db")
    except Error as e:
        print(f"An Error was found {e}")
    empty_data_list = {
        "name": [],
        "operation type": [],
        "operator": [],
        "operation": [],
        "Date": []
    }

    empty_data = pds.DataFrame(empty_data_list)
    print(empty_data)
    if type(connection) != type(None):
        empty_data.to_sql(name="raw_data", con=connection, if_exists="replace")
        # To Add empty table with global variable like balance, last update

    pass