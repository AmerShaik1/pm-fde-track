import requests
import csv

response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = response.json()

with open("posts_output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "title"])

    for post in posts[:10]:
        writer.writerow([post["id"], post["title"]])

print("Done! Saved 10 posts to posts_output.csv")