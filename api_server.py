from fastapi import FastAPI, File, UploadFile
import shutil
import os

from database import SessionLocal
from models import Attendance
from attendance_engine import process_attendance   # ✅ use your updated function

app = FastAPI()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

CURRENT_SESSION = "default_session"   # you can improve later


# 🔹 Mark attendance
@app.post("/mark-attendance")
async def mark_attendance(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Face recognition
    result = process_attendance(file_path)

    # If face not identified
    if result["status"] != "identified":
        os.remove(file_path)
        return result

    name = result["name"]

    db = SessionLocal()

    try:
        # Check duplicate
        existing = db.query(Attendance).filter_by(
            cadet_name=name,
            session_id=CURRENT_SESSION
        ).first()

        if existing:
            db.close()
            os.remove(file_path)
            return {"status": "duplicate", "name": name}

        # Save attendance
        record = Attendance(
            cadet_name=name,
            session_id=CURRENT_SESSION
        )

        db.add(record)
        db.commit()

    except Exception as e:
        db.rollback()
        db.close()
        os.remove(file_path)
        return {"status": "error", "message": str(e)}

    db.close()
    os.remove(file_path)

    return {"status": "marked", "name": name}


# 🔹 Get all attendance
@app.get("/attendance")
def get_attendance():
    db = SessionLocal()

    records = db.query(Attendance).all()

    db.close()

    return [
        {
            "name": r.cadet_name,
            "session": r.session_id,
            "time": str(r.timestamp)
        }
        for r in records
    ]


# 🔹 Start new session (optional but useful)
@app.post("/start-session")
def start_session():
    global CURRENT_SESSION
    import time
    CURRENT_SESSION = str(int(time.time()))
    return {"session_id": CURRENT_SESSION}