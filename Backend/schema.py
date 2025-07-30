from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List, Dict, Annotated, Optional

class SignupModel(BaseModel):
    id: Optional[int]
    username: str = Field(max_length=25)
    email: EmailStr
    password: SecretStr
