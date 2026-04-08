import face_recognition
import cv2
import os
import pickle

# -------------------- PATH SETUP --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "encodings.pkl")

DISTANCE_THRESHOLD = 0.4

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


# -------------------- MAIN IMAGE PROCESS FUNCTION --------------------
def process_attendance(image_path):
    known_encodings, known_labels = load_known_faces()

    image = cv2.imread(image_path)

    if image is None:
        return {"status": "error", "message": "Invalid image"}

    # 🔥 Optimization (important for performance)
    small = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    if not encodings:
        return {"status": "no_face"}

    for enc in encodings:
        distances = face_recognition.face_distance(known_encodings, enc)
        min_dist = min(distances)

        if min_dist < DISTANCE_THRESHOLD:
            idx = distances.tolist().index(min_dist)
            name = known_labels[idx]

            return {
                "status": "identified",
                "name": name
            }

    return {"status": "unknown"}