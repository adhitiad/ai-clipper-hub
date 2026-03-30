from langchain_groq import ChatGroq
from database import db
from logger import logger
import config

def reply_to_new_comments():
    logger.info("Engager: Memeriksa komentar baru untuk dibalas...")
    active_videos = list(db.published_clips.find().sort("timestamp", -1).limit(5))
    llm = ChatGroq(model="gpt-oss-120b", temperature=0.7, api_key=config.GROQ_API_KEY)

    for video in active_videos:
        new_comments = list(db.raw_comments.find({"niche": video["niche"], "replied": {"$ne": True}}).limit(3))
        for comment in new_comments:
            prompt = f"Buat 1 kalimat balasan santai untuk komentar ini: '{comment['text']}'. Memancing diskusi lanjutan. Bahasa gaul."
            reply_text = llm.invoke(prompt).content
            logger.info(f"Membalas: '{reply_text}'")
            db.raw_comments.update_one({"_id": comment["_id"]}, {"$set": {"replied": True, "reply_text": reply_text}})
