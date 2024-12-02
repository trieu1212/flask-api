from flask import Blueprint
from api.user import create_user, get_current_user
from api.auth import login, register_face_v2, verify_face, get_ip
from api.product import get_all_products_handler, get_product_by_id_handler, add_new_product
from api.cart import add_product_to_cart_handler, get_current_user_cart
from api.order import add_new_order_handler
from api.middleware import jwt_middleware

auth_bp = Blueprint('auth_bp', __name__)
user_bp = Blueprint('user_bp', __name__)
product_bp = Blueprint('product_bp', __name__)
cart_bp = Blueprint('cart_bp', __name__)
order_bp = Blueprint('order_bp', __name__)

user_bp.route('/create', methods=['POST'])(create_user)
user_bp.route('/get-current-user', methods=['GET'])(jwt_middleware(get_current_user))

auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/verify-face', methods=['POST'])(jwt_middleware(verify_face))
auth_bp.route('/register-face-v2', methods=['POST'])(jwt_middleware(register_face_v2))
auth_bp.route('/get-ip', methods=['GET'])(get_ip)

product_bp.route('/get-all-products', methods=['GET'])(jwt_middleware(get_all_products_handler))
product_bp.route('/get-product-by-id', methods=['GET'])(jwt_middleware(get_product_by_id_handler))
product_bp.route('/create-product', methods=['POST'])(jwt_middleware(add_new_product))

cart_bp.route('/add-product-to-cart', methods=['POST'])(jwt_middleware(add_product_to_cart_handler))
cart_bp.route('/get-cart', methods=['GET'])(jwt_middleware(get_current_user_cart))

order_bp.route('/add-new-order', methods=['POST'])(jwt_middleware(add_new_order_handler))