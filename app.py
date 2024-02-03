from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
bcrypt = Bcrypt(app)  # Initialize Bcrypt for salting and hashing

# MongoDB connection details (replace with your actual credentials)
mongo_uri = "mongodb+srv://syedmisbah588:yourpasshere@cluster0.ymmp6sk.mongodb.net/users?retryWrites=true&w=majority"

def get_data_from_mongo():
    client = MongoClient(mongo_uri)
    db = client.users
    collection = db.users
    data = list(collection.find({}))  # Fetch all documents from the collection
    client.close()
    return data

def insert_data_into_mongo(email, password):
    client = MongoClient(mongo_uri)
    db = client.users
    collection = db.users
    
    # Hash the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user_data = {"email": email, "password": hashed_password}
    collection.insert_one(user_data)
    client.close()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email and password:
        insert_data_into_mongo(email, password)
        return jsonify({"message": "Signup successful!"})
    else:
        return jsonify({"error": "Email and password are required"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email and password:
        client = MongoClient(mongo_uri)
        db = client.users
        collection = db.users
        user = collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user['password'], password):
            return jsonify({"message": "Login successful!"})
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    else:
        return jsonify({"error": "Email and password are required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
