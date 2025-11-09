from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from db.database import get_db
from db.models import User
from ..schemes import UserResponse, UserCreate, UserCreateForRoot
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import create_access_token, create_refresh_token, verify_password, hash_password
import jwt 
import settings

user_router = APIRouter()

#-------------------------------------------------------------CRUD OPERATIONS-------------------------------------------------------------
@user_router.post('/', response_model=UserResponse)
async def create_user(user_input: UserCreateForRoot, db= Depends(get_db)): 
    """
    Регистрирует нового пользователя с ролью.
    """
    user_result = await db.scalars(select(User).where(User.email == user_input.email))
    if user_result.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Введённый email уже существует.")
    
    db_user = User(
        email = user_input.email,
        hashed_password = hash_password(user_input.password),
        role = user_input.role, 
        nickname = user_input.nickname, 
        name = user_input.name, 
        surname = user_input.surname, 
    ) 
    db.add(db_user) 
    await db.commit()
    await db.refresh(db_user) 

    return UserCreate(**user_input.model_dump())



@user_router.get('/{user_email}', response_model=UserResponse)
async def get_user_by_email(user_email: str, db= Depends(get_db)): 
   
    user_search = await db.scalars(select(User).where(User.email == user_email)) 
    user = user_search.first() 
    if not user: 
        raise HTTPException(status_code=404, detail=f'User not found')
    
    return user 


@user_router.delete('/{user_email}', response_model=UserResponse)
async def delete_user_by_email(user_email: str, db= Depends(get_db)): 
   
    user_search = await db.scalars(select(User).where(User.email == user_email)) 
    user = user_search.first() 
    if not user: 
        raise HTTPException(status_code=404, detail=f'User not found')
    
    await db.delete(user)
    await db.commit()
    
    return f'Пользователь с почтой {user_email} был удалён.' 


#-------------------------------------------------------------AUTH OPERATIONS-------------------------------------------------------------


@user_router.post("/token", name='login')                                                                
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: AsyncSession = Depends(get_db)):
    """
    Аутентифицирует пользователя и возвращает access_token и refresh_token.
    create_access_token и create_refresh_token создают JWT-токены 
    с одинаковым payload (sub, role, id), но разным временем истечения (exp)
    """
    result = await db.scalars(select(User).where(User.email == form_data.username))
    user = result.first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.user_id})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role, "id": user.user_id})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



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
