import sqlite3

connection = sqlite3.connect("apprenticeship.db")
cursor = connection.cursor()

cursor.execute("INSERT INTO customers (name, age, city) VALUES ('Amer', 36, 'Atlanta')")
cursor.execute("INSERT INTO customers (name, age, city) VALUES ('Sara', 29, 'New York')")
cursor.execute("INSERT INTO customers (name, age, city) VALUES ('Tom', 42, 'Chicago')")

connection.commit()
print("Data inserted successfully")