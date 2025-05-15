from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app import schemas, crud, models, auth
from app.dependencies import get_db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.ProjectRead)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_project = crud.create_project(
        db=db,
        project=project,
        creator_id=current_user.id
    )
    return new_project

@router.get("/", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).options(joinedload(models.Project.creator)).all()
