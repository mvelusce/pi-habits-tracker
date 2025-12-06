from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Habit, HabitEntry, MoodEntry
from datetime import datetime
import csv
import io

router = APIRouter()


@router.get("/habits/export")
async def export_habits(db: Session = Depends(get_db)):
    """Export all habits to CSV."""
    habits = db.query(Habit).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['id', 'name', 'description', 'color', 'icon', 'is_active', 'created_at'])
    
    # Write data
    for habit in habits:
        writer.writerow([
            habit.id,
            habit.name,
            habit.description or '',
            habit.color,
            habit.icon or '',
            habit.is_active,
            habit.created_at.isoformat()
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=habits_export.csv"}
    )


@router.get("/habits/entries/export")
async def export_habit_entries(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Export habit entries to CSV."""
    query = db.query(HabitEntry)
    
    if start_date:
        query = query.filter(HabitEntry.date >= start_date)
    if end_date:
        query = query.filter(HabitEntry.date <= end_date)
    
    entries = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['id', 'habit_id', 'habit_name', 'date', 'completed', 'notes', 'created_at'])
    
    # Write data
    for entry in entries:
        habit = db.query(Habit).filter(Habit.id == entry.habit_id).first()
        writer.writerow([
            entry.id,
            entry.habit_id,
            habit.name if habit else '',
            entry.date.isoformat(),
            entry.completed,
            entry.notes or '',
            entry.created_at.isoformat()
        ])
    
    output.seek(0)
    filename = f"habit_entries_export_{datetime.now().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/mood/export")
async def export_mood_entries(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Export mood entries to CSV."""
    query = db.query(MoodEntry)
    
    if start_date:
        query = query.filter(MoodEntry.date >= start_date)
    if end_date:
        query = query.filter(MoodEntry.date <= end_date)
    
    entries = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'id', 'date', 'time', 'mood_score', 'energy_level', 
        'stress_level', 'notes', 'tags', 'created_at'
    ])
    
    # Write data
    for entry in entries:
        writer.writerow([
            entry.id,
            entry.date.isoformat(),
            entry.time.isoformat() if entry.time else '',
            entry.mood_score,
            entry.energy_level or '',
            entry.stress_level or '',
            entry.notes or '',
            entry.tags or '',
            entry.created_at.isoformat()
        ])
    
    output.seek(0)
    filename = f"mood_export_{datetime.now().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/all")
async def export_all_data(db: Session = Depends(get_db)):
    """Export all data (habits, entries, mood) to a single CSV with multiple sheets concept."""
    # For simplicity, we'll create a ZIP file with multiple CSVs
    import zipfile
    from io import BytesIO
    
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Export habits
        habits = db.query(Habit).all()
        habits_csv = io.StringIO()
        writer = csv.writer(habits_csv)
        writer.writerow(['id', 'name', 'description', 'color', 'icon', 'is_active', 'created_at'])
        for habit in habits:
            writer.writerow([
                habit.id, habit.name, habit.description or '', habit.color,
                habit.icon or '', habit.is_active, habit.created_at.isoformat()
            ])
        zip_file.writestr('habits.csv', habits_csv.getvalue())
        
        # Export habit entries
        entries = db.query(HabitEntry).all()
        entries_csv = io.StringIO()
        writer = csv.writer(entries_csv)
        writer.writerow(['id', 'habit_id', 'habit_name', 'date', 'completed', 'notes', 'created_at'])
        for entry in entries:
            habit = db.query(Habit).filter(Habit.id == entry.habit_id).first()
            writer.writerow([
                entry.id, entry.habit_id, habit.name if habit else '',
                entry.date.isoformat(), entry.completed, entry.notes or '',
                entry.created_at.isoformat()
            ])
        zip_file.writestr('habit_entries.csv', entries_csv.getvalue())
        
        # Export mood entries
        mood_entries = db.query(MoodEntry).all()
        mood_csv = io.StringIO()
        writer = csv.writer(mood_csv)
        writer.writerow(['id', 'date', 'time', 'mood_score', 'energy_level', 'stress_level', 'notes', 'tags', 'created_at'])
        for entry in mood_entries:
            writer.writerow([
                entry.id, entry.date.isoformat(), entry.time.isoformat() if entry.time else '',
                entry.mood_score, entry.energy_level or '', entry.stress_level or '',
                entry.notes or '', entry.tags or '', entry.created_at.isoformat()
            ])
        zip_file.writestr('mood_entries.csv', mood_csv.getvalue())
    
    zip_buffer.seek(0)
    filename = f"habits_tracker_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return StreamingResponse(
        iter([zip_buffer.getvalue()]),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

