import sqlite3

def get_connection():
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    #neccesario per far funzionare le foreign key
    con.execute("PRAGMA foreign_keys = 1;")

    return con
