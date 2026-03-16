import tkinter as tk
from tkinter import messagebox
import subprocess

def login():
    username = entry_name.get()

    if username.strip() == "":
        messagebox.showerror("Error", "Please enter your name")
    else:
        subprocess.Popen(["python", "client/chat_ui.py", username])
        root.destroy()

root = tk.Tk()
root.title("Chat Login")
root.geometry("400x300")
root.configure(bg="#1e1e2f")

# Center Frame (Card)
frame = tk.Frame(root, bg="#2c2c3e", padx=30, pady=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

title = tk.Label(
    frame,
    text="💬 Chat Login",
    font=("Helvetica", 18, "bold"),
    fg="white",
    bg="#2c2c3e"
)
title.pack(pady=(0,20))

label = tk.Label(
    frame,
    text="Enter Your Name",
    font=("Arial", 12),
    fg="#dcdcdc",
    bg="#2c2c3e"
)
label.pack()

entry_name = tk.Entry(
    frame,
    width=25,
    font=("Arial", 12),
    bd=0,
    highlightthickness=2,
    highlightbackground="#4a90e2",
    highlightcolor="#4a90e2"
)
entry_name.pack(pady=10, ipady=5)

def on_enter(e):
    login_button['bg'] = "#357ABD"

def on_leave(e):
    login_button['bg'] = "#4a90e2"

login_button = tk.Button(
    frame,
    text="Join Chat",
    font=("Arial", 12, "bold"),
    bg="#4a90e2",
    fg="white",
    bd=0,
    padx=15,
    pady=5,
    command=login
)

login_button.pack(pady=10)

login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

root.mainloop()