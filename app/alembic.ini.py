from fastapi import FastAPI
from app.db.session import SessionLocal, engine
from app.db import base  # Import for creating tables
from app.api.api_v1.api import api_router

app = FastAPI()

# Include your API routes
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    # Creates tables if they don't exist
    base.Base.metadata.create_all(bind=engine)
