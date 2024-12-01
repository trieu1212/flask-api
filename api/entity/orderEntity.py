from bson.objectid import ObjectId
from flask import current_app
from api.config import Config

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
    