from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import crud, schemas, models
from app.db import engine
import os

models.Base.metadata.create_all(bind=engine)

def seed():
    db: Session = SessionLocal()

    if os.getenv("ENV") != "production":
        db.query(models.Message).delete()
        db.query(models.Application).delete()
        db.query(models.Project).delete()
        db.query(models.User).delete()

        db.commit()
        
    user1 = crud.create_user(db, schemas.UserCreate(
        name="Blake Roses",
        email="blake@example.com",
        password="password123",
        role=["Full-Stack"],
        bio="I love building cool dev tools.",
        github_url="https://github.com/rosesblake",
        portfolio_url="https://blakeroses.dev",
        stack=["React", "Node.js", "PostgreSQL"]
    ))

    user2 = crud.create_user(db, schemas.UserCreate(
        name="Jess Smith",
        email="jess@example.com",
        password="password123",
        role=["Frontend"],
        stack=["Vue", "TailwindCSS"]
    ))

    crud.create_project(db, schemas.ProjectCreate(
        title="Pixel Pals",
        description="A gamified accountability app where you raise a pet by completing daily goals.",
        stack=["Flutter", "Firebase"],
        roles_needed=["Product", "Frontend"],
        commitment_level="Light",
        github_repo="https://github.com/sample/pixelpals"
    ), creator_id=user1.id)

    crud.create_project(db, schemas.ProjectCreate(
        title="DevMatch",
        description="A platform to match devs with early-stage projects.",
        stack=["Next.js", "FastAPI", "PostgreSQL"],
        roles_needed=["Backend", "Designer"],
        commitment_level="Medium",
        figma_url="https://figma.com/file/devmatch"
    ), creator_id=user2.id)

    crud.create_project(
    db,
    schemas.ProjectCreate(
        title="DevBuddy",
        description=(
            "DevBuddy is a gamified accountability platform where developers track daily goals, "
            "build momentum, and raise a virtual sidekick that evolves based on user consistency. "
            "It includes habit tracking, collaborative progress boards, and unlockable customizations. "
            "The project is designed to keep developers motivated while working on side projects or learning new skills."
        ),
        stack=[
            "Next.js", "Tailwind CSS", "TypeScript", "Zustand", "FastAPI", 
            "PostgreSQL", "Prisma", "Framer Motion", "Stripe", "tRPC"
        ],
        roles_needed=["Fullstack", "Frontend", "Backend", "UI/UX", "Product Manager"],
        commitment_level="Light",
        github_repo="https://github.com/example/devbuddy",
        figma_url="https://www.figma.com/file/devbuddy-design"
    ),
    creator_id=user2.id
)


    print("🌱 Database seeded.")

if __name__ == "__main__":
    seed()
