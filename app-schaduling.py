# this program works for handling appointments in health center and it is interactive between the patient and doctor
#made by 
# mieraf abebe   dbu1501366
# lidiya shenkut   dbu1501322
#tsedeniya yeshibelay  dbu1501513


import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

PATIENT_FILE = "patients.json"
DOCTOR_FILE = "doctors.json"
APPOINTMENT_FILE = "appointments.json"

class HealthCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Health Center Appointment System")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.current_user = None
        self.current_doctor = None
        self.current_patient = None

        self.load_patients()
        self.load_doctors()
        self.load_appointments()

        self.setup_login_screen()

    def setup_login_screen(self):
        self.clear_screen()

        tk.Label(self, text="Health Center Appointment System", font=("Helvetica", 20), bg="#f0f0f0").pack(pady=20)

        form_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(form_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Login as Patient", command=self.login_patient, width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Login as Doctor", command=self.login_doctor, width=15).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Register as Patient", command=self.register_patient, width=15).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Register as Doctor", command=self.register_doctor, width=15).grid(row=0, column=3, padx=10)

    def login_patient(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        for patient in self.patients:
            if patient['username'] == username and patient['password'] == password:
                self.current_user = "patient"
                self.current_patient = patient
                self.setup_patient_dashboard()
                return

        messagebox.showerror("Error", "Invalid username or password")

    def login_doctor(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for doctor in self.doctors:
            if doctor['username'] == username and doctor['password'] == password:
                self.current_user = "doctor"
                self.current_doctor = doctor
                self.setup_doctor_dashboard()
                return

        messagebox.showerror("Error", "Invalid username or password")

    def register_patient(self):
        self.clear_screen()

        tk.Label(self, text="Patient Registration", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        form_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.register_username_entry = tk.Entry(form_frame)
        self.register_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.register_password_entry = tk.Entry(form_frame, show='*')
        self.register_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Name", bg="#ffffff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.register_name_entry = tk.Entry(form_frame)
        self.register_name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Age", bg="#ffffff").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.register_age_entry = tk.Entry(form_frame)
        self.register_age_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Address", bg="#ffffff").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.register_address_entry = tk.Entry(form_frame)
        self.register_address_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Phone Number", bg="#ffffff").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.register_phone_entry = tk.Entry(form_frame)
        self.register_phone_entry.grid(row=5, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Register", command=self.save_patient, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back", command=self.setup_login_screen, width=15).pack(side="left", padx=10)

    def save_patient(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        name = self.register_name_entry.get()
        age = self.register_age_entry.get()
        address = self.register_address_entry.get()
        phone = self.register_phone_entry.get()

        # Basic validation for required fields
        if not (username and password and name and age and address and phone):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        new_patient = {
            'username': username,
            'password': password,
            'name': name,
            'age': age,
            'address': address,
            'phone': phone
        }

        self.patients.append(new_patient)
        self.save_patients_to_file()

        messagebox.showinfo("Success", "Patient registered successfully!")
        self.setup_login_screen()
    def register_doctor(self):
        self.clear_screen()

        tk.Label(self, text="Doctor Registration", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        form_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.register_username_entry = tk.Entry(form_frame)
        self.register_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.register_password_entry = tk.Entry(form_frame, show='*')
        self.register_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Specialty", bg="#ffffff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.register_specialty_entry = tk.Entry(form_frame)
        self.register_specialty_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email", bg="#ffffff").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.register_email_entry = tk.Entry(form_frame)
        self.register_email_entry.grid(row=3, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Register", command=self.save_doctor, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back", command=self.setup_login_screen, width=15).pack(side="left", padx=10)

    def save_doctor(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        specialty = self.register_specialty_entry.get()
        email = self.register_email_entry.get()

        # Basic validation for required fields
        if not (username and password and specialty and email):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        new_doctor = {
            'username': username,
            'password': password,
            'specialty': specialty,
            'email': email
        }

        self.doctors.append(new_doctor)
        self.save_doctors_to_file()

        messagebox.showinfo("Success", "Doctor registered successfully!")
        self.setup_login_screen()

    def setup_patient_dashboard(self):
        self.clear_screen()

        tk.Label(self, text=f"Welcome, {self.current_patient['name']}", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)
        tk.Button(self, text="Book Appointment", command=self.book_appointment_screen, width=30).pack(pady=10)
        tk.Button(self, text="View My Appointments", command=self.view_my_appointments, width=30).pack(pady=10)
        tk.Button(self, text="Logout", command=self.setup_login_screen, width=15).pack(pady=10)

    def book_appointment_screen(self):
        self.clear_screen()

        tk.Label(self, text="Book Appointment", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        form_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Doctor", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.doctor_var = tk.StringVar(form_frame)
        self.doctor_menu = tk.OptionMenu(form_frame, self.doctor_var, *[doctor['username'] for doctor in self.doctors])
        self.doctor_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Time (HH:MM)", bg="#ffffff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.time_entry = tk.Entry(form_frame)
        self.time_entry.grid(row=2, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Book", command=self.book_appointment, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back", command=self.setup_patient_dashboard, width=15).pack(side="left", padx=10)

    def book_appointment(self):
        doctor_username = self.doctor_var.get()
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()

        try:
            appointment_date = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return

        new_appointment = {
            'patient_username': self.current_patient['username'],
            'doctor_username': doctor_username,
            'date': date_str,
            'time': time_str,
            'status': 'Pending'  # Default status for new appointments
        }

        self.appointments.append(new_appointment)
        self.save_appointments_to_file()

        messagebox.showinfo("Success", "Appointment booked successfully!")
        self.setup_patient_dashboard()

    def view_my_appointments(self):
        self.clear_screen()

        tk.Label(self, text="My Appointments", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        for appointment in self.appointments:
            if appointment['patient_username'] == self.current_patient['username']:
                tk.Label(self, text=f"Doctor: {appointment['doctor_username']}, Date: {appointment['date']}, Time: {appointment['time']}, Status: {appointment['status']}", bg="#f0f0f0").pack(pady=5)

        tk.Button(self, text="Back", command=self.setup_patient_dashboard, width=15).pack(pady=10)

    def setup_doctor_dashboard(self):
        self.clear_screen()

        tk.Label(self, text=f"Welcome, Dr. {self.current_doctor['username']}", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)
        tk.Button(self, text="View Appointments", command=self.view_appointments, width=30).pack(pady=10)
        tk.Button(self, text="Logout", command=self.setup_login_screen, width=15).pack(pady=10)

    def view_appointments(self):
        self.clear_screen()

        tk.Label(self, text="Appointments", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        for appointment in self.appointments:
            if appointment['doctor_username'] == self.current_doctor['username']:
                appointment_frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
                appointment_frame.pack(pady=10, padx=10, fill=tk.X)

                tk.Label(appointment_frame, text=f"Patient: {appointment['patient_username']}, Date: {appointment['date']}, Time: {appointment['time']}, Status: {appointment['status']}", bg="#ffffff").pack(side=tk.LEFT)

                approve_button = tk.Button(appointment_frame, text="Approve", command=lambda app=appointment: self.approve_appointment(app), width=10, bg="#4CAF50", fg="white")
                approve_button.pack(side=tk.LEFT, padx=10)

                disapprove_button = tk.Button(appointment_frame, text="Disapprove", command=lambda app=appointment: self.disapprove_appointment(app), width=10, bg="#FF5733", fg="white")
                disapprove_button.pack(side=tk.LEFT, padx=10)

        tk.Button(self, text="Back", command=self.setup_doctor_dashboard, width=15).pack(pady=10)

    def approve_appointment(self, appointment):
        appointment['status'] = 'Approved'
        self.save_appointments_to_file()
        messagebox.showinfo("Success", "Appointment approved!")
        self.view_appointments()

    def disapprove_appointment(self, appointment):
        appointment['status'] = 'Disapproved'
        self.save_appointments_to_file()
        messagebox.showinfo("Success", "Appointment disapproved!")
        self.view_appointments()

    def load_patients(self):
        try:
            with open(PATIENT_FILE, 'r') as file:
                self.patients = json.load(file)
        except FileNotFoundError:
            self.patients = []

    def save_patients_to_file(self):
        with open(PATIENT_FILE, 'w') as file:
            json.dump(self.patients, file, indent=4)

    def load_doctors(self):
        try:
            with open(DOCTOR_FILE, 'r') as file:
                self.doctors = json.load(file)
        except FileNotFoundError:
            self.doctors = []

    def save_doctors_to_file(self):
        with open(DOCTOR_FILE, 'w') as file:
            json.dump(self.doctors, file, indent=4)

    def load_appointments(self):
        try:
            with open('appointments.json', 'r') as file:
                self.appointments = json.load(file)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            print("Appointments file not found. Creating new empty list.")
            self.appointments = []
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            print(f"Error decoding JSON: {e}")
            self.appointments = []

    def save_appointments_to_file(self):
        with open(APPOINTMENT_FILE, 'w') as file:
            json.dump(self.appointments, file, indent=4)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = HealthCenterApp()
    app.mainloop()
