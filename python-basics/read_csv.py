import csv

with open("customers.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)
    print("Columns:", header)

    for row in reader:
        name = row[0]
        age = int(row[1])
        city = row[2]
        print(f"{name} is {age + 1} years old and lives in {city}")