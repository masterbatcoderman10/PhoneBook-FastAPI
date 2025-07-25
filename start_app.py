#!/usr/bin/env python3
"""
Startup script to handle database initialization and app startup
"""
import os
import sys
import subprocess
import time

def wait_for_db():
    """Wait for database to be ready"""
    max_retries = 30
    for i in range(max_retries):
        try:
            import psycopg2
            conn = psycopg2.connect(os.getenv("PSQL_URL"))
            conn.close()
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for database... ({i+1}/{max_retries})")
            time.sleep(2)
    return False

def run_migrations():
    """Run database migrations"""
    try:
        print("🔧 Running database migrations...")
        result = subprocess.run(["alembic", "upgrade", "head"], 
                              capture_output=True, text=True, cwd="/app")
        if result.returncode == 0:
            print("✅ Database migrations completed!")
            return True
        else:
            print(f"❌ Migration failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def start_app():
    """Start the FastAPI application"""
    print("🚀 Starting PhoneBook API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📍 API documentation at: http://localhost:8000/docs")
    
    os.execvp("uvicorn", ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

if __name__ == "__main__":
    print("🔄 PhoneBook API Startup")
    print("=" * 30)
    
    # Wait for database
    if not wait_for_db():
        print("❌ Database connection failed after 60 seconds")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Database migration failed")
        sys.exit(1)
    
    # Start the app
    start_app()