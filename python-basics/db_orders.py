import sqlite3

connection = sqlite3.connect("apprenticeship.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT,
        amount INTEGER
    )
""")

cursor.execute("INSERT INTO orders (customer_id, product, amount) VALUES (1, 'Laptop', 1200)")
cursor.execute("INSERT INTO orders (customer_id, product, amount) VALUES (1, 'Mouse', 25)")
cursor.execute("INSERT INTO orders (customer_id, product, amount) VALUES (2, 'Keyboard', 75)")

connection.commit()
print("Orders table created and populated")
