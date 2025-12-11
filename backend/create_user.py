#!/usr/bin/env python3
"""
Script to create the initial user for the Wellness Log application.
Run this script after starting the backend to set up authentication.
"""
import sys
import os

# Add the parent directory to the path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash
from getpass import getpass


def create_user():
    """Create a new user in the database."""
    db = SessionLocal()
    
    try:
        # Check if any users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("❌ Error: A user already exists in the database.")
            print("This application only supports a single user.")
            print(f"Found {existing_users} existing user(s).")
            return
        
        print("🌿 Wellness Log - Initial User Setup")
        print("=" * 50)
        print()
        
        # Get username
        while True:
            username = input("Enter username: ").strip()
            if username:
                break
            print("Username cannot be empty. Please try again.")
        
        # Get password
        while True:
            password = getpass("Enter password: ")
            if len(password) < 4:
                print("Password must be at least 4 characters. Please try again.")
                continue
            
            confirm_password = getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
            
            break
        
        # Create user
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print()
        print("=" * 50)
        print("✅ User created successfully!")
        print(f"Username: {username}")
        print(f"User ID: {new_user.id}")
        print()
        print("You can now log in to the Wellness Log application.")
        print("=" * 50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_user()

