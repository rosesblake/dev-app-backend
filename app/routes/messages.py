from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.auth import get_current_user
from app.dependencies import get_db

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=schemas.MessageRead)
def send_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message_data = schemas.MessageCreate(
        project_id=message.project_id,
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        text=message.text
    )
    return crud.create_message(db, message_data)

@router.get("/project/{project_id}", response_model=list[schemas.MessageRead])
def get_project_messages(project_id: int, db: Session = Depends(get_db)):
    return crud.get_messages_for_project(db, project_id)

@router.get("/between/{user1_id}/{user2_id}", response_model=list[schemas.MessageRead])
def get_messages_between_users(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    return crud.get_messages_between_users(db, user1_id, user2_id)
