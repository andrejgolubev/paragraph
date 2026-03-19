from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field



class UserSchema(BaseModel): 
    name: str 
    email: EmailStr
    group_id: str | None = None
    password: str 
    active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = None
    group_number: str | None = None
    password: str | None = None


class UserRegistration(BaseModel):
    username: str
    email: EmailStr 
    password: str = Field(min_length=8, max_length=40)
    group_number: str | None = None
    accept_pd: bool = False 
    accept_terms: bool = False 
   

class UserLogin(BaseModel): 
    email: EmailStr 
    password: str


class UserResponse(BaseModel):
    email: str
    name: str 
    group_id: int | None
    role: str 
    active: bool 

    model_config = ConfigDict(from_attributes=True)


class FullUserResponse(UserResponse):
    sign_up_date: datetime 
    consents: list



class RegistredUserResponse(BaseModel):
    id: int 
    name: str 
    email: EmailStr
    role: str 
    active: bool 
    group_id: int | None = None
    detail: str 
    status: str 
    type: str
    