from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import controller_template
from ws_daemon.app import main as ws
import asyncio
from config import Config

asyncio.create_task(ws(port=9090, listen_notify_from=Config.DbLocal))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(controller_template.router)
