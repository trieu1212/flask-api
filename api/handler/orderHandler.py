from flask import jsonify, request
from api.service.orderService import add_new_order

def add_new_order_handler():
    data = request.json
    user_id = data.get('user_id')
    products = data.get('products')
    total = data.get('total')
    if not user_id or not products or not total:
        return jsonify({'error': 'Missing required fields'}), 400
    
    res = add_new_order(user_id, products, total)
    if not res:
        return jsonify({'error': 'add new order failed'}), 400
    return jsonify(res), 200