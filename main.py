import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tkinter import Tk, Label, Button
from register.register import register_user
from attendance.attendance import recognize_and_attendance


def main():
    root = Tk()
    root.title("Face Attendance with DeepFace + OpenCV")
    root.geometry("800x500")
    root.resizable(False, False)

    Label(
        root,
        text="Face Attendance System",
        font=("Arial", 12, "bold"),
        justify="center",
    ).pack(pady=20)

    Button(root, text="Register User", width=25, command=register_user).pack(pady=10)
    Button(root, text="Start Attendance", width=25, command=recognize_and_attendance).pack(pady=10)
    Button(root, text="Exit", width=25, command=root.destroy).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()