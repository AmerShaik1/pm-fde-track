import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()

print("Title:", data["title"])
print("Post ID:", data["id"])
print("User ID:", data["userId"])

response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = response.json()

print("Number of posts:", len(posts))

for post in posts[:5]:
    print(post["id"], "-", post["title"])

