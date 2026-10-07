import sqlite3

connection = sqlite3.connect("apprenticeship.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT customers.name, orders.product, orders.amount
    FROM customers
    JOIN orders ON customers.id = orders.customer_id
""")

rows = cursor.fetchall()
for row in rows:
    print(row)