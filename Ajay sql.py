import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Initialize database connection
conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    major TEXT,
    gpa REAL
)
""")
conn.commit()

# Functions for CRUD operations
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    major = entry_major.get()
    gpa = entry_gpa.get()
    
    if name and age and gender and major and gpa:
        cursor.execute("INSERT INTO students (name, age, gender, major, gpa) VALUES (?, ?, ?, ?, ?)",
                       (name, age, gender, major, float(gpa)))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully.")
        clear_entries()
        view_students()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

def view_students():
    for item in student_table.get_children():
        student_table.delete(item)
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        student_table.insert("", "end", values=row)

def update_student():
    try:
        selected = student_table.focus()
        student_id = student_table.item(selected, 'values')[0]
        name = entry_name.get()
        age = entry_age.get()
        gender = entry_gender.get()
        major = entry_major.get()
        gpa = entry_gpa.get()
        
        if name and age and gender and major and gpa:
            cursor.execute("UPDATE students SET name = ?, age = ?, gender = ?, major = ?, gpa = ? WHERE student_id = ?",
                           (name, int(age), gender, major, float(gpa), student_id))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully.")
            clear_entries()
            view_students()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a student to update.")

def delete_student():
    try:
        selected = student_table.focus()
        student_id = student_table.item(selected, 'values')[0]
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully.")
        view_students()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")

def search_student():
    search_name = entry_search.get()
    for item in student_table.get_children():
        student_table.delete(item)
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_name + '%',))
    rows = cursor.fetchall()
    for row in rows:
        student_table.insert("", "end", values=row)

def clear_entries():
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    entry_gender.delete(0, END)
    entry_major.delete(0, END)
    entry_gpa.delete(0, END)
    entry_search.delete(0, END)

# GUI setup
root = Tk()
root.title("Student Management System")
root.geometry("750x500")

# Input Fields
Label(root, text="Name:").place(x=20, y=20)
entry_name = Entry(root)
entry_name.place(x=100, y=20)

Label(root, text="Age:").place(x=20, y=50)
entry_age = Entry(root)
entry_age.place(x=100, y=50)

Label(root, text="Gender:").place(x=20, y=80)
entry_gender = Entry(root)
entry_gender.place(x=100, y=80)

Label(root, text="Major:").place(x=20, y=110)
entry_major = Entry(root)
entry_major.place(x=100, y=110)

Label(root, text="GPA:").place(x=20, y=140)
entry_gpa = Entry(root)
entry_gpa.place(x=100, y=140)

# Buttons
Button(root, text="Add Student", command=add_student).place(x=20, y=180)
Button(root, text="Update Student", command=update_student).place(x=120, y=180)
Button(root, text="Delete Student", command=delete_student).place(x=240, y=180)

# Search Field
Label(root, text="Search by Name:").place(x=400, y=20)
entry_search = Entry(root)
entry_search.place(x=500, y=20)
Button(root, text="Search", command=search_student).place(x=650, y=18)
Button(root, text="Show All", command=view_students).place(x=500, y=50)

# Student Table
columns = ("student_id", "name", "age", "gender", "major", "gpa")
student_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col.capitalize())
    student_table.column(col, width=100)
student_table.place(x=20, y=220, width=700, height=250)

view_students()

root.mainloop()

# Close the database connection when done
conn.close()
