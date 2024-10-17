import pymysql
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# Database connection using pymysql
def connect_db():
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="root0417",  # Replace with your MySQL password
            database="airline_scheduling"  # Ensure the correct database name
        )
        return db
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None

# Function to convert HH:MM AM/PM to HH:MM:SS for MySQL
def convert_to_24_hour_format(time_str):
    try:
        return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M:%S")
    except ValueError:
        return None

# Function to validate time format
def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%I:%M %p")  # Check HH:MM AM/PM format
        return True
    except ValueError:
        return False

# Function to reset all input fields
def reset_fields():
    flight_number_entry.delete(0, END)
    origin_entry.delete(0, END)
    destination_entry.delete(0, END)
    departure_time_entry.delete(0, END)
    arrival_time_entry.delete(0, END)
    flight_id_entry.delete(0, END)
    description_entry.delete(0, END)
    weight_entry.delete(0, END)
    flights_list.delete(0, END)
    cargo_list.delete(0, END)

# Function to submit flight details
def submit_flight():
    flight_number = flight_number_entry.get()
    origin = origin_entry.get()
    destination = destination_entry.get()
    departure_time = departure_time_entry.get()
    arrival_time = arrival_time_entry.get()

    if all([flight_number, origin, destination, departure_time, arrival_time]):
        departure_time_24 = convert_to_24_hour_format(departure_time)
        arrival_time_24 = convert_to_24_hour_format(arrival_time)

        if departure_time_24 and arrival_time_24:
            db = connect_db()
            if db is not None:
                cursor = db.cursor()
                sql = "INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time) VALUES (%s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (flight_number, origin, destination, departure_time_24, arrival_time_24))
                    db.commit()
                    messagebox.showinfo("Success", "Flight added successfully")
                    view_flights()  # Refresh the flight list
                except pymysql.MySQLError as e:
                    db.rollback()
                    messagebox.showerror("Error", f"Failed to add flight: {e}")
                finally:
                    cursor.close()
                    db.close()
        else:
            messagebox.showwarning("Warning", "Please enter valid time in HH:MM AM/PM format.")
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to view flights
def view_flights():
    db = connect_db()
    if db is not None:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()
        flights_list.delete(0, END)  # Clear the listbox
        for flight in flights:
            flights_list.insert(END, f"{flight[0]}: {flight[1]} to {flight[2]} departs at {flight[3]} and arrives at {flight[4]}")
        cursor.close()
        db.close()

# Function to delete a flight using Flight Number
def delete_flight():
    flight_number = flight_number_entry.get()

    if flight_number:
        db = connect_db()
        if db is not None:
            cursor = db.cursor()
            sql = "DELETE FROM flights WHERE flight_number = %s"
            try:
                cursor.execute(sql, (flight_number,))
                db.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Flight deleted successfully")
                else:
                    messagebox.showwarning("Warning", "No flight found with that number.")
                view_flights()  # Refresh the flight list
            except pymysql.MySQLError as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to delete flight: {e}")
            finally:
                cursor.close()
                db.close()
    else:
        messagebox.showwarning("Warning", "Please enter a Flight Number to delete.")

# Function to submit cargo details
def submit_cargo():
    flight_id = flight_id_entry.get()
    description = description_entry.get()
    weight = weight_entry.get()

    if flight_id and description and weight:
        db = connect_db()
        if db is not None:
            cursor = db.cursor()
            sql = "INSERT INTO cargo (flight_id, description, weight) VALUES (%s, %s, %s)"
            try:
                cursor.execute(sql, (flight_id, description, weight))
                db.commit()
                messagebox.showinfo("Success", "Cargo added successfully")
                view_cargo()  # Refresh the cargo list
            except pymysql.MySQLError as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to add cargo: {e}")
            finally:
                cursor.close()
                db.close()
        else:
            messagebox.showerror("Error", "Database connection failed")
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to view cargo
def view_cargo():
    db = connect_db()
    if db is not None:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cargo")
        cargo = cursor.fetchall()
        cargo_list.delete(0, END)  # Clear the listbox
        for item in cargo:
            cargo_list.insert(END, f"{item[0]}: Flight ID {item[1]}, {item[2]}, Weight: {item[3]} kg")
        cursor.close()
        db.close()

