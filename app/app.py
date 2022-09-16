from flask import Flask, jsonify, request,redirect, url_for
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin

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

CORS(app, support_credentials=True)
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
db = client.kiddoreadDB

users = db.users
questions = db.questions
gameState = db.gameState
history = db.history

# routes
@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def home():
    return jsonify({"message": "This is a message from flask app"}), 200

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

        #Also update gameState table
        gameState.insert_one({'email':email, 'nextQuestionId':1, 'score':0})
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
    global questions
    if request.method == 'GET':
        #get emailid
        email = get_jwt_identity()
        #get gameState record
        state = gameState.find_one({'email':email})        
        #get question
        next_question_id = state['nextQuestionId']

        questionRecord = questions.find_one({'id':next_question_id})
        score = state['score']

        if not questionRecord:
            return "No question to return"

        return jsonify({'email':email, 'score':state['score'], 'question':questionRecord['question']})
    else:
        data = json.loads(request.data)
        
        email = get_jwt_identity()
        question = data['question']
        answer = data['answer']

        state = gameState.find_one({'email':email})
        score = state['score']

        #update score
        if question == answer:
            score += 5

        curr_question_id =  state['nextQuestionId']
        next_question_id = curr_question_id + 1
        gameState.update_one({'email':email}, { "$set": { 'nextQuestionId': next_question_id, 'score':score } })
        history.insert_one({'email':email, 'questionId':curr_question_id, 'question':question, 'answer':answer})

        return redirect(url_for('question'))

@app.route("/questionDB", methods=['GET', 'POST'])
@jwt_required()
def dump_questions():
    global questions
    if request.method == 'GET':
        questions = questions.find({})
        for q in questions:
            print(q)
        return "questions read"
    else:
        try:
            db.validate_collection("questions")  # Try to validate a collection
            return "QuestionDB already populated"
        except pymongo.errors.OperationFailure:  # If the collection doesn't exist
            #populate questions
            i = 0
            words = ['phone', 'door', 'fan', 'road','car']
            for word in words:
                i += 1
                questions.insert_one({'id':i,'question':word})
            
            return "Questions created"

        return ""

@app.route("/clearQuestionDB", methods=['POST'])
@jwt_required()
def clear_questions():
    questions.delete_many({})
    return "Question cleared"


@app.route("/clearAll", methods=['POST'])
@jwt_required()
def clear_all():
    users.delete_many({})
    questions.delete_many({})
    return "All cleared"

if __name__ == '__main__':
    app.run(debug=True)