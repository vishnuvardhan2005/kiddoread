from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt

import json
import pymongo

app = Flask(__name__)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "this-is-a-mission"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

try:
    client = MongoClient('mongodb://localhost:27017/')
except:
    print("Failed to connect to db")
    exit(1)

# db and collections
db = client.kiddoread_db

#user collection
users = db.users
questions_collection = db.questions

# routes
@app.route("/", methods=['GET'])
def home():
    return "kiddoread home"

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return "register user";
    else:
        data = json.loads(request.data)

        name = data['name']
        email = data['email']
        password = data['password']

        #check if email already exists
        result = users.find_one({"email": email})
        if result:
            return "User exists"

        #hash the password
        #hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hash_password = bcrypt.generate_password_hash(password)

        #validate input
        user_input = {'name': name, 'email': email, 'password': hash_password}

        users.insert_one(user_input)
        return "user register"


@app.route("/login", methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return "login user"
    else:
        data = json.loads(request.data)
        email = data['email']
        password = data['password']

        #validations
        #result = users.find_one({'email':email, 'password':hash_password})

        result = users.find_one({'email':email})

        if not result:
            return "Invalid credentials"

        hash_password = result['password']

        if bcrypt.check_password_hash(hash_password, password) == False: #
            return "Invalid password"

        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

@app.route("/logout", methods=['GET','POST'])
@jwt_required()
def logout_user():
    return ""

@app.route("/question", methods=['GET', 'POST'])
@jwt_required()
def question():
    if request.method == 'GET':
        return "Get question, restricted"
    else:
        return "Update question, restricted"

@app.route("/questionDB", methods=['GET', 'POST'])
@jwt_required()
def dump_questions():
    if request.method == 'GET':
        questions = questions_collection.find({})
        for q in questions:
            print(q)
        return "questions read"
    else:

        try:
            db.validate_collection("questions_collection")  # Try to validate a collection
            return "QuestionDB already populated"
        except pymongo.errors.OperationFailure:  # If the collection doesn't exist
            #populate questions
            i = 0
            questions = ['phone', 'door', 'fan', 'road','car']
            for ques in questions:
                i += 1
                questions_collection.insert_one({'id':i,'question':ques})
            
            return "Questions inserted"

        return ""

@app.route("/clearQuestionDB", methods=['POST'])
@jwt_required()
def clear_questions():
    questions_collection.delete_many({})
    return "Question DB cleared"

if __name__ == '__main__':
    app.run(debug=True)