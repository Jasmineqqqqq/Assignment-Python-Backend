"""CRUD helper functions for interacting with the database."""

from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas, security


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    existing = get_user_by_email(db, user.email)
    if existing:
        raise ValueError("Email already registered")
    hashed_password = security.hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not security.verify_password(password, user.password_hash):
        return None
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_appointment(db: Session, appointment: schemas.AppointmentCreate) -> models.Appointment:
    db_appointment = models.Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        status=appointment.status,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointments_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Appointment]:
    return (
        db.query(models.Appointment)
        .filter((models.Appointment.patient_id == user_id) | (models.Appointment.doctor_id == user_id))
        .offset(skip)
        .limit(limit)
        .all()
    )