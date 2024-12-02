from bson.objectid import ObjectId
from flask import current_app
from api.config import Config
import datetime
from api.cart import CartEntity
from api.product import ProductEntity
from flask import jsonify, request

class OrderEntity:
    def __init__(self, user_id, products, total, date ,_id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.products = products or []
        self.total = total
        self.date = date

    def to_dictionary(self):
        return {
            "_id": str(self._id),
            "user_id": self.user_id,
            "products": self.products,
            "total": self.total,
            "date": self.date
        }
    
    def save(self, update=False):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        orders_collection = db["orders"]

        data = self.to_dictionary()
        data.pop('_id', None)  

        if update:
            orders_collection.update_one({"_id": self._id}, {"$set": data})
        else:
            orders_collection.replace_one({"_id": self._id}, data, upsert=True)
    
    @staticmethod
    def get_user_orders(user_id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        orders_collection = db["orders"]
        orders = orders_collection.find({"user_id": user_id})
        return [OrderEntity(
            user_id=order["user_id"],
            products=order["products"],
            total=order["total"],
            date=order["date"],
            _id=order["_id"]
        ).to_dictionary() for order in orders]
    
# service
def add_new_order(user_id, products, total):
    date = datetime.datetime.now()
    cart = CartEntity.get_user_cart(user_id)
    if cart:
        CartEntity.delete_cart(cart._id)
        for product in products:
            ProductEntity.update_quantity_product(product["product_id"], product["quantity"])
    else:
        return None
    order = OrderEntity(user_id, products, total, date)
    order.save()
    return order.to_dictionary()

# handler
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
    
    result = {
        'id': res['_id'],
        'user_id': res['user_id'],
        'products': res['products'],
        'total': res['total'],
        'date': res['date']
    }

    return jsonify(result), 200