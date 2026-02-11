import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

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
