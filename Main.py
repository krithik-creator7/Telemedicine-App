# Upgraded Telemedicine App with Improved GUI and Email Functionality
# Requirements: pip install mysql-connector-python pillow

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from PIL import Image, ImageTk

# ------------------- Database Setup -------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Rajitha@1',
    'database': 'telemedicines'
}

try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
except Exception as e:
    print("DB Connection Failed:", e)

# ------------------- Email Notification -------------------
def send_email(to_email, subject, message):
    try:
        from_email = "telemedicine103@gmail.com"
        from_password = "datascience123"  # Use a secure App Password from Gmail

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, from_password)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", e)

# ------------------- AI Symptom Checker -------------------
def suggest_doctor(symptom):
    symptom = symptom.lower()
    if "aches" in symptom or "chest" in symptom:
        return "Cardiologist"
    elif "pain" in symptom or "joint" in symptom:
        return "Orthopedic"
    elif "head" in symptom or "memory" in symptom:
        return "Neurologist"
    else:
        return "General Physician"

# ------------------- Tkinter UI -------------------
root = tk.Tk()
root.title("Smart Telemedicine App")
root.geometry("750x600")
root.configure(bg="#F0F8FF")

# ------------------- Helpers -------------------
def clear():
    for widget in root.winfo_children():
        widget.destroy()

def styled_button(text, command, color="blue"):
    return tk.Button(root, text=text, command=command, bg=color, fg="white", font=("Segoe UI", 10, "bold"), width=22, pady=5)

# ------------------- Login Page -------------------
def login_page():
    clear()
    tk.Label(root, text="Login", font=("Segoe UI", 22, "bold"), fg="blue", bg="#F0F8FF").pack(pady=20)

    tk.Label(root, text="Username", bg="#F0F8FF").pack()
    entry_user = tk.Entry(root)
    entry_user.pack(pady=5)

    tk.Label(root, text="Password", bg="#F0F8FF").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack(pady=5)

    role_var = tk.StringVar(value="patient")
    tk.Radiobutton(root, text="Patient", variable=role_var, value="patient", bg="#F0F8FF").pack()
    tk.Radiobutton(root, text="Doctor", variable=role_var, value="doctor", bg="#F0F8FF").pack()
    tk.Radiobutton(root, text="Admin", variable=role_var, value="admin", bg="#F0F8FF").pack()

    def authenticate():
        uname = entry_user.get()
        passwd = entry_pass.get()
        role = role_var.get()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role=%s", (uname, passwd, role))
        result = cursor.fetchone()
        if result:
            if role == 'patient':
                show_report_and_availability(uname)
            elif role == 'doctor':
                doctor_dashboard(uname)
            else:
                admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    styled_button("Login", authenticate, "green").pack(pady=20)
    styled_button("Symptom Checker", symptom_checker, "orange").pack(pady=10)

# ------------------- Symptom Checker -------------------
def symptom_checker():
    clear()
    tk.Label(root, text="AI Symptom Checker", font=("Segoe UI", 20, "bold"), fg="blue", bg="#F0F8FF").pack(pady=20)
    tk.Label(root, text="Enter your symptoms:", bg="#F0F8FF").pack()
    entry_symptom = tk.Entry(root, width=50)
    entry_symptom.pack(pady=10)

    def check():
        doc = suggest_doctor(entry_symptom.get())
        messagebox.showinfo("Suggested Specialist", f"Based on your symptom, consult a {doc}.")

    styled_button("Check", check, "blue").pack(pady=10)
    styled_button("Back", login_page, "gray").pack(pady=5)

# ------------------- Patient Dashboard -------------------
def patient_dashboard(username):
    clear()
    tk.Label(root, text=f"Welcome {username}", font=("Segoe UI", 18, "bold"), fg="green", bg="#F0F8FF").pack(pady=20)
    styled_button("Book Appointment", lambda: book_appointment(username)).pack(pady=10)
    styled_button("View Prescriptions", lambda: view_prescriptions(username)).pack(pady=10)
    styled_button("Logout", login_page, "red").pack(pady=10)

# ------------------- Book Appointment -------------------
def book_appointment(username):
    clear()
    tk.Label(root, text="Book Appointment", font=("Segoe UI", 18, "bold"), fg="blue", bg="#F0F8FF").pack(pady=20)

    cursor.execute("SELECT name, specialization FROM users WHERE role='doctor'")
    doctors = cursor.fetchall()

    selected_doctor = tk.StringVar()
    for name, spec in doctors:
        tk.Radiobutton(root, text=f"Dr. {name} - {spec}", variable=selected_doctor, value=name, bg="#F0F8FF").pack(anchor="w")

    tk.Label(root, text="Choose Time Slot", bg="#F0F8FF").pack(pady=10)
    time_slot = tk.StringVar(value="10:00 AM")
    for t in ["10:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"]:
        tk.Radiobutton(root, text=t, variable=time_slot, value=t, bg="#F0F8FF").pack(anchor="w")

    def confirm():
        cursor.execute("INSERT INTO appointments(patient, doctor, time) VALUES(%s, %s, %s)",
                       (username, selected_doctor.get(), time_slot.get()))
        db.commit()
        messagebox.showinfo("Booked", "Appointment Confirmed")
        send_email("telemedicine103@gmail.com", "Appointment Confirmation", f"Appointment booked with Dr. {selected_doctor.get()} at {time_slot.get()}.")
        patient_dashboard(username)

    styled_button("Confirm", confirm, "green").pack(pady=20)
    styled_button("Back", lambda: patient_dashboard(username)).pack()

