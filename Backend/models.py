from dotenv import load_dotenv,find_dotenv
from pymongo import MongoClient 
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from flask_login import UserMixin
from datetime import datetime
import os

bcrypt = Bcrypt()

load_dotenv(find_dotenv())

password = os.getenv("MONGODB_PWD")

connection_string=f"mongodb+srv://bharathh30:{password}@cluster0.2v8j4dk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self._id = str(user_id)
        self.username = username
        self.email = email
        self.password = password
        self.active = True

    @property
    def is_active(self):
        return self.active
    
    @property
    def is_authenticated(self):
        return True

    @property
    def id(self):
        return self._id

db = client.Ekamatra
ekamatra_collections = db['Ekamatra-c']
blog_collections = db['Blog-c']

# print(db.list_collection_names())

def add_user(username,email,password):
    user_data = {
        'username': username,
        'email': email,
        'password': bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password before storing it
    }

    user_id=ekamatra_collections.insert_one(user_data).inserted_id
    return User(user_id, username, email, user_data['password'])

def get_user_by_email(email):
    user_data = ekamatra_collections.find_one({'email': email})
    if user_data:
        return User(user_data['_id'], user_data['username'], user_data['email'], user_data['password'])
    return None

def get_user_by_username(username):
    user_data = ekamatra_collections.find_one({'username': username})
    if user_data:
        return User(user_data['_id'], user_data['username'], user_data['email'], user_data['password'])
    return None



def get_user_by_id(user_id):
    user_data = ekamatra_collections.find_one({'_id': ObjectId(user_id)})
    if user_data is not None:
        return User(user_data['_id'], user_data['username'], user_data['email'], user_data['password'])
    else:
        return None
    

# user post insertion in blog collection
def insert_blog_post(title,content,author_id):
     # Retrieve the user object based on the author_id
    user = ekamatra_collections.find_one({'_id': ObjectId(author_id)})
    if user:
        username = user['username']

    else:
        username = "EkaMatra"

    post = {
        "title" : title,
        "content" : content,
        "authorId" : author_id,
        "authorUsername" : username,
        "timestamp" : datetime.now()
    }

    blog_collections.insert_one(post)

# get all blog posts in descending order (latest first)
def get_blog_posts():
    return blog_collections.find().sort('timestamp', -1)

def delete_post_in_collections(post_id):
    # Delete the post
    blog_collections.delete_one({'_id': ObjectId(post_id)})