#!/usr/bin/env python3
"""
Migration script to rename habits to lifestyle_factors in the database.

This script will:
1. Rename tables: habits -> lifestyle_factors, habit_entries -> lifestyle_factor_entries
2. Rename columns: habit_id -> lifestyle_factor_id
"""
import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DB_PATH = "../data/wellness_log.db"


def migrate_database():
    """Rename habits tables and columns to lifestyle_factors."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("🔄 Renaming Habits to Lifestyle Factors Migration")
    print("=" * 80)
    
    try:
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'")
        if not cursor.fetchone():
            print("\n❌ 'habits' table not found. Migration may have already been applied.")
            return False
        
        print("\n📋 Current tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for table in cursor.fetchall():
            print(f"   - {table[0]}")
        
        print("\n🔧 Starting migration...")
        
        # Step 1: Rename habit_entries to lifestyle_factor_entries
        print("\n1️⃣  Renaming habit_entries table...")
        cursor.execute("ALTER TABLE habit_entries RENAME TO lifestyle_factor_entries")
        print("   ✅ Renamed habit_entries → lifestyle_factor_entries")
        
        # Step 2: Rename habits to lifestyle_factors
        print("\n2️⃣  Renaming habits table...")
        cursor.execute("ALTER TABLE habits RENAME TO lifestyle_factors")
        print("   ✅ Renamed habits → lifestyle_factors")
        
        # Step 3: The column habit_id in lifestyle_factor_entries is still named habit_id
        # SQLite doesn't support renaming columns in older versions, so we need to recreate the table
        print("\n3️⃣  Renaming habit_id column to lifestyle_factor_id...")
        
        # Get the current schema
        cursor.execute("PRAGMA table_info(lifestyle_factor_entries)")
        columns = cursor.fetchall()
        
        # Create new table with updated column name
        cursor.execute("""
            CREATE TABLE lifestyle_factor_entries_new (
                id INTEGER PRIMARY KEY,
                lifestyle_factor_id INTEGER NOT NULL,
                date DATE NOT NULL,
                completed BOOLEAN DEFAULT 0,
                notes TEXT,
                created_at DATETIME,
                FOREIGN KEY (lifestyle_factor_id) REFERENCES lifestyle_factors (id)
            )
        """)
        
        # Copy data
        cursor.execute("""
            INSERT INTO lifestyle_factor_entries_new 
            (id, lifestyle_factor_id, date, completed, notes, created_at)
            SELECT id, habit_id, date, completed, notes, created_at
            FROM lifestyle_factor_entries
        """)
        
        # Drop old table and rename new one
        cursor.execute("DROP TABLE lifestyle_factor_entries")
        cursor.execute("ALTER TABLE lifestyle_factor_entries_new RENAME TO lifestyle_factor_entries")
        
        print("   ✅ Renamed habit_id → lifestyle_factor_id")
        
        # Recreate indexes
        print("\n4️⃣  Recreating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_lifestyle_factors_id ON lifestyle_factors (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_lifestyle_factor_entries_id ON lifestyle_factor_entries (id)")
        print("   ✅ Indexes recreated")
        
        conn.commit()
        
        print("\n📊 New tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for table in cursor.fetchall():
            print(f"   - {table[0]}")
        
        print("\n✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def main():
    """Main function."""
    auto_commit = "--commit" in sys.argv
    
    print(f"\n📂 Database: {DB_PATH}\n")
    
    if auto_commit:
        print("💾 --commit flag provided, applying migration...")
        success = migrate_database()
        if success:
            print("\n" + "=" * 80)
            print("✅ Database migration complete!")
            print("   Tables renamed: habits → lifestyle_factors")
            print("   Entries renamed: habit_entries → lifestyle_factor_entries")
            print("   Columns renamed: habit_id → lifestyle_factor_id")
            print("=" * 80 + "\n")
    else:
        print("🔍 DRY RUN mode")
        print("   This migration will rename:")
        print("   - habits → lifestyle_factors")
        print("   - habit_entries → lifestyle_factor_entries")
        print("   - habit_id → lifestyle_factor_id")
        print("\n   Run with --commit to apply changes")


if __name__ == "__main__":
    main()

