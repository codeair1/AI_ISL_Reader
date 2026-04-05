import threading
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

inference_thread = None


def show_letter_image(letter_index: int):
    folder = os.path.join("data", str(letter_index))
    if not os.path.isdir(folder):
        messagebox.showerror("Folder Not Found", f"Directory '{folder}' does not exist.")
        return

    img_number = random.randint(0, 199)
    img_path = os.path.join(folder, f"{img_number}.jpg")

    if not os.path.isfile(img_path):
        messagebox.showerror("Image Not Found", f"Image '{img_path}' does not exist.")
        return

    img_win = tk.Toplevel()
    letter_char = chr(65 + letter_index)
    img_win.title(f"Letter: {letter_char}  |  File: {img_path}")
    img_win.resizable(False, False)

    if PIL_AVAILABLE:
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(img_win, image=photo)
        lbl.image = photo
        lbl.pack(padx=10, pady=10)
    else:
        tk.Label(img_win, text="Install Pillow to preview images:\npip install Pillow",
                 font=("Helvetica", 11), fg="red").pack(padx=20, pady=20)

    tk.Label(img_win,
             text=f"Letter: {letter_char}   Index: {letter_index}   File: {img_number}.jpg",
             font=("Helvetica", 11)).pack(pady=(0, 10))


def run_inference_safe(status_var, btn):
    global inference_thread
    try:
        # NOTE: file is inference_classifier.py but function inside is inference_classifer (no 's')
        from inference_classifier import inference_classifier
        status_var.set("Status: Running... (press ESC in webcam to stop)")
        btn.config(state="disabled")
        inference_classifier()
    except ImportError as e:
        messagebox.showerror("Import Error", f"Could not load inference module:\n{e}")
        status_var.set("Status: Import failed.")
    except Exception as e:
        messagebox.showerror("Inference Error", str(e))
        status_var.set(f"Status: Error — {e}")
    finally:
        status_var.set("Status: Stopped. Click button to restart.")
        btn.config(state="normal")
        inference_thread = None


def launch_inference(status_var, btn):
    global inference_thread

    if inference_thread is not None and inference_thread.is_alive():
        messagebox.showinfo("Already Running",
                            "Inference is already running.\nPress ESC in the webcam window to stop it first.")
        return

    status_var.set("Status: Loading model...")
    inference_thread = threading.Thread(
        target=run_inference_safe,
        args=(status_var, btn),
        daemon=True
    )
    inference_thread.start()


def build_gui():
    root = tk.Tk()
    root.title("Sign Language Detector — Control Panel")
    root.resizable(False, False)

    tk.Label(root, text="Sign Language Detector",
             font=("Helvetica", 16, "bold"), pady=10).pack()

    status_var = tk.StringVar(value="Status: Idle")

    inference_btn = ttk.Button(root, text="▶  Start Webcam Inference", width=28)
    inference_btn.config(command=lambda: launch_inference(status_var, inference_btn))
    inference_btn.pack(pady=(6, 4))

    tk.Label(root, textvariable=status_var,
             font=("Helvetica", 9), fg="blue", wraplength=340).pack(pady=(0, 8))

    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=4)

    tk.Label(root, text="Select a letter to view a sample image:",
             font=("Helvetica", 11)).pack(pady=(8, 4))

    grid_frame = tk.Frame(root, padx=10, pady=6)
    grid_frame.pack()

    COLS = 9
    for i in range(26):
        letter = chr(65 + i)
        row, col = divmod(i, COLS)
        ttk.Button(grid_frame, text=letter, width=4,
                   command=lambda idx=i: show_letter_image(idx)
                   ).grid(row=row, column=col, padx=3, pady=3)

    tk.Label(root, text="Press ESC inside the webcam window to stop inference.",
             font=("Helvetica", 9), fg="grey", pady=8).pack()

    root.mainloop()


if __name__ == "__main__":
    build_gui()