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
    existing = db.query(models.Application).filter(
        models.Application.project_id == application.project_id,
        models.Application.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    return crud.create_application(db, application, user_id=current_user.id)

@router.get("/project/{project_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_project(db, project_id)

@router.get("/user/{user_id}", response_model=list[schemas.ApplicationRead])
def get_applications_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_applications_for_user(db, user_id)
