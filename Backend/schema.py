from pydantic import BaseModel, EmailStr
from typing import List, Dict, Annotated, Optional

class SignupModel(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str='B-yEwq-E3qrF1eeAT0Y2HziLK3LxhLOYBsLY1beflWY'
    GOOGLE_CLIENT_ID: str="673108057012-9af5h1g83q2nj09ll2mvhuppn9dlbptt.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET: str="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"

    class Config:
        env_file = ".env"


class LoginModel(BaseModel):
    email: EmailStr
    password: str
