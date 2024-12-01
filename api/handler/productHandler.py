from flask import jsonify, request
from api.service.productService import get_all_products, get_product_by_id, create_product

def get_all_products_handler():
    products = get_all_products()
    if not products:
        return jsonify({'error': 'No products found'}), 400
    return jsonify(products), 200

def get_product_by_id_handler():
    id = request.args.get('id')
    product = get_product_by_id(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 400
    return jsonify(product), 200

def add_new_product():
    product_data = request.json
    name = product_data.get('name')
    price = product_data.get('price')
    quantity = product_data.get('quantity')
    image = product_data.get('image')
    if not name or not price or not quantity or not image:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = create_product(product_data)
    return jsonify(new_product), 200