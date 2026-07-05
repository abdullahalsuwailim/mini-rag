from pathlib import Path
from fastapi import FastAPI
from .routes import base


app = FastAPI()
app.include_router(base.base_router)
