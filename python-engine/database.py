from pymongo import MongoClient
import redis
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import config
from logger import logger

mongo_client = MongoClient(config.MONGO_URI)
db = mongo_client["clipper_db"]
redis_client = redis.Redis(host=config.REDIS_HOST, port=6379, decode_responses=True)

logger.info("Memuat Model Hugging Face...")
embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

pc = Pinecone(api_key=config.PINECONE_API_KEY)
index_name = "ai-clipper-index"
if index_name not in pc.list_indexes().names():
    logger.info(f"Membuat Pinecone Index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
pinecone_index = pc.Index(index_name)
