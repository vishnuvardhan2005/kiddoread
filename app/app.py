from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "this-is-a-mission"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

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
    return "kiddoread home"

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return "register user";
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

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
        email = request.form.get('email')
        password = request.form.get('password')

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

@app.route("/question", methods=['GET', 'POST'])
@jwt_required()
def question():
    if request.method == 'GET':
        return "Get question, restricted"
    else:
        return "Update question, restricted"


if __name__ == '__main__':
    app.run(debug=True)