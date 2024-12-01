import os
import pickle
import numpy as np
from utils.jwt import gen_jwt_token
from utils.hashPassword import check_password
from flask import jsonify, request
from api.config import Config
from api.service import userService
from model.utils import cosine_distance
EMBEDDINGS_PATH = Config.EMBEDDINGS_DIR
THRESHOLD = float(Config.THRESHOLD)

def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify({'error': 'No email provided'}), 400
    if not password:
        return jsonify({'error': 'No password provided'}), 400

    user = userService.get_user_by_email(email)
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    
    if not check_password(password, user['password'].encode('utf-8')):
        return jsonify({'error': 'Invalid password'}), 400

    token = gen_jwt_token(user)
    return jsonify({
        'status': 'success',
        'user': user,
        'token': token
    }), 200

def register_face_v2():
    try:
        data = request.json
        user_id = data['userId']
        user_name = data['userName']
        user_email = data['userEmail']
        embeddings = data['faceEmbeddings']  

        embeddings_values = list(embeddings.values())  

        user = userService.get_user_by_id(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 400
        
        userService.update_label_user(f"{user_id}_{user_email}", user_id)

        file_path = os.path.join(EMBEDDINGS_PATH, f"{user_id}_{user_email}.pkl")

        with open(file_path, 'wb') as f:
            pickle.dump(embeddings_values, f)  

        return jsonify({'message': 'Embeddings saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
def verify_face():
    try:
        data = request.json
        user_id = data['userId']
        user_email = data['userEmail']
        embeddings = data['embeddings']

        file_name = f"{user_id}_{user_email}.pkl"
        file_path = os.path.join(EMBEDDINGS_PATH, file_name)
        with open(file_path, 'rb') as f:
            saved_embeddings = pickle.load(f)

        similarities = [cosine_distance(embeddings, embedding) for embedding in saved_embeddings]
        avg_similarity = (sum(similarities) / len(similarities)) if similarities else 0

        if avg_similarity >= THRESHOLD:
            user = userService.get_user_by_id(user_id)
            return jsonify({
                'verified': True,
                'user': user,
                'similarity': avg_similarity
            }), 200
        else:
            return jsonify({
                'verified': False,
                'message': 'User not recognized',
                'similarity': avg_similarity
            }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
def get_ip():
    client_ip = request.remote_addr
    print(f"Client IP: {client_ip}")
    return f"Your IP is: {client_ip}"