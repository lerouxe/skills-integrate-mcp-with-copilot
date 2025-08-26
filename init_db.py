#!/usr/bin/env python3
"""
Database initialization script for the High School Management System
Run this script to initialize or reset the database with sample data.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import our modules
src_dir = Path(__file__).parent / "src"
sys.path.append(str(src_dir))

from database import create_tables, init_sample_data, get_db

def main():
    """Initialize the database with sample data"""
    print("Initializing database...")
    
    # Create tables
    create_tables()
    print("✓ Database tables created")
    
    # Initialize sample data
    db = next(get_db())
    try:
        init_sample_data(db)
        print("✓ Sample data initialized")
        print("Database initialization complete!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
