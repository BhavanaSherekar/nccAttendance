import face_recognition
import cv2
import os
import csv
import pickle
from datetime import datetime

# -------------------- PATH SETUP --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "encodings.pkl")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "Attendance")

DISTANCE_THRESHOLD = 0.4

# -------------------- SESSION MEMORY --------------------
SESSION_MARKED = {}  # name -> time

# -------------------- LOAD KNOWN FACES --------------------
def load_known_faces():
    with open(DATA_PATH, "rb") as f:
        known_data = pickle.load(f)

    known_encodings = []
    known_labels = []

    for name, enc_list in known_data.items():
        for enc in enc_list:
            known_encodings.append(enc)
            known_labels.append(name)

    return known_encodings, known_labels

# -------------------- MARK ATTENDANCE --------------------
def mark_attendance(name):
    global SESSION_MARKED

    if name in SESSION_MARKED:
        return False

    if not os.path.exists(ATTENDANCE_DIR):
        os.makedirs(ATTENDANCE_DIR)

    date = datetime.now().strftime("%d-%m-%Y")
    time_now = datetime.now().strftime("%H:%M:%S")
    file_path = os.path.join(ATTENDANCE_DIR, f"Attendance_{date}.csv")

    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            csv.writer(f).writerow(["NAME", "TIME"])

    with open(file_path, "a", newline="") as f:
        csv.writer(f).writerow([name, time_now])

    SESSION_MARKED[name] = time_now
    return True


# -------------------- MAIN IMAGE PROCESS FUNCTION --------------------
def mark_attendance_from_image(image_path):
    known_encodings, known_labels = load_known_faces()

    image = cv2.imread(image_path)
    if image is None:
        return {"status": "error", "message": "Invalid image"}

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    if not encodings:
        return {"status": "failed", "message": "No face detected"}

    for enc in encodings:
        distances = face_recognition.face_distance(known_encodings, enc)
        min_dist = min(distances)

        if min_dist < DISTANCE_THRESHOLD:
            idx = distances.tolist().index(min_dist)
            name = known_labels[idx]

            if mark_attendance(name):
                return {
                    "status": "success",
                    "name": name,
                    "message": "Attendance marked"
                }
            else:
                return {
                    "status": "duplicate",
                    "name": name,
                    "message": "Already marked for this session"
                }

    return {"status": "failed", "message": "Face not recognized"}
