import os.path
import sqlite3 as db

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
    #with db.connect(r"./db/main.db") as conn:
    #    cur = conn.cursor()
    #    cur.execute(create_table)
    #    conn.commit()
    pass