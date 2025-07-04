from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from app.auth import verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def hash_password(password: str):
    return pwd_context.hash(password)

def generate_unique_slug(db: Session, title: str, model) -> str:
    base_slug = (
        title.lower()
        .strip()
        .replace(" ", "-")
        .replace("_", "-")
    )

    slug = base_slug
    count = 1

    while db.query(model).filter_by(slug=slug).first():
        slug = f"{base_slug}-{count}"
        count += 1

    return slug


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    slug = generate_unique_slug(db, user.name, models.User)
    new_user = models.User(
        name=user.name,
        slug=slug,
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

def create_project(db: Session, project: schemas.ProjectCreate, creator_id: int):
    slug = generate_unique_slug(db, project.title, models.Project)
    
    new_project = models.Project(
        title=project.title,
        slug=slug,
        description=project.description,
        stack=project.stack,
        roles_needed=project.roles_needed,
        commitment_level=project.commitment_level,
        figma_url=str(project.figma_url) if project.figma_url else None,
        github_repo=str(project.github_repo) if project.github_repo else None,
        creator_id=creator_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_projects(db:Session):
    return db.query(models.Project).all()

def create_application(db: Session, app: schemas.ApplicationCreate, user_id: int):
    new_app = models.Application(
        project_id=app.project_id,
        user_id=user_id, 
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

def update_application_status(db: Session, application_id: int, new_status: str):
    application = db.query(models.Application).filter_by(id=application_id).first()

    if not application:
        return None

    application.status = new_status
    db.commit()
    db.refresh(application)
    return application

def create_message(db: Session, sender_id: int, msg: schemas.MessageCreate):
    new_msg = models.Message(
        project_id=msg.project_id,
        sender_id=sender_id,
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

def get_applications_to_users_projects(db: Session, user_id: int):
    return (
        db.query(models.Application)
        .join(models.Project, models.Application.project_id == models.Project.id)
        .filter(models.Project.creator_id == user_id)
        .all()
    )

def get_conversations(db: Session, user_id: int):
    messages = db.query(models.Message).filter(
        (models.Message.sender_id == user_id) | (models.Message.receiver_id == user_id)
    ).order_by(models.Message.created_at.desc()).all()

    seen = set()
    conversations = []

    for msg in messages:
        other_user = msg.receiver if msg.sender_id == user_id else msg.sender
        key = (other_user.id, msg.project_id)

        if key not in seen:
            seen.add(key)
            conversations.append({
                "userId": other_user.id,
                "userName": other_user.name,
                "projectId": msg.project.id,
                "projectTitle": msg.project.title,
                "lastMessage": msg.text,
                "updatedAt": msg.created_at,
            })

    return conversations
