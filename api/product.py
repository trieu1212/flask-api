from bson.objectid import ObjectId
from flask import current_app
from api.config import Config
from flask import jsonify, request

class ProductEntity:
    def __init__(self, name, price, quantity, image, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.price = price
        self.quantity = quantity
        self.image = image

    def to_dictionary(self):
        return {
            "_id": str(self._id),
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "image": self.image,
        }
    
    def save(self, update=False):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        products_collection = db["products"]

        data = self.to_dictionary()
        data.pop('_id', None)  

        if update:
            products_collection.update_one({"_id": self._id}, {"$set": data})
        else:
            products_collection.replace_one({"_id": self._id}, data, upsert=True)

    
    @staticmethod
    def find_by_id(id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        products_collection = db["products"]

        product = products_collection.find_one({"_id": ObjectId(id)})
        if product:
            return ProductEntity(product["name"], product["price"], product["quantity"], product["image"], product["_id"])
        return None
    
    @staticmethod
    def get_all_products():
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        products_collection = db["products"]
        products = products_collection.find()
        return [ProductEntity(product["name"], product["price"], product["quantity"], product["image"], product["_id"]).to_dictionary() for product in products]
    
    @staticmethod
    def update_quantity_product(product_id, quantity):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        products_collection = db["products"]
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product["quantity"] -= quantity
            products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": product})
            return True
        return False
    
# service
def create_product(product_data):
    new_product = ProductEntity(
        name=product_data["name"],
        price=product_data["price"],
        quantity=product_data["quantity"],
        image=product_data["image"]
    )
    new_product.save()
    return {
        "id": str(new_product._id),
        "name": new_product.name,
        "price": new_product.price,
        "quantity": new_product.quantity,
        "image": new_product.image
    }

def get_product_by_id(id):
    product = ProductEntity.find_by_id(id)
    if product:
        return product.to_dictionary()
    return None

def get_all_products():
    return ProductEntity.get_all_products()

def update_product_quantity(product_id, quantity):
    return ProductEntity.update_quantity_product(product_id, quantity)

def get_product_price(product_id):
    product = ProductEntity.find_by_id(product_id)
    if product:
        return product.price
    return None

# handler
def get_all_products_handler():
    products = get_all_products()
    if not products:
        return jsonify({'error': 'No products found'}), 400
    
    products_result = []

    for product in products:
        product_result = {
            'id': product['_id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': product['quantity'],
            'image': product['image']
        }
        products_result.append(product_result)

    return jsonify(products_result), 200

def get_product_by_id_handler():
    id = request.args.get('id')
    product = get_product_by_id(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 400
    
    result = {
        'id': product['_id'],
        'name': product['name'],
        'price': product['price'],
        'quantity': product['quantity'],
        'image': product['image']
    }
    return jsonify(result), 200

def add_new_product():
    product_data = request.json
    name = product_data.get('name')
    price = product_data.get('price')
    quantity = product_data.get('quantity')
    image = product_data.get('image')

    if not name or not price or not quantity or not image:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = create_product(product_data)

    result = {
        'id': new_product['_id'],
        'name': new_product['name'],
        'price': new_product['price'],
        'quantity': new_product['quantity'],
        'image': new_product['image']
    }
    return jsonify(result), 200