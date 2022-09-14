from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

try:
    client = MongoClient('mongodb://localhost:27017/')
except:
    print("Failed to connect to db")

db = client.kiddoread_db

#user collection
users = db.users

# routes
@app.route("/", methods=['GET'])
def home():
    return "hello world"

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return "";
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        #check if email already exists
        result = users.find_one({"email": email})
        if result:
            return "User exists"

        #hash the password
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #validate input
        user_input = {'name': name, 'email': email, 'password': hash_password}

        users.insert_one(user_input)
        return "record inserted"


@app.route("/login", methods=['GET', 'POST'])
def login_user():
    return ""

@app.route("/question", methods=['GET', 'POST'])
def question():
    return ""

if __name__ == '__main__':
    app.run(debug=True)