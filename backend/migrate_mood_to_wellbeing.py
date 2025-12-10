#!/usr/bin/env python3
"""
Migration script to rename mood to wellbeing_metrics in the database.

This script will:
1. Rename table: mood_entries -> wellbeing_metric_entries
"""
import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DB_PATH = "../data/wellness_log.db"


def migrate_database():
    """Rename mood table to wellbeing_metric_entries."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("🔄 Renaming Mood to Well-Being Metrics Migration")
    print("=" * 80)
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mood_entries'")
        if not cursor.fetchone():
            print("\n❌ 'mood_entries' table not found. Migration may have already been applied.")
            return False
        
        print("\n📋 Current tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for table in cursor.fetchall():
            print(f"   - {table[0]}")
        
        print("\n🔧 Starting migration...")
        
        # Rename mood_entries to wellbeing_metric_entries
        print("\n1️⃣  Renaming mood_entries table...")
        cursor.execute("ALTER TABLE mood_entries RENAME TO wellbeing_metric_entries")
        print("   ✅ Renamed mood_entries → wellbeing_metric_entries")
        
        # Recreate indexes
        print("\n2️⃣  Recreating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_wellbeing_metric_entries_id ON wellbeing_metric_entries (id)")
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
            print("   Tables renamed: mood_entries → wellbeing_metric_entries")
            print("=" * 80 + "\n")
    else:
        print("🔍 DRY RUN mode")
        print("   This migration will rename:")
        print("   - mood_entries → wellbeing_metric_entries")
        print("\n   Run with --commit to apply changes")


if __name__ == "__main__":
    main()

