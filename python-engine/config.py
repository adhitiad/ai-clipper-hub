import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
VIZARDAI_API_KEY = os.getenv("VIZARDAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
