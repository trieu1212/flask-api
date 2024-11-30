# import os
# import cv2
# import pickle
# import numpy as np
# import traceback

# from flask import jsonify
# from deepface import DeepFace
# from sklearn.metrics.pairwise import cosine_similarity
# from config import Config
# from model.face_recognize import normalize_embedding

# DATA_DIR = '/home/trieu/project/bio-python/data/faces'
# EMBEDDINGS_PATH = Config.EMBEDDINGS_DIR
# THRESHOLD = float(Config.THRESHOLD)

# def login_face_biometric(image):
#     image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
#     if image is None:
#         return None, 0

#     try:
#         embedding_obj = DeepFace.represent(image, model_name="Facenet", enforce_detection=False)
#         if not embedding_obj:
#             print("No face detected")
#             return None, 0
#         embedding = embedding_obj[0]["embedding"]
#         if isinstance(embedding, dict):
#             print(f"Invalid format in embedding: {embedding}")
#             return None, 0
#         embedding = normalize_embedding(np.array(embedding, dtype=float))
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         traceback.print_exc()
#         return None, 0

#     best_match = None
#     highest_similarity = 0

#     for filename in os.listdir(EMBEDDINGS_PATH):
#         if filename.endswith(".pkl"):
#             file_path = os.path.join(EMBEDDINGS_PATH, filename)
#             try:
#                 with open(file_path, 'rb') as f:
#                     known_embeddings = pickle.load(f)

#                 for known_embedding in known_embeddings:
#                     if isinstance(known_embedding, dict):
#                         print(f"Invalid format in {filename}, skipping this embedding: {known_embedding}")
#                         continue

#                     known_embedding = normalize_embedding(np.array(known_embedding, dtype=float))
#                     similarity = float(cosine_similarity([embedding], [known_embedding])[0][0])
#                     if similarity > highest_similarity:
#                         highest_similarity = similarity
#                         best_match = filename[:-4] 

#             except Exception as e:
#                 print(f"Error loading or comparing embeddings from {filename}: {e}")
#                 traceback.print_exc()
#                 continue  

#     print(f"Best match: {best_match}, similarity: {highest_similarity}")

#     if highest_similarity >= THRESHOLD:
#         return best_match, highest_similarity
#     else:
#         return None, 0