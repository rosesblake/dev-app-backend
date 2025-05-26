from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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
    existing = db.query(models.Application).filter(
        models.Application.project_id == application.project_id,
        models.Application.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    return crud.create_application(db, application, user_id=current_user.id)

@router.post("/update/{application_id}", response_model=schemas.ApplicationRead)
def update_application_status(
    application_id: int,
    status_update: schemas.StatusUpdate,
    db: Session = Depends(get_db)
):
    application = crud.update_application_status(db, application_id, status_update.status)
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application


@router.get("/project/{project_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_project(db, project_id)

@router.get("/user/{user_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_user(db, user_id)

@router.get("/received/{user_id}", response_model=List[schemas.ApplicationRead])
def get_applications_to_users_projects(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Application)
        .join(models.Project)
        .filter(models.Project.creator_id == user_id)
        .all()
    )

