from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_core.prompts import ChatPromptTemplate
from database import db, redis_client
from logger import logger
import config


def evaluate_and_evolve_persona(target_audience: str = "Gen Z"):
    """
    Mengevaluasi dan memperbarui gaya bahasa berdasarkan komentar viral.
    """
    logger.info("Evaluator Agent: Evaluasi bahasa untuk %s...", target_audience)
    successful_clips = list(
        db.published_clips.find(
            {"niche": {"$regex": target_audience, "$options": "i"}}
        ).limit(5)
    )

    if not successful_clips:
        logger.info("Data belum cukup dievaluasi.")
        return

    sample_comments = list(
        db.raw_comments.find({"processed": True}).sort("timestamp", -1).limit(20)
    )
    comments_text = "\n".join([f"- {c['text']}" for c in sample_comments])

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.5,
        api_key=SecretStr(config.GROQ_API_KEY) if config.GROQ_API_KEY else None,
    )
    prompt = ChatPromptTemplate.from_template(
        "Kamu AI Linguist. Berdasarkan komentar viral ini:\n{comments}\n\nTUGAS: Ekstrak gaya/istilah gaul terbaru, tulis instruksi 'Gaya Penulisan' (maks 3 kalimat) untuk dipatuhi agen konten kami. Berikan instruksinya saja."
    )

    new_persona_rules = (prompt | llm).invoke({"comments": comments_text}).content
    redis_client.set(
        f"dynamic_persona_{target_audience.replace(' ', '_')}", str(new_persona_rules)
    )
    logger.info("Persona %s diperbarui: %s", target_audience, new_persona_rules)
