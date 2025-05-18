from fastapi import FastAPI
from app.routes import users, projects, applications, messages, auth
from app.models import Base
from app.db import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(applications.router)
app.include_router(messages.router)
app.include_router(auth.router)