import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np

cred = credentials.Certificate("embeddings/credentials.json")
firebase_admin.initialize_app(cred)

firestoreDB = firestore.client()


def save_embeddings(user_id, email, embeddings):
    doc_ref = firestoreDB.collection("face_embeddings").document(user_id)
    doc_ref.set({
        "user_id": user_id,
        "email": email,
        "embeddings": embeddings
    })

    print("Embeddings saved successfully!")

def get_embeddings(user_id):
    doc_ref = firestoreDB.collection("face_embeddings").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_all_embeddings():
    docs = firestoreDB.collection("face_embeddings").stream()
    embeddings = []
    for doc in docs:
        embeddings.append(doc.to_dict())
    return embeddings

