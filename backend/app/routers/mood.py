from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.MoodEntry)
def create_mood_entry(entry: schemas.MoodEntryCreate, db: Session = Depends(get_db)):
    """Create a new mood entry"""
    db_entry = models.MoodEntry(
        **entry.model_dump(),
        time=datetime.utcnow()
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/", response_model=List[schemas.MoodEntry])
def get_mood_entries(
    start_date: date = None,
    end_date: date = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get mood entries with optional date filtering"""
    query = db.query(models.MoodEntry)
    
    if start_date:
        query = query.filter(models.MoodEntry.date >= start_date)
    if end_date:
        query = query.filter(models.MoodEntry.date <= end_date)
    
    return query.order_by(models.MoodEntry.date.desc()).limit(limit).all()

@router.get("/{entry_id}", response_model=schemas.MoodEntry)
def get_mood_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get a specific mood entry"""
    entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return entry

@router.get("/date/{entry_date}", response_model=List[schemas.MoodEntry])
def get_mood_entries_by_date(entry_date: date, db: Session = Depends(get_db)):
    """Get all mood entries for a specific date"""
    return db.query(models.MoodEntry).filter(
        models.MoodEntry.date == entry_date
    ).order_by(models.MoodEntry.time).all()

@router.put("/{entry_id}", response_model=schemas.MoodEntry)
def update_mood_entry(
    entry_id: int,
    entry_update: schemas.MoodEntryUpdate,
    db: Session = Depends(get_db)
):
    """Update a mood entry"""
    db_entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    
    update_data = entry_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_entry, key, value)
    
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_mood_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete a mood entry"""
    db_entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    
    db.delete(db_entry)
    db.commit()
    return {"message": "Mood entry deleted successfully"}

@router.get("/stats/summary", response_model=schemas.MoodStats)
def get_mood_stats(
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """Get mood statistics for a date range"""
    query = db.query(models.MoodEntry)
    
    if start_date:
        query = query.filter(models.MoodEntry.date >= start_date)
    if end_date:
        query = query.filter(models.MoodEntry.date <= end_date)
    
    entries = query.all()
    
    if not entries:
        return schemas.MoodStats(
            average_mood=0.0,
            average_energy=None,
            average_stress=None,
            average_anxiety=None,
            average_rumination=None,
            average_anger=None,
            average_general_health=None,
            average_sleep_quality=None,
            average_sweating=None,
            average_libido=None,
            total_entries=0,
            date_range={"start": None, "end": None}
        )
    
    total_entries = len(entries)
    avg_mood = sum(e.mood_score for e in entries) / total_entries
    
    energy_entries = [e.energy_level for e in entries if e.energy_level is not None]
    avg_energy = sum(energy_entries) / len(energy_entries) if energy_entries else None
    
    stress_entries = [e.stress_level for e in entries if e.stress_level is not None]
    avg_stress = sum(stress_entries) / len(stress_entries) if stress_entries else None
    
    anxiety_entries = [e.anxiety_level for e in entries if e.anxiety_level is not None]
    avg_anxiety = sum(anxiety_entries) / len(anxiety_entries) if anxiety_entries else None
    
    rumination_entries = [e.rumination_level for e in entries if e.rumination_level is not None]
    avg_rumination = sum(rumination_entries) / len(rumination_entries) if rumination_entries else None
    
    anger_entries = [e.anger_level for e in entries if e.anger_level is not None]
    avg_anger = sum(anger_entries) / len(anger_entries) if anger_entries else None
    
    general_health_entries = [e.general_health for e in entries if e.general_health is not None]
    avg_general_health = sum(general_health_entries) / len(general_health_entries) if general_health_entries else None
    
    sleep_quality_entries = [e.sleep_quality for e in entries if e.sleep_quality is not None]
    avg_sleep_quality = sum(sleep_quality_entries) / len(sleep_quality_entries) if sleep_quality_entries else None
    
    sweating_entries = [e.sweating_level for e in entries if e.sweating_level is not None]
    avg_sweating = sum(sweating_entries) / len(sweating_entries) if sweating_entries else None
    
    libido_entries = [e.libido_level for e in entries if e.libido_level is not None]
    avg_libido = sum(libido_entries) / len(libido_entries) if libido_entries else None
    
    dates = [e.date for e in entries]
    
    return schemas.MoodStats(
        average_mood=round(avg_mood, 2),
        average_energy=round(avg_energy, 2) if avg_energy else None,
        average_stress=round(avg_stress, 2) if avg_stress else None,
        average_anxiety=round(avg_anxiety, 2) if avg_anxiety else None,
        average_rumination=round(avg_rumination, 2) if avg_rumination else None,
        average_anger=round(avg_anger, 2) if avg_anger else None,
        average_general_health=round(avg_general_health, 2) if avg_general_health else None,
        average_sleep_quality=round(avg_sleep_quality, 2) if avg_sleep_quality else None,
        average_sweating=round(avg_sweating, 2) if avg_sweating else None,
        average_libido=round(avg_libido, 2) if avg_libido else None,
        total_entries=total_entries,
        date_range={
            "start": str(min(dates)),
            "end": str(max(dates))
        }
    )

