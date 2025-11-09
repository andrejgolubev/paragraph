from sqlalchemy.orm import mapped_column as mc , Mapped, DeclarativeBase, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
# from typing import TYPE_CHECKING 

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mc(primary_key=True, index=True)
    name: Mapped[str] = mc(nullable=False)
    hashed_password: Mapped[str] = mc(nullable=False) 
    role: Mapped[str] = mc(nullable=False, default='student')
    rating: Mapped[float] = mc(nullable=False, default=0.0)

    group: Mapped["Group"] = relationship(back_populates='users')

    group_id: Mapped[int] = mc(ForeignKey('groups.id'))

class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data_value: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    group_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    users: Mapped[list["User"]] = relationship(back_populates='group')


class Homework(Base): 
    __tablename__ = 'homeworks' 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
