from fastapi import FastAPI
from app.routes import users, projects, applications, messages
from app.models import Base
from app.db import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(applications.router)
app.include_router(messages.router)