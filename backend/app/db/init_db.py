from app.db.database import engine
from app.models import Base, User, MediaFile, Transcript

def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
