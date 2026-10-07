import sqlite3

connection = sqlite3.connect("apprenticeship.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute("SELECT * FROM customers WHERE age > 30")
rows = cursor.fetchall()

for row in rows:
    print(row)