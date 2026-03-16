import tkinter as tk
from tkinter import filedialog
import socket
import threading
import sys
from PIL import Image, ImageTk

HOST = "127.0.0.1"
PORT = 5050

name = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Chat App")
root.geometry("500x500")

# ---------------- TOP BAR ----------------
top_bar = tk.Frame(root, bg="#1F2C34", height=55)
top_bar.pack(side="top", fill="x")
top_bar.pack_propagate(False)

tk.Label(top_bar, text="💬", font=("Helvetica", 20),
         bg="#1F2C34", fg="#00A884").pack(side="left", padx=(12, 8))

tk.Label(top_bar, text=f"{name}'s Chat",
         font=("Helvetica", 13, "bold"),
         bg="#1F2C34", fg="#E9EDEF").pack(side="left")

tk.Label(top_bar, text="online",
         font=("Helvetica", 9),
         bg="#1F2C34", fg="#8696A0").pack(side="left", padx=(4, 0))

# ---------------- CHAT AREA ----------------
chat_frame = tk.Frame(root)
chat_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(chat_frame, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)


# ---------------- BACKGROUND IMAGE ----------------
bg_image = Image.open("image/background.jpg")
bg_image = bg_image.resize((500,500))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ---------------- MESSAGE FRAME ----------------
messages_frame = tk.Frame(canvas, bg="white")

window = canvas.create_window((0, 0), window=messages_frame, anchor="nw")

# Make frame full width
def resize_frame(event):
    canvas.itemconfig(window, width=event.width)

canvas.bind("<Configure>", resize_frame)

messages_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# ---------------- TEXT MESSAGE ----------------
def add_message(sender, message):

    bubble_frame = tk.Frame(messages_frame, pady=5, bg="white")

    if sender == name:
        bubble_frame.pack(anchor="e", padx=10)

        msg = tk.Label(
            bubble_frame,
            text=message,
            bg="#DCF8C6",
            fg="black",
            padx=10,
            pady=5,
            wraplength=250
        )

    else:
        bubble_frame.pack(anchor="w", padx=10)

        msg = tk.Label(
            bubble_frame,
            text=f"{sender}: {message}",
            bg="#FFFFFF",
            fg="black",
            padx=10,
            pady=5,
            wraplength=250
        )

    msg.pack()

    canvas.update_idletasks()
    canvas.yview_moveto(1)


# ---------------- SYSTEM MESSAGE ----------------
def add_system_message(text):

    label = tk.Label(
        messages_frame,
        text=text,
        fg="blue",
        bg="white",
        font=("Arial",10,"italic")
    )

    label.pack(pady=5)

# ---------------- SEND TEXT ----------------
def send_message():

    msg = msg_entry.get()

    if msg != "":
        client.send(f"{name}:{msg}".encode())
        add_message(name, msg)

    msg_entry.delete(0, tk.END)



# ---------------- RECEIVE ----------------
def receive_messages():

    while True:
        try:

            message = client.recv(1024).decode()

            if message == "NAME":
                client.send(name.encode())

            else:

                if ":" in message:

                    sender, msg = message.split(":", 1)

                    # only show message if from other user
                    if sender != name:
                        add_message(sender, msg)

                else:
                    add_system_message(message)

        except Exception as e:
            print("Error:", e)
            break
# ---------------- EMOJI ----------------
def add_emoji(emoji):
    msg_entry.insert(tk.END, emoji)

emoji_frame = tk.Frame(root)

emojis = ["😀","😂","😍","😎","😭","👍","🔥","❤️","🎉","😇","😡","🤔"]

for e in emojis:
    b = tk.Button(emoji_frame, text=e, font=("Arial",14),
                  command=lambda emoji=e: add_emoji(emoji))
    b.pack(side="left", padx=2)

def toggle_emoji():

    if emoji_frame.winfo_ismapped():
        emoji_frame.pack_forget()
    else:
        emoji_frame.pack(fill="x")

# ---------------- INPUT AREA ----------------
bottom = tk.Frame(root)
bottom.pack(fill="x", pady=10)

msg_entry = tk.Entry(bottom, width=30,font=("Arial",11))
msg_entry.pack(side="left", padx=10)
msg_entry.bind("<Return>", lambda e: send_message())


send_btn = tk.Button(bottom, text="Send", command=send_message)
send_btn.pack(side="left")

emoji_btn = tk.Button(bottom, text="😊", command=toggle_emoji)
emoji_btn.pack(side="right", padx=10)

# ---------------- THREAD ----------------
thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

root.mainloop()