# ------------------- View Prescriptions -------------------
def view_prescriptions(username):
    clear()
    tk.Label(root, text="Your Prescriptions", font=("Segoe UI", 18, "bold"), fg="blue", bg="#F0F8FF").pack(pady=20)

    cursor.execute("SELECT doctor, note FROM prescriptions WHERE patient=%s", (username,))
    rows = cursor.fetchall()
    if rows:
        for doc, note in rows:
            tk.Label(root, text=f"Dr. {doc}: {note}", wraplength=500, bg="#F0F8FF").pack(pady=5)
    else:
        tk.Label(root, text="No prescriptions found.", bg="#F0F8FF").pack()

    styled_button("Back", lambda: patient_dashboard(username)).pack(pady=20)

# ------------------- Doctor/Admin Dashboards -------------------
def doctor_dashboard(username):
    clear()
    tk.Label(root, text=f"Doctor {username} Dashboard", font=("Segoe UI", 18, "bold"), fg="blue", bg="#F0F8FF").pack(pady=20)

    tk.Label(root, text="Write Prescription (Patient, Note):", bg="#F0F8FF").pack()
    entry_patient = tk.Entry(root)
    entry_patient.pack()
    entry_note = tk.Entry(root, width=50)
    entry_note.pack(pady=5)

    def submit_prescription():
        cursor.execute("INSERT INTO prescriptions(patient, doctor, note) VALUES(%s, %s, %s)",
                       (entry_patient.get(), username, entry_note.get()))
        db.commit()
        messagebox.showinfo("Done", "Prescription Added")

    styled_button("Submit", submit_prescription, "green").pack(pady=10)
    styled_button("Logout", login_page).pack(pady=20)

def admin_dashboard():
    clear()
    tk.Label(root, text="Admin Dashboard (Read-only)", font=("Segoe UI", 18, "bold"), fg="red", bg="#F0F8FF").pack(pady=20)

    cursor.execute("SELECT * FROM appointments")
    for row in cursor.fetchall():
        tk.Label(root, text=str(row), bg="#F0F8FF").pack()

    styled_button("Logout", login_page).pack(pady=20)

# ------------------- Patient Info -------------------
def show_report_and_availability(username):
    clear()
    tk.Label(root, text=f"\U0001F469‍⚕️ Patient Report for {username}", font=("Georgia", 20, "bold"), fg="darkblue", bg="#F0F8FF").pack(pady=10)

    cursor.execute("SELECT name, mobile, age, problem, last_visit FROM patients WHERE username = %s", (username,))
    details = cursor.fetchone()

    if details:
        name, mobile, age, problem, last_visit = details

        report_frame = tk.Frame(root, bg="#EAF6F6", bd=2, relief="groove", padx=20, pady=10)
        report_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(report_frame, text=f"🧍 Name: {name}", font=("Arial", 12, "bold"), bg="#EAF6F6").pack(anchor="w")
        tk.Label(report_frame, text=f"📱 Mobile: {mobile}", font=("Arial", 12), bg="#EAF6F6").pack(anchor="w")
        tk.Label(report_frame, text=f"🎂 Age: {age}", font=("Arial", 12), bg="#EAF6F6").pack(anchor="w")
        tk.Label(report_frame, text=f"🩺 Current Issue: {problem}", font=("Arial", 12), bg="#EAF6F6", wraplength=600).pack(anchor="w", pady=5)
        tk.Label(report_frame, text=f"📅 Last Visit: {last_visit}", font=("Arial", 12), bg="#EAF6F6").pack(anchor="w")

    tk.Label(root, text="📄 Prescriptions", font=("Arial", 14, "bold"), fg="green", bg="#F0F8FF").pack(pady=10)
    cursor.execute("SELECT doctor, note FROM prescriptions WHERE patient=%s", (username,))
    prescriptions = cursor.fetchall()
    if prescriptions:
        for doc, note in prescriptions:
            tk.Label(root, text=f"💊 Dr. {doc}: {note}", font=("Arial", 11), wraplength=600, bg="#F0F8FF").pack(anchor="w", padx=40, pady=2)
    else:
        tk.Label(root, text="No prescriptions found.", fg="red", font=("Arial", 11), bg="#F0F8FF").pack()

    tk.Label(root, text="\n✅ Doctors Available for Online Consultation", font=("Arial", 14, "bold"), fg="darkgreen", bg="#F0F8FF").pack(pady=10)
    cursor.execute("SELECT name, specialization FROM users WHERE role='doctor'")
    doctors = cursor.fetchall()
    if doctors:
        for name, spec in doctors:
            tk.Label(root, text=f"🩻 Dr. {name} ({spec})", font=("Arial", 11), bg="#F0F8FF").pack(anchor="w", padx=40)
    else:
        tk.Label(root, text="No doctors currently online.", fg="red", bg="#F0F8FF").pack()

    styled_button("➡ Proceed to Dashboard", lambda: patient_dashboard(username), "orange").pack(pady=20)

# ------------------- App Start -------------------
login_page()
root.mainloop()
