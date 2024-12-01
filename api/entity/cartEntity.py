from bson.objectid import ObjectId
from flask import current_app
from api.config import Config

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