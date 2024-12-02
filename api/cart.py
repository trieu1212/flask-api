from bson.objectid import ObjectId
from flask import current_app
from api.config import Config
from api.product import ProductEntity
from flask import jsonify, request

class CartEntity:
    def __init__(self, user_id, products, total, _id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.products = products or []
        self.total = total

    def to_dictionary(self):
        return {
            "_id": str(self._id),
            "user_id": self.user_id,
            "products": self.products,
            "total": self.total,
        }
    
    def save(self, update=False):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        carts_collection = db["carts"]

        data = self.to_dictionary()
        data.pop('_id', None)  

        if update:
            carts_collection.update_one({"_id": self._id}, {"$set": data})
        else:
            carts_collection.replace_one({"_id": self._id}, data, upsert=True)

    @staticmethod
    def get_user_cart(user_id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        carts_collection = db["carts"]
        cart = carts_collection.find_one({"user_id": user_id})
        if cart:
            return CartEntity(
                user_id=cart["user_id"],
                products=cart["products"],
                total=cart["total"],
                _id=cart["_id"]
            )
        return None
    

    @staticmethod
    def add_new_product_to_cart(user_id, product_id, quantity, price):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        carts_collection = db["carts"]
        cart = carts_collection.find_one({"user_id": user_id})
        
        if cart:
            products = cart["products"]
            for item in products:
                if item["product_id"] == product_id:
                    item["quantity"] += quantity
                    cart["total"] += quantity * price
                    break
            else:
                products.append({"product_id": product_id, "quantity": quantity})
                cart["total"] += quantity * price

            carts_collection.update_one({"user_id": user_id}, {"$set": {"products": products, "total": cart["total"]}})

            updated_cart = carts_collection.find_one({"user_id": user_id})
            
            return CartEntity(
                user_id=updated_cart["user_id"],
                products=updated_cart["products"],
                total=updated_cart["total"],
                _id=updated_cart["_id"]
            )
        else:
            cart = CartEntity(
                user_id=user_id,
                products=[{"product_id": product_id, "quantity": quantity}],
                total=quantity * price
            )
            cart.save()

        return cart

    @staticmethod
    def delete_cart(_id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        carts_collection = db["carts"]
        carts_collection.delete_one({"_id": ObjectId(_id)})
        return True
    
# service
def add_product_to_cart(user_id, product_id, quantity):
    product = ProductEntity.find_by_id(product_id)
    price = product.price
    cart = CartEntity.add_new_product_to_cart(user_id, product_id, quantity, price)
    return cart.to_dictionary()


def get_user_cart(user_id):
    cart = CartEntity.get_user_cart(user_id)
    if cart:
        return cart.to_dictionary()
    return None

# handler
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
    
    result = {
        "id": cart["_id"],
        "user_id": cart["user_id"],
        "products": cart["products"],
        "total": cart["total"]
    }

    return jsonify(result), 200