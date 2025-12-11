from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import LifestyleFactor, LifestyleFactorEntry, WellbeingMetricEntry
from app.auth import get_current_user
from datetime import datetime
import csv
import io

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/lifestyle-factors/export")
async def export_lifestyle_factors(db: Session = Depends(get_db)):
    """Export all lifestyle factors to CSV."""
    lifestyle_factors = db.query(LifestyleFactor).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['id', 'name', 'description', 'color', 'icon', 'is_active', 'created_at'])
    
    # Write data
    for lifestyle_factor in lifestyle_factors:
        writer.writerow([
            lifestyle_factor.id,
            lifestyle_factor.name,
            lifestyle_factor.description or '',
            lifestyle_factor.color,
            lifestyle_factor.icon or '',
            lifestyle_factor.is_active,
            lifestyle_factor.created_at.isoformat()
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=wellness_log_lifestyle_factors.csv"}
    )


@router.get("/lifestyle-factors/entries/export")
async def export_lifestyle_factor_entries(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Export lifestyle factor entries to CSV."""
    query = db.query(LifestyleFactorEntry)
    
    if start_date:
        query = query.filter(LifestyleFactorEntry.date >= start_date)
    if end_date:
        query = query.filter(LifestyleFactorEntry.date <= end_date)
    
    entries = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['id', 'lifestyle_factor_id', 'lifestyle_factor_name', 'date', 'completed', 'notes', 'created_at'])
    
    # Write data
    for entry in entries:
        lifestyle_factor = db.query(LifestyleFactor).filter(LifestyleFactor.id == entry.lifestyle_factor_id).first()
        writer.writerow([
            entry.id,
            entry.lifestyle_factor_id,
            lifestyle_factor.name if lifestyle_factor else '',
            entry.date.isoformat(),
            entry.completed,
            entry.notes or '',
            entry.created_at.isoformat()
        ])
    
    output.seek(0)
    filename = f"lifestyle_factor_entries_export_{datetime.now().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/wellbeing/export")
async def export_wellbeing_metric_entries(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Export mood entries to CSV."""
    query = db.query(WellbeingMetricEntry)
    
    if start_date:
        query = query.filter(WellbeingMetricEntry.date >= start_date)
    if end_date:
        query = query.filter(WellbeingMetricEntry.date <= end_date)
    
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
    filename = f"wellbeing_metrics_export_{datetime.now().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/all")
async def export_all_data(db: Session = Depends(get_db)):
    """Export all data (lifestyle factors, entries, mood) to a single CSV with multiple sheets concept."""
    # For simplicity, we'll create a ZIP file with multiple CSVs
    import zipfile
    from io import BytesIO
    
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Export lifestyle factors
        lifestyle_factors = db.query(LifestyleFactor).all()
        lifestyle_factors_csv = io.StringIO()
        writer = csv.writer(lifestyle_factors_csv)
        writer.writerow(['id', 'name', 'description', 'color', 'icon', 'is_active', 'created_at'])
        for lifestyle_factor in lifestyle_factors:
            writer.writerow([
                lifestyle_factor.id, lifestyle_factor.name, lifestyle_factor.description or '', lifestyle_factor.color,
                lifestyle_factor.icon or '', lifestyle_factor.is_active, lifestyle_factor.created_at.isoformat()
            ])
        zip_file.writestr('lifestyle_factors.csv', lifestyle_factors_csv.getvalue())
        
        # Export lifestyle factor entries
        entries = db.query(LifestyleFactorEntry).all()
        entries_csv = io.StringIO()
        writer = csv.writer(entries_csv)
        writer.writerow(['id', 'lifestyle_factor_id', 'lifestyle_factor_name', 'date', 'completed', 'notes', 'created_at'])
        for entry in entries:
            lifestyle_factor = db.query(LifestyleFactor).filter(LifestyleFactor.id == entry.lifestyle_factor_id).first()
            writer.writerow([
                entry.id, entry.lifestyle_factor_id, lifestyle_factor.name if lifestyle_factor else '',
                entry.date.isoformat(), entry.completed, entry.notes or '',
                entry.created_at.isoformat()
            ])
        zip_file.writestr('lifestyle_factor_entries.csv', entries_csv.getvalue())
        
        # Export mood entries
        wellbeing_metric_entries = db.query(WellbeingMetricEntry).all()
        mood_csv = io.StringIO()
        writer = csv.writer(mood_csv)
        writer.writerow(['id', 'date', 'time', 'mood_score', 'energy_level', 'stress_level', 'notes', 'tags', 'created_at'])
        for entry in wellbeing_metric_entries:
            writer.writerow([
                entry.id, entry.date.isoformat(), entry.time.isoformat() if entry.time else '',
                entry.mood_score, entry.energy_level or '', entry.stress_level or '',
                entry.notes or '', entry.tags or '', entry.created_at.isoformat()
            ])
        zip_file.writestr('wellbeing_metric_entries.csv', mood_csv.getvalue())
    
    zip_buffer.seek(0)
    filename = f"wellness_log_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return StreamingResponse(
        iter([zip_buffer.getvalue()]),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

