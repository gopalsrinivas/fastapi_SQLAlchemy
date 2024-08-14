from fastapi import FastAPI
from app.routers.user import router as api_router
from app.database import engine
from app.models import Base

app = FastAPI(
    title="FastAPI SQLAlchemy Example",
    description="This is a sample API with FastAPI and SQLAlchemy",
    version="1.0.0",
)

app.include_router(api_router, prefix="/users")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}
