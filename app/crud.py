from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        bio=user.bio,
        github_url=str(user.github_url) if user.github_url else None,
        portfolio_url=str(user.portfolio_url) if user.portfolio_url else None,
        stack=user.stack,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db:Session):
    return db.query(models.User).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    new_project = models.Project(
        title=project.title,
        description=project.description,
        stack=project.stack,
        roles_needed=project.roles_needed,
        commitment_level=project.commitment_level,
        figma_url=str(project.figma_url) if project.figma_url else None,
        github_repo=str(project.github_repo) if project.github_repo else None
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_projects(db:Session):
    return db.query(models.Project).all()

def create_application(db: Session, app: schemas.ApplicationCreate):
    new_app = models.Application(
        project_id=app.project_id,
        user_id=app.user_id,
        status=app.status
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def get_applications_for_project(db: Session, project_id: int):
    return db.query(models.Application).filter_by(project_id=project_id).all()

def get_applications_for_user(db: Session, user_id: int):
    return db.query(models.Application).filter_by(user_id=user_id).all()

def create_message(db: Session, msg: schemas.MessageCreate):
    new_msg = models.Message(
        project_id=msg.project_id,
        sender_id=msg.sender_id,
        receiver_id=msg.receiver_id,
        text=msg.text
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

def get_messages_for_project(db: Session, project_id: int):
    return db.query(models.Message).filter_by(project_id=project_id).all()

def get_messages_between_users(db: Session, user1_id: int, user2_id: int):
    return db.query(models.Message).filter(
        ((models.Message.sender_id == user1_id) & (models.Message.receiver_id == user2_id)) |
        ((models.Message.sender_id == user2_id) & (models.Message.receiver_id == user1_id))
    ).all()
