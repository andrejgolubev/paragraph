from sqlalchemy.orm import mapped_column as mc , Mapped, DeclarativeBase
from sqlalchemy import ForeignKey
class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mc(primary_key=True)
    group: Mapped[str] = mc(nullable=False) 
    name: Mapped[str] = mc(nullable=False)
    role: Mapped[str] = mc(nullable=False, default='student')
    is_active: Mapped[bool] = mc(default=True)
    hashed_password: Mapped[str] = mc(nullable=False) 



class Group(Base): 
    
