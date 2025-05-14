from fastapi import FastAPI
from app.routes import users
from app.models import Base
from app.db import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
