from sqlalchemy.orm import mapped_column as mc, Mapped, relationship
from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Integer,
)
from api.db.database import Base
from datetime import UTC, datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mc(primary_key=True, index=True)
    name: Mapped[str] = mc(nullable=False)
    email: Mapped[str] = mc(nullable=False, unique=True)
    password: Mapped[str] = mc(nullable=False)
    role: Mapped[str] = mc(nullable=False, default="student")
    sign_up_date: Mapped[datetime] = mc(nullable=False, default=datetime.now())
    active: Mapped[bool] = mc(nullable=False, default=True)

    group_id: Mapped[int] = mc(ForeignKey("groups.id"), nullable=True)

    group: Mapped["Group"] = relationship(back_populates="users")
    
    consents: Mapped[list['UserConsent']] = relationship(back_populates="user", cascade="all, delete-orphan")



class UserConsent(Base):
    """terms подразумевает пользовательское соглашение и политику конфиденциальности"""
    __tablename__ = "user_consents"
    
    id: Mapped[int] = mc(primary_key=True, index=True)
    user_id: Mapped[int] = mc(ForeignKey("users.id", ondelete='CASCADE'))
    consent_type: Mapped[str] = mc(String(50))  # "terms", "pd"
    accepted_at: Mapped[datetime] = mc(DateTime(timezone=True), default=datetime.now(UTC))
    ip: Mapped[str] = mc()

    user: Mapped["User"] = relationship(back_populates='consents')









class GroupDateAssociation(Base):
    __tablename__ = "group_date_association"
    

    id: Mapped[int] = mc(primary_key=True)
    group_id: Mapped[int] = mc(ForeignKey("groups.id"), nullable=False)
    dates_id: Mapped[str] = mc(ForeignKey("dates.id"), nullable=False)
    lesson: Mapped[int] = mc(nullable=True)

    homework: Mapped[str] = mc(nullable=True)

    updated: Mapped[datetime] = mc(nullable=True)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mc(Integer, primary_key=True, index=True)
    group_number: Mapped[str] = mc(String(100), nullable=False, index=True)
    data_value: Mapped[str] = mc(String(50), nullable=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="group"
    )  # one to many rel with users

    dates: Mapped[list["Date"]] = relationship(
        secondary="group_date_association", back_populates="groups"
    )


class Date(Base):
    __tablename__ = "dates"

    id: Mapped[int] = mc(primary_key=True, index=True)
    date: Mapped[str] = mc(nullable=False)
    data_value: Mapped[str] = mc()

    groups: Mapped[list["Group"]] = relationship(
        secondary="group_date_association", back_populates="dates"
    )




