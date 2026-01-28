import sqlite3 as sql
from sqlite3 import Connection, Cursor

# ------------------------------------------------------------------------------#
# Database connection functions
# ------------------------------------------------------------------------------#


def open_connection() -> Connection:
    """
    Open a connection to the SQLite database.
    """
    conn = sql.connect("./res/data/db.sql")
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


# ------------------------------------------------------------------------------#
# Temporary database functions
# ------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------#
# Temporary database functions
# ------------------------------------------------------------------------------#


def create_tables() -> None:
    """
    Creating the default tables for the poject, do not use in main
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
