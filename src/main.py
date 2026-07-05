from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from .routes import base

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI()
app.include_router(base.base_router)
