from sqlalchemy.orm import mapped_column as mc , Mapped, DeclarativeBase

class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mc(primary_key=True)
    name: Mapped[str] = mc(nullable=False)
    surname: Mapped[str] = mc(nullable=False)
    nickname: Mapped[str] = mc(nullable=True, index=True, unique=True)
    email: Mapped[str] = mc(nullable=False, unique=True)
    role: Mapped[str] = mc(nullable=False, default='student')
    is_active:Mapped[bool] = mc(default=True)
    hashed_password: Mapped[str] = mc(nullable=False)
