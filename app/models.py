from sqlalchemy import Column, Integer, String, Text, ARRAY, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(ARRAY(String)) 
    bio = Column(Text)
    github_url = Column(String)
    portfolio_url = Column(String)
    stack = Column(ARRAY(String)) 
    hashed_password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP, server_default=func.now())
