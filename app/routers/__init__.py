from fastapi import FastAPI
from app.database import SessionLocal, engine
from app.models import Base  # Change this line to import Base correctly
from app.routers.user import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
