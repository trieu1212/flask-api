from flask import jsonify, request
from api.service import userService
from utils.hashPassword import hash_password

def create_user():
    data = request.json
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')

    if not firstName or not lastName or not password or not email or not phone:
        return jsonify({'error': 'Missing fields'}), 400

    user = userService.get_user_by_email(email)
    print(user)
    if user:
        return jsonify({'error': 'Email already exists'}), 400  
    
    hashed_password = hash_password(password).decode('utf-8')

    user_data = {
        'firstName': firstName,
        'lastName': lastName,
        'password': hashed_password,
        'email': email,
        'phone': phone
    }

    res = userService.create_user(user_data)
    return jsonify(res), 200

def get_current_user():
    id = request.args.get('id')
    user = userService.get_user_by_id(id)
    if not user:
        return jsonify({'error': 'User not found'}), 400
    return jsonify(user), 200