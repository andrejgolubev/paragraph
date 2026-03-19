from sqlalchemy.orm import mapped_column as mc, Mapped, relationship
from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Integer,
)
from ..db.database import Base
from datetime import UTC, datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mc(primary_key=True, index=True)
    name: Mapped[str] = mc(nullable=False)
    email: Mapped[str] = mc(nullable=False, unique=True)
    password: Mapped[str] = mc(nullable=False)
    role: Mapped[str] = mc(nullable=False, default="student")
    sign_up_date: Mapped[datetime] = mc(DateTime(timezone=True), default=datetime.now(UTC))
    active: Mapped[bool] = mc(nullable=False, default=True)

    group_id: Mapped[int] = mc(ForeignKey("groups.id"), nullable=True)

    group: Mapped["Group"] = relationship(back_populates="users")
    
    consents: Mapped[list['UserConsent']] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan",
    )

    homeworks: Mapped[list['Homework']] = relationship(
        back_populates='user', 
        cascade="all, delete-orphan" 
    )


class UserConsent(Base):
    """terms подразумевает пользовательское соглашение и политику конфиденциальности"""
    __tablename__ = "user_consents"
    
    id: Mapped[int] = mc(primary_key=True, index=True)
    user_id: Mapped[int] = mc(ForeignKey("users.id", ondelete='CASCADE'))
    consent_type: Mapped[str] = mc(String(50))  # "terms", "pd"
    accepted_at: Mapped[datetime] = mc(DateTime(timezone=True), default=datetime.now(UTC))
    ip: Mapped[str] = mc()

    user: Mapped["User"] = relationship(back_populates='consents')




class Homework(Base):
    __tablename__ = "homework"
    

    id: Mapped[int] = mc(primary_key=True)
    group_id: Mapped[int] = mc(ForeignKey("groups.id", ondelete="CASCADE"))
    dates_id: Mapped[int] = mc(ForeignKey("dates.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mc(ForeignKey("users.id", ondelete="CASCADE"))
    lesson_index: Mapped[int] = mc(nullable=True)
    homework_text: Mapped[str] = mc(nullable=True)
    is_note: Mapped[bool] = mc(default=False)
    updated: Mapped[datetime] = mc(nullable=True)

    user: Mapped["User"] = relationship(
        back_populates='homeworks'
    )
    


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mc(Integer, primary_key=True, index=True)
    group_number: Mapped[str] = mc(String(100), nullable=False, index=True)
    data_value: Mapped[str] = mc(String(50), nullable=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="group"
    )  # one to many rel with users

    dates: Mapped[list["Date"]] = relationship(
        secondary="homework", 
        back_populates="groups", 
    )


class Date(Base):
    __tablename__ = "dates"

    id: Mapped[int] = mc(primary_key=True, index=True)
    date: Mapped[str] = mc(nullable=False)
    data_value: Mapped[str] = mc()

    groups: Mapped[list["Group"]] = relationship(
        secondary="homework", 
        back_populates="dates", 
    )




