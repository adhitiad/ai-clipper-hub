from database import db, embedding_model, pinecone_index
from logger import logger


def process_new_comments_to_pinecone():
    logger.info("Sinkronisasi Mongo ke Pinecone...")
    unprocessed = list(db.raw_comments.find({"processed": False}))
    if not unprocessed:
        return

    try:
        for item in unprocessed:
            emb = embedding_model.encode(item["text"]).tolist()
            namespace = item["niche"].lower().replace(" ", "-").replace("&", "n")

            pinecone_index.upsert(
                vectors=[
                    {
                        "id": str(item["_id"]),
                        "values": emb,
                        "metadata": {"text": item["text"], "niche": item["niche"]},
                    }
                ],
                namespace=namespace,
            )
            db.raw_comments.update_one(
                {"_id": item["_id"]}, {"$set": {"processed": True}}
            )
        logger.info(f"{len(unprocessed)} vektor disimpan ke Pinecone.")
    except Exception as e:
        logger.error(f"Gagal sinkronisasi Pinecone: {str(e)}")
