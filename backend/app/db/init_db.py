import sys
import os

# Add the backend directory to Python path
backend_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from app.utils.database import init_database, run_migrations

def setup_database():
    """Setup database with migrations"""
    try:
        run_migrations()
        print("Database setup completed successfully!")
    except Exception as e:
        print(f"Error setting up database: {e}")
        print("Falling back to direct table creation...")
        init_database()

if __name__ == "__main__":
    setup_database()
