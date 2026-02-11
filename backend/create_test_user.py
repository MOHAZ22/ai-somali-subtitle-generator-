from app.db.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

db = SessionLocal()

# Create a simple test user
test_user = User(
    username="testuser",
    email="test@example.com", 
    hashed_password=get_password_hash("test123")
)

db.add(test_user)
db.commit()
print(f"Created user: {test_user.username} with ID: {test_user.id}")
db.close()
