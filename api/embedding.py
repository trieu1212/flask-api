from bson.objectid import ObjectId
from flask import current_app
from api.config import Config

class EmbeddingEntity:
    def __init__(self, user_id, user_email, embeddings, _id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.user_email = user_email
        self.embeddings = embeddings

    def to_dictionary(self):
        return {
            "_id": str(self._id),
            "user_id": self.user_id,
            "user_email": self.user_email,
            "embeddings": self.embeddings
        }
    
    def save(self, update=False):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        embeddings_collection = db["faces_embeddings"]

        data = self.to_dictionary()
        data.pop('_id', None)  

        if update:
            embeddings_collection.update_one({"_id": self._id}, {"$set": data})
        else:
            embeddings_collection.replace_one({"_id": self._id}, data, upsert=True)

    @staticmethod
    def find_by_user_id(user_id):
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        embeddings_collection = db["faces_embeddings"]

        embeddings = embeddings_collection.find_one({"user_id": user_id})
        if embeddings:
            return EmbeddingEntity(embeddings["user_id"], embeddings["user_email"], embeddings["embeddings"], embeddings["_id"])
        return None
    
    @staticmethod
    def get_all_embeddings():
        db = current_app.config['MONGO_URI'][Config.MONGO_DB_NAME]
        embeddings_collection = db["faces_embeddings"]

        embeddings = embeddings_collection.find()
        return [EmbeddingEntity(embedding["user_id"], embedding["user_email"], embedding["embeddings"], embedding["_id"]).to_dictionary() for embedding in embeddings]
    
# service
def get_embeddings(user_id):
    embedding = EmbeddingEntity.find_by_user_id(user_id)
    if embedding:
        return embedding.to_dictionary()
    return None

def get_all_embeddings():
    embeddings = EmbeddingEntity.get_all_embeddings()
    if embeddings:
        return embeddings
    return None

def save_embeddings(user_id, user_email, embeddings):
    embedding = EmbeddingEntity(
        user_id=user_id,
        user_email=user_email,
        embeddings=embeddings
    )
    embedding.save()
    return embedding.to_dictionary()

