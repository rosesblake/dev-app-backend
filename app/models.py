from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True) 
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(ARRAY(String))
    bio = Column(Text)
    github_url = Column(String)
    portfolio_url = Column(String)
    stack = Column(ARRAY(String))
    created_at = Column(TIMESTAMP, server_default=func.now())

    projects = relationship("Project", back_populates="creator")
    applications = relationship("Application", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]")
    received_messages = relationship("Message", foreign_keys="[Message.receiver_id]")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True) 
    description = Column(Text, nullable=False)
    stack = Column(ARRAY(String))
    roles_needed = Column(ARRAY(String))
    commitment_level = Column(String)
    figma_url = Column(String)
    github_repo = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    creator = relationship("User", back_populates="projects")
    applications = relationship("Application", back_populates="project")
    messages = relationship("Message", back_populates="project")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")
    applied_at = Column(TIMESTAMP, server_default=func.now())

    project = relationship("Project", back_populates="applications")
    user = relationship("User", back_populates="applications")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    project = relationship("Project", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], overlaps="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], overlaps="received_messages")

class Conversation(BaseModel):
    userId: int
    userName: str
    projectId: int
    projectTitle: str
    lastMessage: str
    updatedAt: datetime
