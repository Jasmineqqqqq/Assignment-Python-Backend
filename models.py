"""Database models for the telemedicine service.

This version includes ``__allow_unmapped__ = True`` on each model class to
instruct SQLAlchemy 2.0 to ignore type annotations for relationship
attributes.  Without this flag SQLAlchemy raises a ``TypeError`` for
``List[Appointment]`` annotations.  Alternatively you could use the new
``Mapped`` typing style; see SQLAlchemy’s migration guide.
"""

from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class UserRole(str, Enum):
    doctor = "doctor"
    patient = "patient"


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password_hash: str = Column(String, nullable=False)
    role: UserRole = Column(SAEnum(UserRole), nullable=False)

    patient_appointments: List["Appointment"] = relationship(
        "Appointment",
        back_populates="patient",
        foreign_keys="Appointment.patient_id",
    )
    doctor_appointments: List["Appointment"] = relationship(
        "Appointment",
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id!r} email={self.email!r} role={self.role!r}>"


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Appointment(Base):
    __tablename__ = "appointments"
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, index=True)
    patient_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    status: AppointmentStatus = Column(
        SAEnum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False
    )
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient: User = relationship(
        "User", back_populates="patient_appointments", foreign_keys=[patient_id]
    )
    doctor: User = relationship(
        "User", back_populates="doctor_appointments", foreign_keys=[doctor_id]
    )

    def __repr__(self) -> str:
        return f"<Appointment id={self.id!r} patient_id={self.patient_id!r} doctor_id={self.doctor_id!r}>"