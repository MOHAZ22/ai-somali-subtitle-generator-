import os
from alembic import command
from alembic.config import Config
from app.db.database import engine
from app.models import Base

def init_database():
    """Initialize database with all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def run_migrations():
    """Run alembic migrations"""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("Database migrations applied successfully!")

def reset_database():
    """Reset database (WARNING: This will drop all tables)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")
