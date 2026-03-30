from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_core.prompts import ChatPromptTemplate
from database import redis_client
from logger import logger
import config


def generate_creative_brief(insight: str, niche: str, target_audience: str):
    """
    Menghasilkan hook kreatif berdasarkan insight pasar.
    """
    logger.info("Creative Agent: Meracik hook untuk %s...", target_audience)
    base_personas = {
        "Gen Z": "Bahasa gaul TikTok/X. Singkat, ngegas, sarkas ringan. Pakai emoji 💀🤡🔥.",
        "Gen X": "Bahasa tongkrongan bapak/ibu (mantap, info penting). Fokus realita hidup. Pakai emoji ☕👍.",
        "Baby Boomers": "Gaya broadcast WA keluarga. Sopan, HURUF KAPITAL penekanan. Sapaan 'Bunda/Bapak'. Emoji 🙏🌹.",
    }

    redis_key = f"dynamic_persona_{target_audience.replace(' ', '_')}"
    learned_persona = redis_client.get(redis_key)

    if learned_persona:
        persona_instruction = f"{base_personas.get(target_audience, '')} ATURAN TREN TERBARU: {learned_persona}"
    else:
        persona_instruction = base_personas.get(target_audience, base_personas["Gen Z"])

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.8,
        api_key=SecretStr(config.GROQ_API_KEY) if config.GROQ_API_KEY else None,
    )
    prompt = ChatPromptTemplate.from_template(
        "Kamu adalah Creative Director.\nTARGET AUDIENS: {target_audience}\nINSTRUKSI GAYA: {persona_instruction}\n\nINSIGHT NETIZEN:\n{insight}\n\nTUGAS: Buat 1 kalimat 'Hook' judul video pendek untuk niche '{niche}'. Wajib sesuai gaya bahasa target."
    )
    result = (
        (prompt | llm)
        .invoke(
            {
                "insight": insight,
                "niche": niche,
                "target_audience": target_audience,
                "persona_instruction": persona_instruction,
            }
        )
        .content
    )
    return result
