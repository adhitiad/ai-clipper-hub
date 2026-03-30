import os
import uuid
import shutil
import logging
from typing import Dict, Optional
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel

try:
    from database import db, redis_client
    from tasks import process_new_comments_to_pinecone
    from engagement import reply_to_new_comments
    from agents.supervisor import run_autonomous_workflow
    from agents.evaluator import evaluate_and_evolve_persona
except ImportError:
    pass

from engine.graph import app as graph_app, VideoState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Clipper Content Factory - Backend Heavy")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

scheduler = BackgroundScheduler()
try:
    scheduler.add_job(process_new_comments_to_pinecone, "interval", minutes=30)
    scheduler.add_job(reply_to_new_comments, "interval", hours=1)

    # Evaluator (Self-Learning)
    scheduler.add_job(
        evaluate_and_evolve_persona, "cron", hour="02", minute="00", args=["Gen Z"]
    )
    scheduler.add_job(
        evaluate_and_evolve_persona, "cron", hour="02", minute="30", args=["Gen X"]
    )

    # Multi-Agent Executions
    scheduler.add_job(
        run_autonomous_workflow,
        "cron",
        hour="04",
        minute="30",
        args=["Ceramah Religi", "Baby Boomers"],
    )
    scheduler.add_job(
        run_autonomous_workflow,
        "cron",
        hour="12",
        minute="15",
        args=["Manajemen Keuangan", "Gen X"],
    )
    scheduler.add_job(
        run_autonomous_workflow,
        "cron",
        hour="19",
        minute="30",
        args=["Gosip Selebriti", "Gen Z"],
    )
except NameError:
    pass # In case imports failed during testing


@app.on_event("startup")
def startup_event():
    logger.info("Server AI Clipper & Supervisor Agent menyala...")
    try:
        scheduler.start()
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")

# Ensure directories exist
os.makedirs("inputs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# In-memory status tracker
task_status: Dict[str, str] = {}
task_results: Dict[str, Optional[str]] = {}

class PublishRequest(BaseModel):
    platform: str
    caption: str

def run_pipeline(video_id: str, input_path: str):
    logger.info(f"Starting pipeline for task {video_id}")
    task_status[video_id] = "Processing..."

    initial_state: VideoState = {
        "video_id": video_id,
        "input_path": input_path,
        "mp3_path": None,
        "transcript": None,
        "chunks": None,
        "safeguard_passed": None,
        "selected_clip": None,
        "srt_path": None,
        "cloudinary_url": None,
        "output_path": None,
        "error": None
    }

    try:
        final_state = graph_app.invoke(initial_state)

        if final_state.get("error"):
            task_status[video_id] = f"Error: {final_state['error']}"
            logger.error(f"Pipeline failed for {video_id}: {final_state['error']}")
        else:
            task_status[video_id] = "Ready"
            task_results[video_id] = final_state.get("output_path")
            logger.info(f"Pipeline completed successfully for {video_id}")

    except Exception as e:
        task_status[video_id] = f"Error: {str(e)}"
        logger.error(f"Pipeline exception for {video_id}: {e}")

@app.post("/api/process")
async def process_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only .mp4 files are supported.")

    task_id = str(uuid.uuid4())
    input_path = f"inputs/{task_id}.mp4"

    # Save file
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    task_status[task_id] = "Queued"
    background_tasks.add_task(run_pipeline, task_id, input_path)

    return {"task_id": task_id, "status": "Queued"}

@app.get("/api/status/{task_id}")
def get_status(task_id: str):
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task_status[task_id]}

@app.get("/api/videos/{video_id}/download")
def download_video(video_id: str):
    output_path = f"outputs/clip_{video_id}.mp4"
    if not os.path.exists(output_path):
        # Fallback to check if it's in results just in case path is different
        if video_id in task_results and task_results[video_id]:
            output_path = task_results[video_id]
        else:
            raise HTTPException(status_code=404, detail="Processed video not found")

    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"viral_clip_{video_id}.mp4"
    )

def simulate_publish(video_id: str, platform: str, caption: str):
    import time
    logger.info(f"Simulating publish for {video_id} to {platform}...")
    time.sleep(2) # Simulate API call delay
    logger.info(f"Successfully published {video_id} to {platform}! Caption: {caption}")

@app.post("/api/videos/{video_id}/publish")
def publish_video(video_id: str, request: PublishRequest, background_tasks: BackgroundTasks):
    output_path = f"outputs/clip_{video_id}.mp4"
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Processed video not found locally to publish")

    if request.platform not in ["tiktok", "youtube", "instagram"]:
        raise HTTPException(status_code=400, detail="Invalid platform")

    background_tasks.add_task(simulate_publish, video_id, request.platform, request.caption)
    return {"message": f"Publishing to {request.platform} initiated in background"}

@app.get("/api/dashboard")
def get_dashboard_data():
    try:
        active_status = redis_client.get("active_agent_status") or "Idle"
        clips = list(db.published_clips.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    except Exception:
        active_status = "Idle"
        clips = []

    return {
        "agent_status": active_status,
        "total_projects": len(clips),
        "recent_clips": clips,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
