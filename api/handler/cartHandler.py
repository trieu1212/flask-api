from flask import jsonify, request
from api.service.cartService import add_product_to_cart, get_user_cart
from api.entity.productEntity import ProductEntity

def add_product_to_cart_handler():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    if not user_id or not product_id or not quantity:
        return jsonify({'error': 'Missing required fields'}), 400
    
    product = ProductEntity.find_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 400
    
    res = add_product_to_cart(user_id, product_id, quantity)
    if not res:
        return jsonify({'error': 'add to cart failed'}), 400
    
    return jsonify(res), 200

def get_current_user_cart():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    cart = get_user_cart(user_id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 400
    
    return jsonify(cart), 200