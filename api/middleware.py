from functools import wraps
from flask import request, jsonify
from utils.jwt import verify_jwt_token

def jwt_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Không có Authorization'}), 400
        
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify({'error': 'jwt không hợp lệ'}), 400
        
        token = parts[1]
        if not token:
            return jsonify({'error': 'Không có token'}), 403
        
        result = verify_jwt_token(token)
        if 'error' in result:
            return jsonify(result), 401
        
        request.jwt_payload = result

        return f(*args, **kwargs)
    return decorated_function