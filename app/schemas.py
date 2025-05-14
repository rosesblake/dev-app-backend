from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[List[str]] = []
    bio: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    stack: Optional[List[str]] = []

class UserCreate(UserBase):
    password: str
    

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
