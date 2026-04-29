# ============================================
# DATABASE CONNECTION
# retail-inventory-pipeline/02_pipeline/db_connection.py
# ============================================

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

def get_engine():
    """
    Creates and returns a SQLAlchemy engine using environment variables.
    """
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )
        return engine
    
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise

def test_connection():
    """Test database connection"""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()

