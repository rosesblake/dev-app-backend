from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationRead)
def apply_to_project(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, application)

@router.get("/project/{project_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_project(db, project_id)

@router.get("/user/{user_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_user(db, user_id)
