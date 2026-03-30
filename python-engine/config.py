import os
from dotenv import load_dotenv

load_dotenv()

# GROQ
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# PINECONE
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# YOUTUBE
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# VIZARDAI
VIZARDAI_API_KEY = os.getenv("VIZARDAI_API_KEY")

# MONGO
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_USERNAME = os.getenv("REDIS_USERNAME", "default")

# HF
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
