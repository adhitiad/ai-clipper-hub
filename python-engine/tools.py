import requests
from datetime import datetime
from langchain.tools import tool
import config
from database import db
from logger import logger

@tool
def search_youtube_tool(query: str) -> str:
    """Cari URL video panjang di YouTube berdasarkan kata kunci."""
    logger.info(f"Mencari video YT: '{query}'")
    search_url = "[https://www.googleapis.com/youtube/v3/search](https://www.googleapis.com/youtube/v3/search)"
    params = {
        "part": "snippet", "q": query, "type": "video",
        "videoDuration": "long", "order": "relevance",
        "maxResults": 1, "key": config.YOUTUBE_API_KEY
    }
    try:
        resp = requests.get(search_url, params=params).json()
        if "items" in resp and len(resp["items"]) > 0:
            return f"[https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=){resp['items'][0]['id']['videoId']}"
        return "Tidak ditemukan video."
    except Exception as e:
        logger.error(f"Error YT API: {str(e)}")
        return "Terjadi kesalahan."

@tool
def send_to_vizard_tool(video_url: str, project_name: str, niche: str) -> str:
    """Kirim URL video ke Vizard AI."""
    logger.info(f"Kirim ke Vizard: {video_url} | Project: {project_name}")
    create_url = "[https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/create](https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/create)"
    payload = {
        "videoUrl": video_url, "videoType": 2,
        "preferLength": [2], "projectName": project_name, "lang": "id"
    }
    headers = {"VIZARDAI_API_KEY": config.VIZARDAI_API_KEY, "Content-Type": "application/json"}

    try:
        resp = requests.post(create_url, headers=headers, json=payload).json()
        if resp.get("code") == 2000:
            db.published_clips.insert_one({
                "project_id": resp.get("projectId"),
                "niche": niche,
                "title": project_name,
                "status": "Processing in Vizard",
                "timestamp": datetime.now()
            })
            return f"Sukses! Project ID: {resp.get('projectId')}"
        return f"Gagal: {resp.get('errMsg')}"
    except Exception as e:
        logger.error(f"Error Vizard API: {str(e)}")
        return "Terjadi kesalahan koneksi."
