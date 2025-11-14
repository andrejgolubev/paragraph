from sqlalchemy.orm import mapped_column as mc , Mapped, DeclarativeBase, relationship
from sqlalchemy import ForeignKey , String, DateTime, Integer, Table, Column, UniqueConstraint
from db.database import Base
# from typing import TYPE_CHECKING 


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mc(primary_key=True, index=True)
    name: Mapped[str] = mc(nullable=False)
    hashed_password: Mapped[str] = mc(nullable=False) 
    role: Mapped[str] = mc(nullable=False, default='student')
    rating: Mapped[int] = mc(nullable=False, default=0)
    

    group_id: Mapped[int] = mc(ForeignKey('groups.id'))

    group: Mapped["Group"] = relationship(back_populates='users')
    homeworks: Mapped[list["Homework"]] = relationship(back_populates='user')



"""MANY TO MANY RELATION - GROUPS <-> DATES"""

group_date_association = Table( 
    'group_date_association', 
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', ForeignKey('groups.id'), nullable=False),
    Column('dates_id', ForeignKey('dates.id'), nullable=False),
    UniqueConstraint('group_id', 'dates_id', name="index_unique_group_date"), 
    # благодаря UniqueConstraint все комбинации group_id и dates_id будут УНИКАЛЬНЫМИ в ассоциативной таблице
)

class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mc(Integer, primary_key=True, index=True)
    data_value: Mapped[str] = mc(String(50), unique=True, index=True, nullable=False)
    group_number: Mapped[str] = mc(String(100), nullable=False, index=True)

    users: Mapped[list["User"]] = relationship(back_populates='group') # one to many rel with users 

    dates: Mapped[list["Date"]] = relationship(secondary=group_date_association, back_populates='groups')



class Date(Base): 
    __tablename__ = 'dates'

    id: Mapped[int] = mc(primary_key=True, index=True)  
    date: Mapped[str] = mc(nullable=False, )

    groups: Mapped[list["Group"]] = relationship(secondary=group_date_association, back_populates='dates')
    

"""MANY TO MANY RELATION - GROUPS <-> DATES"""



class Homework(Base): 
    __tablename__ = 'homeworks' 

    id: Mapped[int] = mc(Integer, primary_key=True, index=True)
    text: Mapped[str] = mc(String(150), nullable=True, default='не указано')


    user: Mapped['User'] = relationship(back_populates='homework')