from bson.objectid import ObjectId
from flask import current_app
from api.config import Config

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
    