from database import db, embedding_model, pinecone_index
from logger import logger


def process_new_comments_to_pinecone():
    logger.info("Sinkronisasi Mongo ke Pinecone...")
    unprocessed = list(db.raw_comments.find({"processed": False}))
    if not unprocessed:
        return

    try:
        texts = [item["text"] for item in unprocessed]
        embeddings = embedding_model.encode(texts).tolist()

        namespaces = {}
        for i, item in enumerate(unprocessed):
            namespace = item["niche"].lower().replace(" ", "-").replace("&", "n")
            if namespace not in namespaces:
                namespaces[namespace] = []

            namespaces[namespace].append({
                "id": str(item["_id"]),
                "values": embeddings[i],
                "metadata": {"text": item["text"], "niche": item["niche"]},
            })

        for namespace, vectors in namespaces.items():
            pinecone_index.upsert(vectors=vectors, namespace=namespace)

        db.raw_comments.update_many(
            {"_id": {"$in": [item["_id"] for item in unprocessed]}},
            {"$set": {"processed": True}}
        )
        logger.info(f"{len(unprocessed)} vektor disimpan ke Pinecone di {len(namespaces)} namespace.")
    except Exception as e:
        logger.error(f"Gagal sinkronisasi Pinecone: {str(e)}")
