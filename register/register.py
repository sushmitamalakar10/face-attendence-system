# import os
# import cv2
# import tkinter as tk
# from deepface import DeepFace
# from tkinter import Tk, messagebox, simpledialog


# def register_user():
#     root = tk.Tk()
#     root.withdraw()
#     user_name = simpledialog.askstring("Register", "Enter name")
#     root.destroy()
    
#     if not user_name:
#         return
    
#     dataset_dir = os.path.join("dataset", user_name)
#     os.makedirs(dataset_dir, exist_ok=True)
    
#     cap = cv2.VideoCapture(0)
#     samples = 0
#     total = 20
    
#     messagebox.showinfo(
#         "Register",
#         f"Capturing {total} images for {user_name}.\n"
#         "Face detection will confirm each sample."
#     )
    
#     while samples < total:
#         ret, frame = cap.read()
#         if not ret:
#             continue

#         display_text = f"{user_name}: {samples}/{total} (Press SPACE to capture)"
#         cv2.putText(frame, display_text, (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

#         cv2.imshow("Register Face", frame)

#         key = cv2.waitKey(1) & 0xFF

#         if key == 27:  
#             break

#         elif key == 32:
#             filename = f"frame_{samples + 1:03d}.jpg"
#             temp_path = os.path.join("temp", filename)
#             os.makedirs("temp", exist_ok=True)
#             cv2.imwrite(temp_path, frame)

#             try:
#                 objs = DeepFace.extract_faces(
#                     temp_path,
#                     enforce_detection=False,
#                     detector_backend="opencv"
#                 )

#                 if not objs or not objs[0]["face"].any():
#                     messagebox.showwarning("Warning", "No face detected. Try again.")
#                 else:
#                     samples += 1
#                     img_path = os.path.join(dataset_dir, f"img_{samples:03d}.jpg")
#                     cv2.imwrite(img_path, frame)
#                     messagebox.showinfo("Captured", f"Image {samples} saved")

#             except Exception:
#                 messagebox.showerror("Error", "Face detection failed")

#             os.remove(temp_path)


#     cap.release()
#     cv2.destroyAllWindows()
#     messagebox.showinfo("Done", f"Registration for {user_name} with {samples} images.")
    
# register_user()

# import os
# import cv2
# from deepface import DeepFace
# from tkinter import simpledialog, Tk

# def register_user():
#     root = Tk()
#     root.withdraw()
#     user_name = simpledialog.askstring("Register", "Enter name")
#     root.destroy()

#     if not user_name:
#         return

#     dataset_dir = os.path.join("dataset", user_name)
#     os.makedirs(dataset_dir, exist_ok=True)

#     cap = cv2.VideoCapture(0)
#     samples = 0
#     total = 20

#     while samples < total:
#         ret, frame = cap.read()
#         if not ret:
#             continue

#         text = f"{user_name}: {samples}/{total} | SPACE=Capture ESC=Exit"
#         cv2.putText(frame, text, (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

#         cv2.imshow("Register Face", frame)
#         key = cv2.waitKey(1) & 0xFF

#         if key == 27:  # ESC
#             break

#         elif key == 32:  # SPACE
#             temp_path = "temp.jpg"
#             cv2.imwrite(temp_path, frame)

#             try:
#                 objs = DeepFace.extract_faces(
#                     temp_path,
#                     enforce_detection=False
#                 )

#                 if objs and objs[0]["face"].any():
#                     samples += 1
#                     img_path = os.path.join(dataset_dir, f"img_{samples:03d}.jpg")
#                     cv2.imwrite(img_path, frame)
#                     print(f"[INFO] Saved {samples}")
#                 else:
#                     print("[WARNING] No face detected")

#             except Exception:
#                 print("[ERROR] Detection failed")

#             if os.path.exists(temp_path):
#                 os.remove(temp_path)

#     cap.release()
#     cv2.destroyAllWindows()
#     print(f"[DONE] {user_name} registered with {samples} images")


# register_user()



import os
import cv2
from deepface import DeepFace
from tkinter import simpledialog, Tk

def register_user():
    root = Tk()
    root.withdraw()
    user_name = simpledialog.askstring("Register", "Enter name")
    root.destroy()

    if not user_name:
        return

    dataset_dir = os.path.join("dataset", user_name)
    os.makedirs(dataset_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    samples = 0
    total = 1

    while samples < total:
        ret, frame = cap.read()
        if not ret:
            continue

        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, frame)

        face_detected = False

        try:
            objs = DeepFace.extract_faces(
                temp_path,
                enforce_detection=False,
                detector_backend="opencv"
            )

            for obj in objs:
                if obj["face"].any():
                    face_detected = True

                    x = obj["facial_area"]["x"]
                    y = obj["facial_area"]["y"]
                    w = obj["facial_area"]["w"]
                    h = obj["facial_area"]["h"]

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        except:
            pass

        status = "Face Detected" if face_detected else "No Face"
        text = f"{user_name}: {samples}/{total} | {status} | SPACE=Capture"
        
        cv2.putText(frame, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0,255,0), 2)

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27: 
            break

        elif key == 32: 
            if face_detected:
                samples += 1
                img_path = os.path.join(dataset_dir, f"img_{samples:03d}.jpg")
                cv2.imwrite(img_path, frame)
                print(f"[INFO] Saved {samples}")
            else:
                print("[WARNING] No face detected")

        if os.path.exists(temp_path):
            os.remove(temp_path)

    cap.release()
    cv2.destroyAllWindows()
    print(f"[DONE] {user_name} registered with {samples} images")

