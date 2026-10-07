import requests

new_post = {
    "title": "My first post",
    "body": "Learning APIs as part of my FDE apprenticeship",
    "userId": 1
}

response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)

print(response.status_code)
print(response.json())