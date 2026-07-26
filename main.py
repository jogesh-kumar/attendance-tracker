import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------- GLOBAL DATA ---------- #
subjects = {}

FILE_NAME = "attendance_data.json"

# ---------- FUNCTIONS ---------- #

def add_subject():
    name = subject_entry.get().strip()

    if name == "":
        messagebox.showerror("Error", "Enter subject name")
        return

    if name in subjects:
        messagebox.showerror("Error", "Subject already exists")
        return

    subjects[name] = {"present": 0, "absent": 0}
    subject_entry.delete(0, tk.END)
    update_listbox()
    update_dashboard()


def delete_subject():
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a subject")
        return

    subject = listbox.get(selected[0])
    del subjects[subject]

    update_listbox()
    update_dashboard()


def mark_present():
    update_attendance("present")


def mark_absent():
    update_attendance("absent")


def update_attendance(type_):
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a subject")
        return

    subject = listbox.get(selected[0])
    subjects[subject][type_] += 1

    update_dashboard()


def update_listbox():
    listbox.delete(0, tk.END)
    for subject in subjects:
        listbox.insert(tk.END, subject)


def update_dashboard():
    for row in tree.get_children():
        tree.delete(row)

    for subject, data in subjects.items():
        present = data["present"]
        absent = data["absent"]
        total = present + absent

        pct = (present / total * 100) if total != 0 else 0
        status = "Safe" if pct >= 75 else "Low"

        if pct >= 75:
            tree.insert("", tk.END,
                values=(subject, present, absent, f"{pct:.2f}%", status),
                tags=("safe",))
        else:
            tree.insert("", tk.END,
                values=(subject, present, absent, f"{pct:.2f}%", status),
                tags=("low",))


def save_data():
    try:
        with open(FILE_NAME, "w") as f:
            json.dump(subjects, f)
        messagebox.showinfo("Success", "Data saved successfully")
    except:
        messagebox.showerror("Error", "Failed to save data")


def load_data():
    global subjects

    if not os.path.exists(FILE_NAME):
        messagebox.showwarning("Warning", "No saved data found")
        return

    try:
        with open(FILE_NAME, "r") as f:
            subjects = json.load(f)

        update_listbox()
        update_dashboard()
        messagebox.showinfo("Success", "Data loaded successfully")
    except:
        messagebox.showerror("Error", "Failed to load data")


def reset_all():
    confirm = messagebox.askyesno("Confirm", "Delete all data?")

    if confirm:
        subjects.clear()
        update_listbox()
        update_dashboard()


# ---------- GUI ---------- #

root = tk.Tk()
root.title("Attendance Tracker System")
root.geometry("750x615")
root.configure(bg="#4599ff")

# ----- Subject Frame ----- #
frame1 = tk.Frame(root, bg="#4599ff")
frame1.pack(pady=10)

subject_entry = tk.Entry(frame1, width=30)
subject_entry.grid(row=0, column=0, padx=5)

tk.Button(frame1, text="Add Subject", command=add_subject).grid(row=0, column=1, padx=5)
tk.Button(frame1, text="Delete Subject", command=delete_subject).grid(row=0, column=2, padx=5)

# ----- Listbox ----- #
listbox = tk.Listbox(root, width=40, height=8,  bg="#C4C4C4", fg="black")
listbox.pack(pady=10)

# ----- Attendance Buttons ----- #
frame2 = tk.Frame(root, bg="#4599ff")
frame2.pack()

tk.Button(frame2, text="Mark Present", bg="green", fg="white", command=mark_present).grid(row=0, column=0, padx=10)
tk.Button(frame2, text="Mark Absent", bg="red", fg="white", command=mark_absent).grid(row=0, column=1, padx=10)

# ----- Dashboard ----- #
columns = ("Subject", "Present", "Absent", "Percentage", "Status")

frame_table = tk.Frame(root, bg="#4599ff")
frame_table.pack(pady=10, fill="x")

# ----- STYLE (ADD HERE) ----- #
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#ff0000",
                foreground="black",
                fieldbackground="#C4C4C4",
                rowheight=28)

style.configure("Treeview.Heading",
                background="#63FCFF",
                foreground="black",
                font=("Arial", 10, "bold"))

tree = ttk.Treeview(frame_table, columns=columns, show="headings")

# Row color tags
tree.tag_configure("safe", background="#52ff42")  # green
tree.tag_configure("low", background="#ff7878")   # red

tree.pack(fill="both", padx=20, pady=10)

for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center", width=130)

# ----- Bottom Buttons ----- #
frame3 = tk.Frame(root, bg="#4599ff")
frame3.pack(pady=10)

tk.Button(frame3, text="Save", command=save_data).grid(row=0, column=0, padx=10)
tk.Button(frame3, text="Load", command=load_data).grid(row=0, column=1, padx=10)
tk.Button(frame3, text="Reset", command=reset_all).grid(row=0, column=2, padx=10)

# ---------- RUN ---------- #
root.mainloop()
