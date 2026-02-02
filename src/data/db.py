import sqlite3 as sql
from sqlite3 import Connection, Cursor

import pandas as pds

# ------------------------------------------------------------------------------#
# Database Getting values
# ------------------------------------------------------------------------------#


def get_values_as_dataframe(query: str) -> pds.DataFrame:
    conn = open_connection()
    df = pds.read_sql_query(query, conn)
    close_connection(conn)
    return df


def get_value(query: str) -> str:
    conn = open_connection()
    cursor = return_cursor(conn)
    cursor.execute(query)
    result = cursor.fetchone()
    close_connection(conn)
    return result[0]


def insert_values_as_dataframe(table: str, df: pds.DataFrame) -> None:
    conn = open_connection()
    df.to_sql(table, conn, if_exists="append", index=False)
    close_connection(conn)


def update_value(table: str, column: str, index: int, value: str) -> None:
    conn = open_connection()
    cursor = return_cursor(conn)
    cursor.execute(f"UPDATE {table} SET {column} = ? WHERE id = ?", (value, index))
    conn.commit()
    close_connection(conn)


# ------------------------------------------------------------------------------#
# Database connection functions
# ------------------------------------------------------------------------------#


def open_connection() -> Connection:
    """
    Open a connection to the SQLite database.
    """
    conn = sql.connect("../res/data/db.sql")
    return conn


def return_cursor(conn: Connection) -> Cursor:
    """
    Return a cursor object for the given connection.
    """
    cur = conn.cursor()
    return cur


def close_connection(conn: Connection) -> None:
    """
    Close the connection to the SQLite database.
    """
    conn.close()


def create_tables() -> None:
    """
    Creating the default tables for the project, do not use in main
    """
    conn = open_connection()
    cursor = return_cursor(conn)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_values (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value REAL NOT NULL
        );
    """)

    cursor.execute("""
        INSERT INTO global_values (key, value) VALUES ('balance', '0.0');
    """)

    cursor.execute("""
        INSERT INTO global_values (key, value) VALUES ('last_update_date', '01/01/0001');
    """)

    cursor.execute("""
        INSERT INTO global_values (key, value) VALUES ('oldest_date', '31/12/9999');
    """)

    conn.commit()
    close_connection(conn)


def drop_tables() -> None:
    """
    Used to drop tables for testing purposes
    """
    conn = open_connection()
    cursor = return_cursor(conn)

    cursor.execute("DROP TABLE IF EXISTS operations;")
    cursor.execute("DROP TABLE IF EXISTS global_values;")
    conn.commit()
    close_connection(conn)


if __name__ == "__main__":
    create_tables()
