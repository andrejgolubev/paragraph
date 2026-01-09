from pydantic import BaseModel,  EmailStr,  ConfigDict


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr
    group_number: str | None = None
    password: str | None = None


class HomeworkRequest(BaseModel):
    group_data_value: str
    date_data_value: str
    lesson_index: int
    homework: str


class UserRegistration(BaseModel):
    username: str
    email: EmailStr 
    password: str 
    group_number: str
   


class UserLogin(BaseModel): 
    email: EmailStr 
    password: str
    

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    name: str
    role: str
    active: bool
    group_id: int | None = None

    

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
    
