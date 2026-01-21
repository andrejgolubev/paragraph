from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict




#homework

class HomeworkRequest(BaseModel):
    group_data_value: str
    date_data_value: str
    lesson_index: int
    homework: str
    
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

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr
    group_number: str | None = None
    password: str | None = None

class UserRegistration(BaseModel):
    username: str
    email: EmailStr 
    password: str 
    group_number: str | None = None
    accept_pd: bool = False 
    accept_terms: bool = False 
   

class UserLogin(BaseModel): 
    email: EmailStr 
    password: str
    

class FullUserResponse(BaseModel):
    email: str
    name: str 
    group_id: int | None
    role: str 
    active: bool 
    sign_up_date: datetime 
    consents: list

    model_config = ConfigDict(from_attributes=True)


    
