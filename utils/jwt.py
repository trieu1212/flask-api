import jwt
from datetime import datetime, timedelta
from api.user import UserEntity
from api.config import Config

SECRET_KEY = Config.SECRET_KEY

def gen_jwt_token(user: dict) -> str:
    payload = {
        'user_id': str(user['_id']),     
        'label': user['label'],
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')     
    return token


def verify_jwt_token(token: str) -> dict:
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


