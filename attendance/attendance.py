import os
import cv2
import csv
from datetime import datetime
from deepface import DeepFace
from tkinter import Tk, messagebox


def mark_attendance(name):
    os.makedirs("records", exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join("records", f"attendance_{today}.csv")
    file_exists = os.path.isfile(file_path)

    already_marked = False

    if file_exists:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) > 0 and row[0] == name:
                    already_marked = True
                    break

    if not already_marked:
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["Name", "Date", "Time"])

            now = datetime.now()
            writer.writerow([
                name,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S")
            ])

        print(f"[ATTENDANCE] Marked for {name}")
    
def recognize_and_attendance():
    if not os.path.exists("dataset") or not os.listdir("dataset"):
        root = Tk()
        root.withdraw()
        messagebox.showwarning("Warning", "No registered users found in dataset folder.")
        root.destroy()
        return

    os.makedirs("temp", exist_ok=True)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        temp_path = os.path.join("temp", "temp_attendance.jpg")
        cv2.imwrite(temp_path, frame)

        person_name = "Unknown"

        try:
            result = DeepFace.find(
                img_path=temp_path,
                db_path="dataset",
                enforce_detection=False,
                detector_backend="opencv",
                silent=True
            )

            if len(result) > 0 and not result[0].empty:
                identity_path = result[0].iloc[0]["identity"]
                person_name = os.path.basename(os.path.dirname(identity_path))
                mark_attendance(person_name)

        except Exception as e:
            print("[ERROR]", e)

        color = (0, 255, 0) if person_name != "Unknown" else (0, 0, 255)
        text = f"Person: {person_name} | ESC=Exit"

        cv2.putText(
            frame,
            text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        cv2.imshow("Attendance System", frame)

        if os.path.exists(temp_path):
            os.remove(temp_path)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()