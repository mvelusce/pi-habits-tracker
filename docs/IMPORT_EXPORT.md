# Data Import/Export Guide

## Importing Legacy Data

### Quick Start

If you have existing habit data in CSV format (Habits.csv and Checkmarks.csv), you can import it using:

```bash
./import_data.sh
```

This script will:
1. Check for your CSV files in the `data/` directory
2. Set up a virtual environment if needed
3. Import all habits and their completion history
4. Ask if you want to include archived habits

### Manual Import

If you prefer to run the import manually:

```bash
cd backend
source venv/bin/activate
python import_legacy_data.py --habits=../data/Habits.csv --checkmarks=../data/Checkmarks.csv
```

**Options:**
- `--habits`: Path to your Habits.csv file
- `--checkmarks`: Path to your Checkmarks.csv file
- `--include-archived`: Include checkmarks for archived habits (optional)

### Data Format

**Habits.csv** should contain:
- Position, Name, Type, Question, Description, FrequencyNumerator, FrequencyDenominator, Color, Unit, Target Type, Target Value, Archived?

**Checkmarks.csv** should contain:
- Date column followed by one column per habit
- Values: `YES_MANUAL` (completed), `YES_AUTO`, `NO`, `UNKNOWN`
- Only `YES_MANUAL` entries are imported as completed habits

### Import Rules

1. **Habits**: Creates new habits with names, colors, and icons
2. **Archived Habits**: By default, skips checkmarks for archived habits
3. **Duplicates**: Skips habits that already exist (by name)
4. **Completion**: Only `YES_MANUAL` values count as completed

## Exporting Data

### Via API

The application provides several export endpoints:

**Export all data (ZIP file):**
```bash
curl http://localhost:8000/api/export/all -o backup.zip
```

**Export only habits:**
```bash
curl http://localhost:8000/api/export/habits/export -o habits.csv
```

**Export habit entries:**
```bash
curl "http://localhost:8000/api/export/habits/entries/export?start_date=2025-01-01" -o entries.csv
```

**Export mood entries:**
```bash
curl "http://localhost:8000/api/export/mood/export?start_date=2025-01-01" -o mood.csv
```

### Via Web Interface

You can also access these exports through your browser:
- All data: http://localhost:8000/api/export/all
- Habits: http://localhost:8000/api/export/habits/export
- Habit entries: http://localhost:8000/api/export/habits/entries/export
- Mood entries: http://localhost:8000/api/export/mood/export

## Database Backup

### SQLite Database

Your data is stored in `data/habits_tracker.db`. To backup:

```bash
# Simple copy
cp data/habits_tracker.db data/habits_tracker_backup_$(date +%Y%m%d).db

# Or use SQLite backup command
sqlite3 data/habits_tracker.db ".backup data/habits_tracker_backup.db"
```

### Restore from Backup

```bash
cp data/habits_tracker_backup.db data/habits_tracker.db
```

## Automated Backups

You can set up automated backups using cron:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /path/to/habits-tracker && cp data/habits_tracker.db data/backups/habits_tracker_$(date +\%Y\%m\%d).db
```

## Import/Export Tips

1. **Before importing**: Backup your current database
2. **Test first**: Try importing with a small dataset
3. **Regular exports**: Export your data regularly as backup
4. **Archive habits**: Use archived habits feature to keep history without cluttering active habits

## Troubleshooting

### Import fails with "file not found"
- Make sure CSV files are in the `data/` directory
- Check file permissions

### Import shows "habit already exists"
- The import script skips existing habits
- Delete existing habits first if you want to re-import

### Missing dependencies
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Database locked error
- Stop the Docker containers: `docker-compose down`
- Run import
- Restart containers: `docker-compose up -d`

