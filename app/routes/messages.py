from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=schemas.MessageRead)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message)

@router.get("/project/{project_id}", response_model=list[schemas.MessageRead])
def get_project_messages(project_id: int, db: Session = Depends(get_db)):
    return crud.get_messages_for_project(db, project_id)

@router.get("/between/{user1_id}/{user2_id}", response_model=list[schemas.MessageRead])
def get_messages_between_users(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    return crud.get_messages_between_users(db, user1_id, user2_id)
