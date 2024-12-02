from bson.objectid import ObjectId
from flask import current_app
from api.config import Config
from flask import jsonify, request
from utils.hashPassword import hash_password

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
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        users_collection = db["users"]

        data = self.to_dictionary()
        data.pop('_id', None)  

        if update:
            users_collection.update_one({"_id": self._id}, {"$set": data})
        else:
            users_collection.replace_one({"_id": self._id}, data, upsert=True)

    
    @staticmethod
    def find_by_label(label):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        users_collection = db["users"]

        user = users_collection.find_one({"label": label})
        if user:
            return UserEntity(user["firstName"], user["lastName"], user["phone"], user["password"], user["email"], user["label"], user["_id"])
        return None
    
    @staticmethod
    def find_by_id(id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        users_collection = db["users"]

        user = users_collection.find_one({"_id": ObjectId(id)})
        if user:
            return UserEntity(user["firstName"], user["lastName"], user["phone"], user["password"], user["email"], user["label"], user["_id"])
        return None
    
    @staticmethod
    def find_by_email(email):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        users_collection = db["users"]

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
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        users_collection = db["users"]

        users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"password": password}})

    @staticmethod
    def delete(id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        users_collection = db["users"]
        
        users_collection.delete_one({"_id": ObjectId(id)})


# service
def create_user(user_data):
    new_user = UserEntity(
        firstName =user_data["firstName"],
        lastName=user_data["lastName"],
        phone=user_data["phone"],
        password=user_data["password"],
        email=user_data["email"],
    )
    new_user.save()
    return {
        "id": str(new_user._id), 
        "firstName": new_user.firstName,
        "lastName": new_user.lastName,
        "email": new_user.email,
        "phone": new_user.phone
    }


def update_label_user(label, id):
    user = UserEntity.find_by_id(id)
    if user:
        user.label = label
        user.save(update=True)
        user_dict = user.to_dictionary()
        id, firstname, lastName, email, phone, label = user.to_dictionary().get("_id"), user.to_dictionary().get("firstName"), user.to_dictionary().get("lastName") ,user.to_dictionary().get("email"), user.to_dictionary().get("phone"), user.to_dictionary().get("label")
        return user_dict
    return None

def get_user_by_id(id):
    user = UserEntity.find_by_id(id)
    if user:
        return user.to_dictionary()
    return None

def get_user_by_label(label):
    user = UserEntity.find_by_label(label)
    if user:
        return user.to_dictionary()
    return None

def get_user_by_email(email):
    user = UserEntity.find_by_email(email)
    if user:
        return user.to_dictionary()
    return None

# handler

def create_user():
    data = request.json
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')

    if not firstName or not lastName or not password or not email or not phone:
        return jsonify({'error': 'Missing fields'}), 400

    user = get_user_by_email(email)
    if user:
        return jsonify({'error': 'Email already exists'}), 400  
    
    hashed_password = hash_password(password).decode('utf-8')

    user_data = {
        'firstName': firstName,
        'lastName': lastName,
        'password': hashed_password,
        'email': email,
        'phone': phone
    }

    res = create_user(user_data)
    return jsonify(res), 200

def get_current_user():
    id = request.args.get('id')
    user = get_user_by_id(id)
    if not user:
        return jsonify({'error': 'User not found'}), 400
    return jsonify(user), 200