"""
Simple User Management REST API
A quick sample application for QA automation testing demo
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory database (for demo purposes)
users_db = {}

# Error handlers
class UserNotFoundError(Exception):
    pass

class InvalidUserDataError(Exception):
    pass


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        
        # Validation
        if not data:
            return jsonify({"error": "Request body is empty"}), 400
        
        if 'email' not in data or not data['email']:
            return jsonify({"error": "Email is required"}), 400
        
        if 'name' not in data or not data['name']:
            return jsonify({"error": "Name is required"}), 400
        
        # Email validation
        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Check if user already exists
        for user in users_db.values():
            if user['email'] == data['email']:
                return jsonify({"error": "User with this email already exists"}), 409
        
        # Create user
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": data['name'],
            "email": data['email'],
            "age": data.get('age'),
            "created_at": datetime.now().isoformat()
        }
        
        users_db[user_id] = user
        return jsonify(user), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['GET'])
def list_users():
    """Get all users"""
    try:
        users = list(users_db.values())
        return jsonify({"users": users, "count": len(users)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        if user_id not in users_db:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(users_db[user_id]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        if user_id not in users_db:
            return jsonify({"error": "User not found"}), 404
        
        data = request.json
        
        if not data:
            return jsonify({"error": "Request body is empty"}), 400
        
        user = users_db[user_id]
        
        # Update fields
        if 'name' in data:
            user['name'] = data['name']
        if 'email' in data:
            if '@' not in data['email']:
                return jsonify({"error": "Invalid email format"}), 400
            user['email'] = data['email']
        if 'age' in data:
            user['age'] = data['age']
        
        user['updated_at'] = datetime.now().isoformat()
        return jsonify(user), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        if user_id not in users_db:
            return jsonify({"error": "User not found"}), 404
        
        deleted_user = users_db.pop(user_id)
        return jsonify({"message": "User deleted", "user": deleted_user}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
