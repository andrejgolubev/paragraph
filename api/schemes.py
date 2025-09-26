# BLOCK WITH API MODELS #
import re
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator



class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class UserResponse(TunedModel):
    name: str
    surname: str
    nickname: str | None
    email: EmailStr


class UserFullResponse(TunedModel):
    user_id: int
    name: str
    surname: str
    nickname: str | None
    email: EmailStr
    is_active: bool



class UserCreate(BaseModel):
    name: str
    surname: str
    nickname: str | None
    email: EmailStr
    password: str 


    @field_validator("name")
    def validate_name(cls, name: str):
        if not name.isalpha():
            raise HTTPException(
                status_code=403, detail="Имя должно содержать только буквы."
            )
        if len(name) > 11: 
            raise HTTPException(
                status_code=403, detail=f"Имя не может содержать {len(name)} символов."
            )
        return name
    
    @field_validator("surname")
    def validate_surname(cls, surname: str):
        if not surname.isalpha():
            raise HTTPException(
                status_code=403, detail="Фамилия должна содержать только буквы."
            )
        if len(surname) > 15: 
            raise HTTPException(
                status_code=403, detail=f"Фамилия не может содержать {len(surname)} символов."
            )
        return surname
    
    @field_validator("surname")
    def validate_nickname(cls, nickname):
        if nickname:
            # pattern = re.compile(r'^[a-zA-Z1-9_]+$')
            # if not pattern.match(nickname):
            #     raise HTTPException(
            #         status_code=403, detail="Никнэйм может содержать латинницу, цифры и символы нижнего подчеркивания."
            #     )
            if len(nickname) > 32: 
                raise HTTPException(
                    status_code=403, detail=f"Никнэйм не может содержать {len(nickname)} символов!"
                )
            return nickname
        
    @field_validator("surname")
    def validate_password(cls, pwd):
        # if len(pwd) < 11: 
        #     raise HTTPException(status_code=403, detail='Введён слишком короткий пароль.')
        # pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$')
        # if not pattern.match(pwd):
        #     raise HTTPException(
        #         status_code=403, detail="Введён слишком простой пароль."
        #     )
        if len(pwd) > 64: 
            raise HTTPException(
                status_code=403, detail=f"Пароль не может содержать {len(pwd)} символов!"
            )
        return pwd
        
class UserCreateForRoot(UserCreate): 
    role: str