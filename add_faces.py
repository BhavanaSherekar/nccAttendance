# import cv2
# import face_recognition
# import pickle
# import os

# if not os.path.exists("data"):
#     os.makedirs("data")

# video = cv2.VideoCapture(0)

# name = input("Enter Cadet Name: ")

# encodings = []
# count = 0

# print("Look at the camera. Capturing face data...")

# while True:
#     ret, frame = video.read()
#     if not ret:
#         break

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     locations = face_recognition.face_locations(rgb)
#     face_encs = face_recognition.face_encodings(rgb, locations)

#     for enc in face_encs:
#         encodings.append(enc)
#         count += 1

#     for (top, right, bottom, left) in locations:
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

#     cv2.putText(frame, f"Samples: {count}", (30, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     cv2.imshow("Register Face", frame)

#     if cv2.waitKey(1) == ord('q') or count == 30:
#         break

# video.release()
# cv2.destroyAllWindows()

# # Save data
# if os.path.exists("data/encodings.pkl"):
#     with open("data/encodings.pkl", "rb") as f:
#         data = pickle.load(f)
# else:
#     data = {}

# data[name] = encodings

# with open("data/encodings.pkl", "wb") as f:
#     pickle.dump(data, f)

# print("Face registration completed successfully.")


import cv2
import face_recognition
import pickle
import os


# -------------------- CONFIG --------------------
DATA_DIR = "data"
ENCODING_FILE = os.path.join(DATA_DIR, "encodings.pkl")
SAMPLES_REQUIRED = 30


# -------------------- ENSURE DATA FOLDER --------------------
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# -------------------- INPUT CADET NAME --------------------
name = input("Enter Cadet Name: ").strip()
if name == "":
    print("❌ Name cannot be empty")
    exit()


# -------------------- LOAD EXISTING ENCODINGS --------------------
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "rb") as f:
        data = pickle.load(f)
else:
    data = {}


# -------------------- CAMERA SETUP --------------------
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("❌ Camera not accessible")
    exit()

encodings = []
count = 0

print("📸 Look at the camera. Capturing face data...")
print("➡ Press 'q' to stop early")

# -------------------- CAPTURE LOOP --------------------
while True:
    ret, frame = video.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb, model="hog")
    face_encs = face_recognition.face_encodings(rgb, locations)

    for enc in face_encs:
        encodings.append(enc)
        count += 1

    for (top, right, bottom, left) in locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"Samples: {count}/{SAMPLES_REQUIRED}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow("Register Face - NCC Attendance", frame)

    if cv2.waitKey(1) == ord('q') or count >= SAMPLES_REQUIRED:
        break


# -------------------- CLEANUP --------------------
video.release()
cv2.destroyAllWindows()

if len(encodings) == 0:
    print("❌ No face captured. Try again.")
    exit()


# -------------------- SAVE ENCODINGS --------------------
if name in data:
    data[name].extend(encodings)
else:
    data[name] = encodings

with open(ENCODING_FILE, "wb") as f:
    pickle.dump(data, f)

print(f"✅ Face registration completed successfully for {name}")
print(f"📁 Total samples stored for {name}: {len(data[name])}")
