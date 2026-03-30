from pymongo import MongoClient
import os
import redis
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

import config
from logger import logger

if config.HUGGINGFACE_API_KEY:
    os.environ["HF_TOKEN"] = config.HUGGINGFACE_API_KEY

mongo_client = MongoClient(config.MONGO_URI)
db = mongo_client["clipper_db"]
redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=int(config.REDIS_PORT),
    password=config.REDIS_PASSWORD,
    username=config.REDIS_USERNAME,
    decode_responses=True,
)

logger.info("Memuat Model Hugging Face...")
embedding_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

pc = Pinecone(api_key=config.PINECONE_API_KEY)
index_name = "ai-clipper-index"
if index_name not in pc.list_indexes().names():
    logger.info("Membuat Pinecone Index: %s", index_name)
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
pinecone_index = pc.Index(index_name)
