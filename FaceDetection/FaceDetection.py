import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time

class FaceDetectionApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Face Detection - Image & Video")
        self.window.geometry("1000x700")
        self.window.configure(bg="#1a1a1a")

        heading = tk.Label(self.window,
                           text="FACE DETECTION",
                           font=("Arial", 28, "bold"),
                           fg="cyan",
                           bg="#1a1a1a")
        heading.pack(pady=20)

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        self.media_label = tk.Label(self.window, bg="#1a1a1a")
        self.media_label.pack()

        button_frame = tk.Frame(self.window, bg="#1a1a1a")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Detect Faces in Image",
                  font=("Arial", 12, "bold"), width=22,
                  command=self.upload_image).pack(side=tk.LEFT, padx=20)

        tk.Button(button_frame, text="Detect Faces in Video",
                  font=("Arial", 12, "bold"), width=22,
                  command=self.open_video).pack(side=tk.LEFT, padx=20)

        self.cap = None
        self.running = False

    def resize_for_display(self, frame):
        win_w = int(self.window.winfo_width() * 0.5)
        win_h = int(self.window.winfo_height() * 0.5)

        h, w = frame.shape[:2]
        aspect = w / h

        if win_w / aspect <= win_h:
            win_h = int(win_w / aspect)
        else:
            win_w = int(win_h * aspect)

        return cv2.resize(frame, (win_w, win_h))

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not file_path:
            return

        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        resized = self.resize_for_display(img)

        img_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img_display = ImageTk.PhotoImage(Image.fromarray(img_rgb))

        self.media_label.imgtk = img_display
        self.media_label.configure(image=img_display)

        messagebox.showinfo("Image Result", f"Faces Detected: {len(faces)}")

    def open_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video files", "*.mp4 *.avi *.mkv")]
        )
        if not file_path:
            return

        self.cap = cv2.VideoCapture(file_path)
        self.running = True
        self.total_faces = 0
        self.total_frames = 0
        self.start_time = time.time()

        self.process_video()

    def process_video(self):
        if not self.running or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self.finish_processing()
            return

        self.total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        self.total_faces += len(faces)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        resized_frame = self.resize_for_display(frame)

        img_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img_rgb))

        self.media_label.imgtk = img
        self.media_label.configure(image=img)

        self.window.after(10, self.process_video)

    def finish_processing(self):
        self.running = False
        self.cap.release()

        elapsed_time = time.time() - self.start_time
        msg = (
            f"Video Analysis Complete!\n\n"
            f"Total Frames Processed: {self.total_frames}\n"
            f"Total Face Detections: {self.total_faces}\n"
            f"Time Taken: {elapsed_time:.2f} seconds"
        )
        messagebox.showinfo("Video Result", msg)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FaceDetectionApp()
    app.run()
