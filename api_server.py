from fastapi import FastAPI, File, UploadFile
import shutil
import os
from attendance import mark_attendance_from_image, SESSION_MARKED
from attendance import SESSION_MARKED

app = FastAPI()

@app.post("/mark-attendance")
async def mark_attendance_api(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = mark_attendance_from_image(file_path)
    return result

@app.get("/session-attendance")
def session_attendance():
    return SESSION_MARKED