# Function to delete cargo using Flight ID
def delete_cargo():
    flight_id = flight_id_entry.get()

    if flight_id:
        db = connect_db()
        if db is not None:
            cursor = db.cursor()
            sql = "DELETE FROM cargo WHERE flight_id = %s"
            try:
                cursor.execute(sql, (flight_id,))
                db.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Cargo deleted successfully")
                else:
                    messagebox.showwarning("Warning", "No cargo found with that Flight ID.")
                view_cargo()  # Refresh the cargo list
            except pymysql.MySQLError as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to delete cargo: {e}")
            finally:
                cursor.close()
                db.close()
    else:
        messagebox.showwarning("Warning", "Please enter a Flight ID to delete.")

# Setting up the main window
root = Tk()
root.title("Airline Scheduling System")
root.state("zoomed")  # Maximize the window
root.configure(bg="blue")

# Create a PanedWindow to divide the window into two vertical sections
pane = PanedWindow(root, orient=HORIZONTAL, sashwidth=5, bg="blue")
pane.pack(fill=BOTH, expand=1, pady=20, padx=20)

# Flight Input Frame (Left Section)
flight_frame = Frame(pane, bg="lightblue", padx=10, pady=10)
pane.add(flight_frame, stretch="always")

Label(flight_frame, text="Flight Number:", bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
flight_number_entry = Entry(flight_frame)
flight_number_entry.grid(row=0, column=1, padx=5, pady=5)

Label(flight_frame, text="Origin:", bg="lightblue").grid(row=1, column=0, padx=5, pady=5)
origin_entry = Entry(flight_frame)
origin_entry.grid(row=1, column=1, padx=5, pady=5)

Label(flight_frame, text="Destination:", bg="lightblue").grid(row=2, column=0, padx=5, pady=5)
destination_entry = Entry(flight_frame)
destination_entry.grid(row=2, column=1, padx=5, pady=5)

Label(flight_frame, text="Departure Time (HH:MM AM/PM):", bg="lightblue").grid(row=3, column=0, padx=5, pady=5)
departure_time_entry = Entry(flight_frame)
departure_time_entry.grid(row=3, column=1, padx=5, pady=5)

Label(flight_frame, text="Arrival Time (HH:MM AM/PM):", bg="lightblue").grid(row=4, column=0, padx=5, pady=5)
arrival_time_entry = Entry(flight_frame)
arrival_time_entry.grid(row=4, column=1, padx=5, pady=5)

Button(flight_frame, text="Add Flight", command=submit_flight).grid(row=5, column=0, padx=5, pady=5)
Button(flight_frame, text="Delete Flight", command=delete_flight).grid(row=5, column=1, padx=5, pady=5)
Button(flight_frame, text="View Flights", command=view_flights).grid(row=5, column=2, padx=5, pady=5)
flights_list = Listbox(flight_frame, height=10, width=50)
flights_list.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Cargo Input Frame (Right Section)
cargo_frame = Frame(pane, bg="lightblue", padx=10, pady=10)
pane.add(cargo_frame, stretch="always")

Label(cargo_frame, text="Flight ID:", bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
flight_id_entry = Entry(cargo_frame)
flight_id_entry.grid(row=0, column=1, padx=5, pady=5)

Label(cargo_frame, text="Description:", bg="lightblue").grid(row=1, column=0, padx=5, pady=5)
description_entry = Entry(cargo_frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

Label(cargo_frame, text="Weight (kg):", bg="lightblue").grid(row=2, column=0, padx=5, pady=5)
weight_entry = Entry(cargo_frame)
weight_entry.grid(row=2, column=1, padx=5, pady=5)

Button(cargo_frame, text="Add Cargo", command=submit_cargo).grid(row=3, column=0, padx=5, pady=5)
Button(cargo_frame, text="Delete Cargo", command=delete_cargo).grid(row=3, column=1, padx=5, pady=5)
Button(cargo_frame, text="View Cargo", command=view_cargo).grid(row=3, column=2, padx=5, pady=5)
cargo_list = Listbox(cargo_frame, height=10, width=50)
cargo_list.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Reset button
reset_button = Button(root, text="Reset All Fields", command=reset_fields)
reset_button.pack(pady=10)

root.mainloop()
