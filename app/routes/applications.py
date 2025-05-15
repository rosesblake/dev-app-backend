from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.dependencies import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationRead)
def apply_to_project(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    application_data = schemas.ApplicationCreate(
        project_id=application.project_id,
        user_id=current_user.id,
        status=application.status
    )
    return crud.create_application(db, application_data)

@router.get("/project/{project_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_project(db, project_id)

@router.get("/user/{user_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_user(db, user_id)
