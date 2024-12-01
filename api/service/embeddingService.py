from api.entity.embeddingEntity import EmbeddingEntity

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
