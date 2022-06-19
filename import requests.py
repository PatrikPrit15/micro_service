import requests
response = requests.post('https://jsonplaceholder.typicode.com/posts', data= {"title": 'foo',"body": 'bar',"userId": "1",})

response_put = requests.put('https://jsonplaceholder.typicode.com/posts/1', data= {"title": 'some title',"body": 'grass is green',"userId": 1,"id": 1 ,})
response_get = requests.get('https://jsonplaceholder.typicode.com/posts/101')

response_del = requests.delete('https://jsonplaceholder.typicode.com/posts/10')
print(response.json(),response)  
print()
print(response_put.json(),response_put)
print()
print(response_del.json(),response_del)
print()
print(response_get.json(),response_get)


# @app.route("/users/<user_id>/")
# def get_user(user_id):
#     data = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}/")
#     if data.status_code == 200:
#         return data.json()
#     return f"error code {data.status_code}"

# @app.route("/users/")
# def get_users():
#     data = requests.get(f"https://jsonplaceholder.typicode.com/users/")
#     if data.status_code == 200:
#         return json.dumps(data.json())
#     return f"error code {data.status_code}"