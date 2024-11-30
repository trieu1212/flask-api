from bson.objectid import ObjectId
from pymongo import MongoClient
from api.config import Config


users_collection = MongoClient(Config.MONGO_URI)[Config.MONGO_DB_NAME]["users"]

class UserEntity:
    def __init__(self, firstName, lastName, phone ,password, email, label = None, _id=None):
        self._id = _id or ObjectId()
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.password = password
        self.email = email
        self.label = label

    def to_dictionary(self):
         return {
            "_id": str(self._id),
            "firstName": self.firstName,
            "lastName": self.lastName,
            "phone": self.phone,
            "password": self.password,
            "email": self.email,
            "label": self.label,
        }
    
    def save(self, update=False):
        data = self.to_dictionary()
        data.pop('_id', None)  

        if update:
            users_collection.update_one({"_id": self._id}, {"$set": data})
        else:
            users_collection.replace_one({"_id": self._id}, data, upsert=True)

    
    @staticmethod
    def find_by_label(label):
        user = users_collection.find_one({"label": label})
        if user:
            return UserEntity(user["firstName"], user["lastName"], user["phone"], user["password"], user["email"], user["label"], user["_id"])
        return None
    
    @staticmethod
    def find_by_id(id):
        user = users_collection.find_one({"_id": ObjectId(id)})
        if user:
            return UserEntity(user["firstName"], user["lastName"], user["phone"], user["password"], user["email"], user["label"], user["_id"])
        return None
    
    @staticmethod
    def find_by_email(email):
        user = users_collection.find_one({"email": email})
        if not user:
            return None
        return UserEntity(
            firstName=user.get("firstName", ""),
            lastName=user.get("lastName", ""),
            phone=user.get("phone", ""),
            password=user.get("password", ""),
            email=user.get("email", ""),
            label=user.get("label", None),
            _id=user.get("_id", None)
        )
    
    @staticmethod
    def update_password(id, password):
        users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"password": password}})

    @staticmethod
    def delete(id):
        users_collection.delete_one({"_id": ObjectId(id)})

    