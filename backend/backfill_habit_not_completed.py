#!/usr/bin/env python3
"""
Backfill habit entries with completed=False for days when a habit was NOT completed.

This is necessary for correlation calculations, which require variation in both variables.
Without this, all habit entries show completed=True, resulting in constant input arrays
that can't be correlated.

This script:
1. For each active habit, find all dates between the habit's creation and today
2. For each date, if there's no HabitEntry, create one with completed=False
"""

import argparse
import sys
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming models and database setup are in app/
sys.path.insert(0, './backend')
from app.database import Base
from app.models import Habit, HabitEntry

def backfill_habit_entries(db_path: str, auto_confirm: bool = False):
    """Backfill habit entries with completed=False for missing dates."""
    
    print(f"🔧 Backfilling habit entries in database: {db_path}")
    print()
    
    # Create database connection
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get all active habits
        habits = db.query(Habit).filter(Habit.is_active == True).all()
        
        if not habits:
            print("❌ No active habits found!")
            return
        
        print(f"Found {len(habits)} active habits to process")
        print()
        
        if not auto_confirm:
            response = input("Do you want to continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Aborted by user")
                return
        
        total_added = 0
        today = date.today()
        
        # Find the earliest date across all habit entries to determine backfill range
        earliest_entry = db.query(HabitEntry).order_by(HabitEntry.date).first()
        global_start_date = earliest_entry.date if earliest_entry else today
        
        print(f"ℹ️  Will backfill from {global_start_date} to {today}")
        print()
        
        for habit in habits:
            print(f"📋 Processing habit: {habit.name}")
            
            # Get existing habit entries for this habit
            existing_entries = db.query(HabitEntry).filter(
                HabitEntry.habit_id == habit.id
            ).all()
            
            # Create a set of dates that already have entries
            existing_dates = {entry.date for entry in existing_entries}
            
            # Use the global start date (earliest date in any habit data)
            start_date = global_start_date
            
            # Generate all dates from global start to today
            current_date = start_date
            added_for_habit = 0
            
            while current_date <= today:
                if current_date not in existing_dates:
                    # Create a new entry with completed=False
                    new_entry = HabitEntry(
                        habit_id=habit.id,
                        date=current_date,
                        completed=False,
                        notes=None
                    )
                    db.add(new_entry)
                    added_for_habit += 1
                
                current_date += timedelta(days=1)
            
            print(f"  ✅ Added {added_for_habit} not-completed entries")
            total_added += added_for_habit
        
        # Commit all changes
        db.commit()
        print()
        print(f"✅ Successfully backfilled {total_added} habit entries!")
        print()
        
        # Verification
        print("📊 Verification:")
        for habit in habits:
            total_entries = db.query(HabitEntry).filter(HabitEntry.habit_id == habit.id).count()
            completed_entries = db.query(HabitEntry).filter(
                HabitEntry.habit_id == habit.id,
                HabitEntry.completed == True
            ).count()
            not_completed_entries = total_entries - completed_entries
            
            print(f"  {habit.name}: {total_entries} total entries ({completed_entries} completed, {not_completed_entries} not completed)")
        
    except Exception as e:
        print(f"❌ Error during backfill: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill habit entries with completed=False")
    parser.add_argument("db_path", help="Path to SQLite database file")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-confirm (non-interactive)")
    
    args = parser.parse_args()
    
    backfill_habit_entries(args.db_path, auto_confirm=args.yes)

