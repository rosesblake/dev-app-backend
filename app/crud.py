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