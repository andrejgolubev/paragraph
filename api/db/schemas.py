from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional


class HomeworkRequest(BaseModel):
    group_data_value: str
    date_data_value: str
    lesson_index: int
    homework: str


# class UserRegistration(BaseModel):
#     email: EmailStr 
#     password: str = Field(min_length=8, max_length=40)
   


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    role: str
    group_id: int | None = None
    group: Optional["GroupResponse"] = None

class GroupCreate(BaseModel): 
    data_value: str
    group_number: str

    model_config = ConfigDict(from_attributes=True)

class GroupResponse(BaseModel):
    id: int
    users: list["UserResponse"]| None  = None

    model_config = ConfigDict(from_attributes=True)


    date: str


class OnlyDateResponse(BaseModel): 
    id: int
    group_number: str
    data_value: str

    class Config:
        from_attributes = True
    

class GroupSelection(BaseModel):
    group_data_value: str


# users 

class UserSchema(BaseModel): 
    name: str 
    email: EmailStr
    group_id: str | None = None
    password: str 
    active: bool = True

    model_config = ConfigDict(from_attributes=True)

    # @field_validator("username")
    # def validate_name(cls, name: str):
    #     if not name.replace(' ', '').isalnum():
    #         raise HTTPException(detail="Name can only contain letters, numbers and spaces", status_code=400)
    #     if len(name) > 50: 
    #         raise HTTPException(detail='Name is too long', status_code=400)
    #     if len(name) < 3: 
    #         raise HTTPException(detail='Name is too short', status_code=400)
        
    #     return name.strip()


class TokenInfo(BaseModel): 
    access_token: str 
    token_type: str
    
