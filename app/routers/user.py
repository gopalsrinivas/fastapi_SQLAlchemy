from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    result = crud.get_users(db, skip=skip, limit=limit)
    if result["status_code"] != 200:
        raise HTTPException(
            status_code=result["status_code"], detail=result["msg"])
    return result["data"]


@router.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    result = crud.get_user_by_email(db, email=email)
    if result["status_code"] != 200:
        raise HTTPException(
            status_code=result["status_code"], detail=result["msg"])
    return result["data"]


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    result = crud.create_user(db, user=user)
    if result["status_code"] != 201:
        raise HTTPException(
            status_code=result["status_code"], detail=result["msg"])
    return result["data"]


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    result = crud.update_user(db, user_id=user_id, user=user)
    if result["status_code"] != 200:
        raise HTTPException(
            status_code=result["status_code"], detail=result["msg"])
    return result["data"]


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = crud.delete_user(db, user_id=user_id)
    if result["status_code"] != 200:
        raise HTTPException(
            status_code=result["status_code"], detail=result["msg"])
    return result["data"]
