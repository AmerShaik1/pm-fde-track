import sqlite3

connection = sqlite3.connect("apprenticeship.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        city TEXT
    )
""")

connection.commit()
print("Table created successfully")