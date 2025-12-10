from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime, timedelta
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.LifestyleFactor)
def create_lifestyle_factor(lifestyle_factor: schemas.LifestyleFactorCreate, db: Session = Depends(get_db)):
    """Create a new lifestyle factor to track"""
    db_lifestyle_factor = models.LifestyleFactor(**lifestyle_factor.model_dump())
    db.add(db_lifestyle_factor)
    db.commit()
    db.refresh(db_lifestyle_factor)
    return db_lifestyle_factor

@router.get("/", response_model=List[schemas.LifestyleFactor])
def get_lifestyle_factors(include_inactive: bool = False, db: Session = Depends(get_db)):
    """Get all lifestyle factors"""
    query = db.query(models.LifestyleFactor)
    if not include_inactive:
        query = query.filter(models.LifestyleFactor.is_active == True)
    return query.order_by(models.LifestyleFactor.created_at).all()

@router.get("/{lifestyle_factor_id}", response_model=schemas.LifestyleFactor)
def get_lifestyle_factor(lifestyle_factor_id: int, db: Session = Depends(get_db)):
    """Get a specific lifestyle factor"""
    lifestyle_factor = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.id == lifestyle_factor_id).first()
    if not lifestyle_factor:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    return lifestyle_factor

@router.put("/{lifestyle_factor_id}", response_model=schemas.LifestyleFactor)
def update_lifestyle_factor(lifestyle_factor_id: int, lifestyle_factor_update: schemas.LifestyleFactorUpdate, db: Session = Depends(get_db)):
    """Update a lifestyle factor"""
    db_lifestyle_factor = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.id == lifestyle_factor_id).first()
    if not db_lifestyle_factor:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    update_data = lifestyle_factor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lifestyle_factor, key, value)
    
    db.commit()
    db.refresh(db_lifestyle_factor)
    return db_lifestyle_factor

@router.delete("/{lifestyle_factor_id}")
def delete_lifestyle_factor(lifestyle_factor_id: int, db: Session = Depends(get_db)):
    """Permanently delete a lifestyle factor and all its entries"""
    db_lifestyle_factor = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.id == lifestyle_factor_id).first()
    if not db_lifestyle_factor:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    # Delete all associated entries first
    db.query(models.LifestyleFactorEntry).filter(models.LifestyleFactorEntry.lifestyle_factor_id == lifestyle_factor_id).delete()
    
    # Delete the lifestyle factor itself
    db.delete(db_lifestyle_factor)
    db.commit()
    return {"message": "Lifestyle factor deleted successfully"}

@router.post("/{lifestyle_factor_id}/archive", response_model=schemas.LifestyleFactor)
def archive_lifestyle_factor(lifestyle_factor_id: int, db: Session = Depends(get_db)):
    """Archive a lifestyle factor (set is_active to False)"""
    db_lifestyle_factor = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.id == lifestyle_factor_id).first()
    if not db_lifestyle_factor:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    db_lifestyle_factor.is_active = False
    db.commit()
    db.refresh(db_lifestyle_factor)
    return db_lifestyle_factor

@router.post("/{lifestyle_factor_id}/unarchive", response_model=schemas.LifestyleFactor)
def unarchive_lifestyle_factor(lifestyle_factor_id: int, db: Session = Depends(get_db)):
    """Unarchive a lifestyle factor (set is_active to True)"""
    db_lifestyle_factor = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.id == lifestyle_factor_id).first()
    if not db_lifestyle_factor:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    db_lifestyle_factor.is_active = True
    db.commit()
    db.refresh(db_lifestyle_factor)
    return db_lifestyle_factor

@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """Get all unique lifestyle factor categories"""
    categories = db.query(models.LifestyleFactor.category).distinct().all()
    return {"categories": [cat[0] for cat in categories if cat[0]]}


@router.post("/entries", response_model=schemas.LifestyleFactorEntry)
def create_lifestyle_factor_entry(entry: schemas.LifestyleFactorEntryCreate, db: Session = Depends(get_db)):
    """Create or update a lifestyle factor entry for a specific date"""
    # Check if entry already exists for this lifestyle factor and date
    existing_entry = db.query(models.LifestyleFactorEntry).filter(
        models.LifestyleFactorEntry.lifestyle_factor_id == entry.lifestyle_factor_id,
        models.LifestyleFactorEntry.date == entry.date
    ).first()
    
    if existing_entry:
        existing_entry.completed = entry.completed
        existing_entry.notes = entry.notes
        db.commit()
        db.refresh(existing_entry)
        return existing_entry
    
    db_entry = models.LifestyleFactorEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/entries/range", response_model=List[schemas.LifestyleFactorEntry])
def get_lifestyle_factor_entries_range(
    start_date: date,
    end_date: date,
    lifestyle_factor_id: int = None,
    db: Session = Depends(get_db)
):
    """Get lifestyle factor entries for a date range"""
    query = db.query(models.LifestyleFactorEntry).filter(
        models.LifestyleFactorEntry.date >= start_date,
        models.LifestyleFactorEntry.date <= end_date
    )
    
    if lifestyle_factor_id:
        query = query.filter(models.LifestyleFactorEntry.lifestyle_factor_id == lifestyle_factor_id)
    
    return query.order_by(models.LifestyleFactorEntry.date).all()

@router.get("/entries/date/{entry_date}", response_model=List[schemas.LifestyleFactorEntry])
def get_lifestyle_factor_entries_by_date(entry_date: date, db: Session = Depends(get_db)):
    """Get all lifestyle factor entries for a specific date"""
    return db.query(models.LifestyleFactorEntry).filter(
        models.LifestyleFactorEntry.date == entry_date
    ).all()

@router.get("/{lifestyle_factor_id}/stats", response_model=schemas.LifestyleFactorStats)
def get_lifestyle_factor_stats(lifestyle_factor_id: int, db: Session = Depends(get_db)):
    """Get statistics for a specific lifestyle factor"""
    lifestyle_factor = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.id == lifestyle_factor_id).first()
    if not lifestyle_factor:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    entries = db.query(models.LifestyleFactorEntry).filter(
        models.LifestyleFactorEntry.lifestyle_factor_id == lifestyle_factor_id
    ).order_by(models.LifestyleFactorEntry.date).all()
    
    if not entries:
        return schemas.LifestyleFactorStats(
            lifestyle_factor_id=lifestyle_factor_id,
            lifestyle_factor_name=lifestyle_factor.name,
            total_days=0,
            completed_days=0,
            completion_rate=0.0,
            current_streak=0,
            longest_streak=0
        )
    
    completed_entries = [e for e in entries if e.completed]
    total_days = len(entries)
    completed_days = len(completed_entries)
    completion_rate = (completed_days / total_days * 100) if total_days > 0 else 0
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    # Sort by date
    sorted_entries = sorted(entries, key=lambda x: x.date)
    
    for i, entry in enumerate(sorted_entries):
        if entry.completed:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0
    
    # Calculate current streak (from today backwards)
    today = date.today()
    for entry in reversed(sorted_entries):
        if entry.date > today:
            continue
        if entry.completed and (today - entry.date).days <= len(sorted_entries):
            current_streak += 1
        else:
            break
    
    return schemas.LifestyleFactorStats(
        lifestyle_factor_id=lifestyle_factor_id,
        lifestyle_factor_name=lifestyle_factor.name,
        total_days=total_days,
        completed_days=completed_days,
        completion_rate=round(completion_rate, 2),
        current_streak=current_streak,
        longest_streak=longest_streak
    )

