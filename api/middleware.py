from functools import wraps
from flask import request, jsonify
from utils.jwt import verify_jwt_token

def jwt_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'No token provided'}), 400
        
        if request.headers['Authorization'].split(' ')[0] != 'Bearer':
            return jsonify({'error': 'Invalid token provided'}), 400
        
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        verify_jwt_token(token)

        return f(*args, **kwargs)
    return decorated_function