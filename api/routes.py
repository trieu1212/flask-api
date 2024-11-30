from flask import Blueprint
from api.handler.userHandler import create_user, get_current_user
from api.handler.authHandler import verify_face_login_biometrics, register_face, login, register_face_v2, verify_face
from api.middleware import jwt_middleware

auth_bp = Blueprint('auth_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

user_bp.route('/create', methods=['POST'])(create_user)
user_bp.route('/get-current-user', methods=['GET'])(jwt_middleware(get_current_user))
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/verify-face', methods=['POST'])(jwt_middleware(verify_face))
auth_bp.route('/register-face-v2', methods=['POST'])(jwt_middleware(register_face_v2))
