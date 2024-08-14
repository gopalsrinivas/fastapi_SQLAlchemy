from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
import datetime
import logging
import psycopg2

logger = logging.getLogger(__name__)


def get_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            return {"status_code": 200, "data": user, "msg": "User retrieved successfully"}
        else:
            return {"status_code": 404, "data": None, "msg": "User not found"}
    except Exception as e:
        logger.error(f"Error retrieving user by ID: {e}")
        return {"status_code": 500, "data": None, "msg": "Internal Server Error"}


def get_user_by_email(db: Session, email: str):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            return {"status_code": 200, "data": user, "msg": "User retrieved successfully"}
        else:
            return {"status_code": 404, "data": None, "msg": "User not found"}
    except Exception as e:
        logger.error(f"Error retrieving user by email: {e}")
        return {"status_code": 500, "data": None, "msg": "Internal Server Error"}


def get_users(db: Session, skip: int = 0, limit: int = 10):
    try:
        users = db.query(models.User).offset(skip).limit(limit).all()
        return {"status_code": 200, "data": users, "msg": "Users retrieved successfully"}
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        return {"status_code": 500, "data": None, "msg": "Internal Server Error"}


def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        user_data = {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at
        }

        return {"status_code": 201, "data": user_data, "msg": "User created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")

        if hasattr(e, 'orig') and isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {user.email} already exists."
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


def update_user(db: Session, user_id: int, user: schemas.UserBase):
    try:
        db_user = db.query(models.User).filter(
            models.User.id == user_id).first()
        if db_user:
            db_user.name = user.name
            db_user.email = user.email
            db_user.updated_at = datetime.datetime.utcnow()
            db.commit()
            db.refresh(db_user)
            return {"status_code": 200, "data": db_user, "msg": "User updated successfully"}
        else:
            return {"status_code": 404, "data": None, "msg": "User not found"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        return {"status_code": 500, "data": None, "msg": "Internal Server Error"}


def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(models.User).filter(
            models.User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return {"status_code": 200, "data": db_user, "msg": "User deleted successfully"}
        else:
            return {"status_code": 404, "data": None, "msg": "User not found"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user: {e}")
        return {"status_code": 500, "data": None, "msg": "Internal Server Error"}
