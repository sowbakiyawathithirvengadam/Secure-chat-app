import tkinter as tk
import sqlite3

def view_users():
    conn = sqlite3.connect("database/chat.db")
    cur = conn.cursor()

    cur.execute("SELECT username, role FROM users")

    for row in cur.fetchall():
        print(row)

root = tk.Tk()
root.title("Admin Panel")

btn = tk.Button(root, text="View Users", command=view_users)
btn.pack()

root.mainloop()