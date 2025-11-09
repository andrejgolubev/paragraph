# BLOCK WITH API MODELS #
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional






class UserRegistration(BaseModel):
    name: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=8, max_length=40)
    group: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    def validate_name(cls, name: str):
        if not name.replace(' ', '').isalnum():
            raise HTTPException(detail="Name can only contain letters, numbers and spaces", status_code=400)
        return name.strip()

        

class UserCreate(UserRegistration): 
    role: str = 'student'
    rating: float = Field(default=0.0, ge=0.0)



class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    role: str
    rating: float
    group_id: int | None = None
    group: Optional["GroupResponse"] = None

class GroupCreate(BaseModel): 
    data_value: str
    group_number: str


class GroupResponse(BaseModel):
    id: int
    users: list["UserResponse"]| None  = None

    model_config = ConfigDict(from_attributes=True)