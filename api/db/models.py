from sqlalchemy.orm import mapped_column as mc, Mapped, DeclarativeBase, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
)
from api.db.database import Base
from datetime import datetime
from sqlalchemy import func

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mc(primary_key=True, index=True)
    name: Mapped[str] = mc(nullable=False)
    hashed_password: Mapped[str] = mc(nullable=False)
    role: Mapped[str] = mc(nullable=False, default="student")
    rating: Mapped[int] = mc(nullable=False, default=0)

    group_id: Mapped[int] = mc(ForeignKey("groups.id"))

    group: Mapped["Group"] = relationship(back_populates="users")



"""MANY TO MANY RELATION - GROUPS <-> parse_dates"""


class GroupDateAssociation(Base):
    __tablename__ = "group_date_association"
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "dates_id",
            name="index_unique_group_date",
        ),
    )  # благодаря UniqueConstraint все комбинации group_id и dates_id будут УНИКАЛЬНЫМИ в ассоциативной таблице

    id: Mapped[int] = mc(primary_key=True)
    group_id: Mapped[int] = mc(ForeignKey("groups.id"), nullable=False)
    dates_id: Mapped[str] = mc(ForeignKey("dates.id"), nullable=False)
    created_at: Mapped[datetime] = mc(server_default=func.now())
    homework: Mapped[str] = mc(nullable=True)


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


"""MANY TO MANY RELATION - GROUPS <-> parse_dates"""


