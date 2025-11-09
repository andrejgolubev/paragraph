from fastapi import Depends, HTTPException, status, APIRouter
from db.database import get_db
from db.models import User, Group
from db.schemes import UserCreate, UserResponse
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import create_access_token, create_refresh_token, verify_password, hash_password
import jwt 
import bcrypt

user_router = APIRouter() # prefix в main.py


@user_router.post('/register/', response_model=UserResponse)
async def register(user:UserCreate, db: AsyncSession = Depends(get_db)): 

    """для регистрации пользователя саморучно. использует UserResponse, наследующую от UserCreate.
    не имеет функц. задавать role, rating."""

    result = await db.execute(select(User).where(User.name == user.name))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже есть в БД"
        )

    # Если указан group_id, проверяем что группа существует
    if user.group_id:
        result = await db.execute(select(Group).where(Group.id == user.group_id))
        existing_group = result.scalar_one_or_none()
        if not existing_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Группа не найдена"
            )

    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user) 

    return db_user



#-------------------------------------------------------------AUTH OPERATIONS-------------------------------------------------------------


# @user_router.post("/token", name='login')                                                                
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
#                 db: AsyncSession = Depends(get_db)):
#     """
#     Аутентифицирует пользователя и возвращает access_token и refresh_token.
#     create_access_token и create_refresh_token создают JWT-токены 
#     с одинаковым payload (sub, role, id), но разным временем истечения (exp)
#     """
#     result = await db.scalars(select(User).where(User.email == form_data.username))
#     user = result.first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.user_id})
#     refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role, "id": user.user_id})
    
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



# @user_router.post("/refresh-token")
# async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
#     """
#     Обновляет access_token с помощью refresh_token.
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate refresh token",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # type: ignore
#         # Автоматически проверяется exp! Если токен просрочен, здесь выбросится исключение.
#         email: str = payload.get("sub")
#         if not email: 
#             raise credentials_exception
#     except jwt.exceptions:
#         raise credentials_exception
#     result = await db.scalars(select(User).where(User.email == email, User.is_active == True))
#     user = result.first()
#     if not user:
#         raise credentials_exception
#     access_token = create_access_token(data={
#         "sub": user.email,
#         "role": user.role,
#         "id": user.user_id,
#     })
#     return {"access_token": access_token, "token_type": "bearer"}
