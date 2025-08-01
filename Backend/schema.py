from pydantic import BaseModel, EmailStr
from typing import List, Dict, Annotated, Optional

class SignupModel(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str='B-yEwq-E3qrF1eeAT0Y2HziLK3LxhLOYBsLY1beflWY'


class LoginModel(BaseModel):
    email: EmailStr
    password: str