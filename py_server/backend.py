
from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for development purposes

# Retrieve MongoDB connection string and database name from environment variables
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME", "ML")  # Default to "ML" if not set
collection_name = os.getenv("COLLECTION_NAME", "RATNA_SUPERMARKET")  # Default to "RATNA_SUPERMARKET" if not set

# Check if the variables are loaded correctly
if not mongo_uri:
    raise ValueError("Missing environment variable 'MONGO_URI'. Please check your .env file.")

try:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    print("MongoDB connected successfully")
except errors.ConfigurationError as e:  # Change to ConfigurationError
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Ratna Supermarket API!'})

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Returns a 204 No Content response

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    login_data = {'username': username, 'password': password}
    
    try:
        result = collection.insert_one(login_data)
        response = {'message': 'Login data saved successfully!', 'inserted_id': str(result.inserted_id)}
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/trail', methods=['GET'])
def trail():
    return "Hello World!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    login_data = collection.find_one({'username': username, 'password': password})

    if login_data:
        response = {'message': 'Login successful!'}
    else:
        response = {'message': 'Invalid login credentials!'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5000)), debug=True)
