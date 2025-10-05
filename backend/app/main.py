import logging, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import companions, rooms, recordings, auth
from app.socket_handlers import sio
import app.config as config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="AI Companion Backend (Final)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(companions.router)
app.include_router(rooms.router)
app.include_router(recordings.router)
app.include_router(auth.router)
os.makedirs(config.RECORDINGS_DIR, exist_ok=True)
app.mount("/recordings-static", StaticFiles(directory=config.RECORDINGS_DIR), name="recordings-static")
from socketio import ASGIApp
app_asgi = ASGIApp(sio, other_asgi_app=app)
@app.on_event("startup")
async def startup_event():
    logger.info("AI Companion backend starting up...")
