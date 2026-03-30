from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn

from database import db, redis_client
from tasks import process_new_comments_to_pinecone
from engagement import reply_to_new_comments
from agents.supervisor import run_autonomous_workflow
from agents.evaluator import evaluate_and_evolve_persona
from logger import logger

app = FastAPI(title="AI Clipper Content Factory")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

scheduler = BackgroundScheduler()
scheduler.add_job(process_new_comments_to_pinecone, 'interval', minutes=30)
scheduler.add_job(reply_to_new_comments, 'interval', hours=1)

# Evaluator (Self-Learning)
scheduler.add_job(evaluate_and_evolve_persona, 'cron', hour='02', minute='00', args=['Gen Z'])
scheduler.add_job(evaluate_and_evolve_persona, 'cron', hour='02', minute='30', args=['Gen X'])

# Multi-Agent Executions
scheduler.add_job(run_autonomous_workflow, 'cron', hour='04', minute='30', args=['Ceramah Religi', 'Baby Boomers'])
scheduler.add_job(run_autonomous_workflow, 'cron', hour='12', minute='15', args=['Manajemen Keuangan', 'Gen X'])
scheduler.add_job(run_autonomous_workflow, 'cron', hour='19', minute='30', args=['Gosip Selebriti', 'Gen Z'])

@app.on_event("startup")
def startup_event():
    logger.info("Server AI Clipper & Supervisor Agent menyala...")
    scheduler.start()

@app.get("/api/dashboard")
def get_dashboard_data():
    active_status = redis_client.get("active_agent_status") or "Idle"
    clips = list(db.published_clips.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return {"agent_status": active_status, "total_projects": db.published_clips.count_documents({}), "recent_clips": clips}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
