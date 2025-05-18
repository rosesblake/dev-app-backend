from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[List[str]] = Field(default_factory=list)
    bio: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    stack: Optional[List[str]] = Field(default_factory=list)

class UserCreate(UserBase):
    password: str
    

class UserRead(UserBase):
    id: int
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str
    description: str
    stack: Optional[List[str]] = Field(default_factory=list)
    roles_needed: Optional[List[str]] = Field(default_factory=list)
    commitment_level: Optional[str] = None
    figma_url: Optional[HttpUrl] = None
    github_repo: Optional[HttpUrl] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectCreate):
    id: int
    slug: str
    created_at: datetime
    creator: UserRead

    class Config:
        from_attributes = True


class ApplicationBase(BaseModel):
    project_id: int
    status: Optional[str] = "pending"

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationRead(ApplicationBase):
    id: int
    user_id: int
    applied_at: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    project_id: int
    sender_id: int
    receiver_id: int
    text: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
