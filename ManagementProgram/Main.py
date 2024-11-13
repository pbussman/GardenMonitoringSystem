import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# Function to add a new garden bed
def add_garden_bed(name, plant, plant_date):
    conn = sqlite3.connect('garden_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO GardenBeds (name, plant, plant_date)
        VALUES (?, ?, ?)
    ''', (name, plant, plant_date))
    conn.commit()
    conn.close()

# Function to add a maintenance activity
def add_maintenance(garden_bed_id, activity, date, notes=None):
    conn = sqlite3.connect('garden_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Maintenance (garden_bed_id, activity, date, notes)
        VALUES (?, ?, ?, ?)
    ''', (garden_bed_id, activity, date, notes))
    conn.commit()
    conn.close()

# Function to get all garden beds
def get_garden_beds():
    conn = sqlite3.connect('garden_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM GardenBeds')
    garden_beds = cursor.fetchall()
    conn.close()
    return garden_beds

# Function to get maintenance activities for a garden bed
def get_maintenance(garden_bed_id):
    conn = sqlite3.connect('garden_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Maintenance WHERE garden_bed_id = ?', (garden_bed_id,))
    maintenance = cursor.fetchall()
    conn.close()
    return maintenance

# Function to add a new garden bed from the GUI
def add_garden_bed_gui():
    name = name_entry.get()
    plant = plant_entry.get()
    plant_date = plant_date_entry.get()
    if name and plant and plant_date:
        add_garden_bed(name, plant, plant_date)
        messagebox.showinfo("Success", "Garden bed added successfully!")
        name_entry.delete(0, tk.END)
        plant_entry.delete(0, tk.END)
        plant_date_entry.delete(0, tk.END)
        update_garden_bed_list()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to add a maintenance activity from the GUI
def add_maintenance_gui():
    garden_bed_id = garden_bed_id_entry.get()
    activity = activity_entry.get()
    date = date_entry.get()
    notes = notes_entry.get()
    if garden_bed_id and activity and date:
        add_maintenance(garden_bed_id, activity, date, notes)
        messagebox.showinfo("Success", "Maintenance activity added successfully!")
        garden_bed_id_entry.delete(0, tk.END)
        activity_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        notes_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to update the garden bed list in the GUI
def update_garden_bed_list():
    garden_beds = get_garden_beds()
    garden_bed_list.delete(*garden_bed_list.get_children())
    for bed in garden_beds:
        garden_bed_list.insert("", "end", values=(bed[0], bed[1], bed[2], bed[3]))

# Create the main window
root = tk.Tk()
root.title("Garden Management")

# Create and place the widgets for adding a garden bed
tk.Label(root, text="Add Garden Bed").grid(row=0, column=0, columnspan=2)
tk.Label(root, text="Name:").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)
tk.Label(root, text="Plant:").grid(row=2, column=0)
plant_entry = tk.Entry(root)
plant_entry.grid(row=2, column=1)
tk.Label(root, text="Plant Date (YYYY-MM-DD):").grid(row=3, column=0)
plant_date_entry = tk.Entry(root)
plant_date_entry.grid(row=3, column=1)
tk.Button(root, text="Add Garden Bed", command=add_garden_bed_gui).grid(row=4, column=0, columnspan=2)

# Create and place the widgets for adding a maintenance activity
tk.Label(root, text="Add Maintenance Activity").grid(row=5, column=0, columnspan=2)
tk.Label(root, text="Garden Bed ID:").grid(row=6, column=0)
garden_bed_id_entry = tk.Entry(root)
garden_bed_id_entry.grid(row=6, column=1)
tk.Label(root, text="Activity:").grid(row=7, column=0)
activity_entry = tk.Entry(root)
activity_entry.grid(row=7, column=1)
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=8, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=8, column=1)
tk.Label(root, text="Notes:").grid(row=9, column=0)
notes_entry = tk.Entry(root)
notes_entry.grid(row=9, column=1)
tk.Button(root, text="Add Maintenance Activity", command=add_maintenance_gui).grid(row=10, column=0, columnspan=2)

# Create and place the treeview for displaying garden beds
tk.Label(root, text="Garden Beds").grid(row=11, column=0, columnspan=2)
columns = ("ID", "Name", "Plant", "Plant Date")
garden_bed_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    garden_bed_list.heading(col, text=col)
garden_bed_list.grid(row=12, column=0, columnspan=2)

# Update the garden bed list
update_garden_bed_list()

# Run the main loop
root.mainloop()
