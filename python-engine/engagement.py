from langchain_groq import ChatGroq
from database import db
from pymongo import UpdateOne
from pydantic import SecretStr
from logger import logger
import config


def reply_to_new_comments():
    logger.info("Engager: Memeriksa komentar baru untuk dibalas...")
    active_videos = list(db.published_clips.find().sort("timestamp", -1).limit(5))
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
        api_key=SecretStr(config.GROQ_API_KEY) if config.GROQ_API_KEY else None,
    )

    all_comments = []

    # Kumpulkan semua komentar yang perlu dibalas
    for video in active_videos:
        new_comments = list(
            db.raw_comments.find(
                {"niche": video["niche"], "replied": {"$ne": True}}
            ).limit(3)
        )
        all_comments.extend(new_comments)

    if not all_comments:
        logger.info("Tidak ada komentar baru untuk dibalas.")
        return

    # Siapkan semua prompt untuk diproses sekaligus (batch)
    prompts = [
        f"Buat 1 kalimat balasan santai untuk komentar ini: '{comment['text']}'. Memancing diskusi lanjutan. Bahasa gaul."
        for comment in all_comments
    ]

    # Eksekusi batch call ke LLM
    try:
        replies = llm.batch(prompts)
    except Exception as e:
        logger.error(f"Gagal memanggil LLM secara batch: {e}")
        return

    # Siapkan operasi update MongoDB dalam satu batch (bulk write)
    operations = []
    for comment, reply in zip(all_comments, replies):
        reply_text = reply.content
        logger.info("Membalas: '%s'", reply_text)
        operations.append(
            UpdateOne(
                {"_id": comment["_id"]},
                {"$set": {"replied": True, "reply_text": reply_text}},
            )
        )

    # Lakukan bulk write jika ada operasi
    if operations:
        db.raw_comments.bulk_write(operations)
        logger.info(f"Berhasil membalas {len(operations)} komentar sekaligus.")
