import sqlite3

try:
    connection = sqlite3.connect("uploads.db")

    cursor = connection.cursor()
    cursor.execute("CREATE TABLE upload (id integer PRIMARY KEY, file_name TEXT NOT NULL, created_at TEXT, path TEXT "
                   "NOT NULL, status TEXT, user TEXT)")
    print("Successfully Connected to SQLite")

    print("SQLite script executed successfully")
    cursor.close()

except sqlite3.Error as error:
    print("Error while executing sqlite script", error)
finally:
    if connection:
        connection.close()
        print("sqlite connection is closed")
