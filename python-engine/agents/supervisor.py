from agents.analyst import get_market_insight
from agents.creative import generate_creative_brief
from tools import search_youtube_tool, send_to_vizard_tool
from database import redis_client
from logger import logger

def run_autonomous_workflow(target_niche: str, target_audience: str = "Gen Z"):
    logger.info(f"=== SUPERVISOR: Operasi '{target_niche}' ({target_audience}) ===")
    redis_client.set("active_agent_status", f"Membuat konten {target_niche} ({target_audience})...")

    try:
        insight = get_market_insight(target_niche)
        brief = generate_creative_brief(insight, target_niche, target_audience)
        logger.info(f"Hook Final: {brief}")

        video_url = search_youtube_tool.invoke(target_niche)
        if "youtube.com" in video_url:
            send_to_vizard_tool.invoke({"video_url": video_url, "project_name": brief, "niche": target_niche})

    except Exception as e:
        logger.error(f"Kegagalan sistem otonom: {str(e)}", exc_info=True)
    finally:
        redis_client.set("active_agent_status", "Idle / Menunggu Jadwal")
        logger.info("=== SUPERVISOR: Operasi Selesai ===")
