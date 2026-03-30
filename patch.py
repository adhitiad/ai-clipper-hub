with open("python-engine/main.py", "r") as f:
    content = f.read()

content = content.replace("import uvicorn\n", "import uvicorn\nfrom contextlib import asynccontextmanager\n")

content = content.replace("""app = FastAPI(title="AI Clipper Content Factory")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

scheduler = BackgroundScheduler()""", "scheduler = BackgroundScheduler()")

content = content.replace("""@app.on_event("startup")
def startup_event():
    logger.info("Server AI Clipper & Supervisor Agent menyala...")
    # --- TAMBAHKAN KODE INI UNTUK TESTING LANGSUNG ---

    # --------------------------------------------------

    scheduler.start()


@app.get("/api/dashboard")""", """@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server AI Clipper & Supervisor Agent menyala...")
    # --- TAMBAHKAN KODE INI UNTUK TESTING LANGSUNG ---

    # --------------------------------------------------

    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="AI Clipper Content Factory", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/api/dashboard")""")

with open("python-engine/main.py", "w") as f:
    f.write(content)
