import requests
import json
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///posts.db"
db=SQLAlchemy(app) 

class Post(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(100))
    body = db.Column(db.String(10000))

    def __repr__(self):
        return f"userId: {self.userId},id {self.id} title: {self.title}, body: {self.body}"


@app.route("/users/posts/<user_id>/",methods=['GET'])
def get_users_posts(user_id):
    users_data=[]
    if not user_id.isnumeric():
        return f"'{user_id}' is not valid number"
    posts = db.session.query(Post).filter(Post.userId==user_id).all()
    if len(posts)==0:
        return f"No posts for user with id {user_id} on server (na externom api mozno su)"

    for post in posts:
        users_data.append({"id":post.id,"userId":post.userId,"title":post.title, "body":post.body})
    return json.dumps(users_data)


@app.route("/posts/<post_id>/",methods=['GET'])
def get_post(post_id):
    if not post_id.isnumeric():
        return f"'{post_id}' is not valid number"
    post = db.session.query(Post).filter(Post.id==post_id).all()
    if post!=[]:
        return {"id":post[0].id,"userId":post[0].userId,"title":post[0].title, "body":post[0].body}
    data = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}/")
    if data.status_code == 200:
        data=data.json()
        db.session.add(Post(id=data["id"], userId=data["userId"], title=data["title"], body=data["body"]))
        db.session.commit()
        return data
    return f"error code {data.status_code}"

@app.route("/posts/",methods=['POST'])
def add_post():
    userId = request.json["userId"]
    title = request.json["title"]
    body = request.json["body"]
    is_user_valid=requests.get(f"https://jsonplaceholder.typicode.com/users/{userId}/")
    response_from_external_api = requests.post('https://jsonplaceholder.typicode.com/posts', data= {"title": title,"body": body,"userId": userId,})

    if response_from_external_api.status_code != 201:
        return f"error code {response_from_external_api.status_code}"

    if is_user_valid.status_code != 200:
        return "invalid id"
    
    if len(title)>100 or len(body)>10000:
        return "invalid length of title or body"

    if Post.query.all()==[]:
        postid=101
    else:
        postid = max(101,max([p.id for p in Post.query.all()])+1)
    post = Post(id=postid, userId=userId, title=title, body=body)
    db.session.add(post)
    db.session.commit()
    return f"post with id {postid} added"

@app.route("/posts/<post_id>/",methods=['PUT'])
def change_post(post_id):
    title = request.json["title"]
    body = request.json["body"]
    id = request.json["userId"]
    if not post_id.isnumeric() or not type(id)==int:
        return f"'{post_id}' or '{id}' is not valid number"
    post = db.session.query(Post).filter(Post.id==int(post_id)).all()
    if post==[]:
        return f"post with id {post_id} not found"
    else:
        post[0].title=title
        post[0].body=body
    db.session.commit()
    return f"post with id: {post_id} changed"

@app.route("/posts/<post_id>/",methods=['DELETE'])
def delete_post(post_id):
    if not post_id.isnumeric():
        return f"'{post_id}' is not valid number"
    post=db.session.query(Post).filter(Post.id==post_id).first()
    if post is None:
        return f"post with id {post_id} not found"
    db.session.delete(post)
    db.session.commit()
    return f"post with id {post_id} deleted"