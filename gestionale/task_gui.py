import tkinter as tk

from tkinter import messagebox

from tkcalendar import Calendar

import datetime
from calendario import CalendarWindow
 

class TaskWindow:

    def __init__(self, master, db, username):

        self.master = master

        self.db = db

        self.username = username

 

        self.master.title(f"Assign Task to {username}")

        self.users = self.db.get_users()

        self.user_id = self.db.check_username()

 

        # Campi di input con etichette specifiche

        self.fields = {}

 

        # Etichette per i campi

        labels = ["SO", "Nome Strumento", "Matricola", "Tipo di Riparazione", "Start Date", "Work Hours", "Attesa", "Commento Admin"]

 

        # Creazione dinamica dei campi

        for i, label in enumerate(labels):

            tk.Label(master, text=label + ":").grid(row=i, column=0)

            entry = tk.Entry(master)

            entry.grid(row=i, column=1)

            self.fields[label] = entry  # Salviamo ogni entry in un dizionario

 

        # Bottone per aprire il calendario e selezionare la data

        calendar_button = tk.Button(master, text="Select Start Date", command=self.open_calendar)

        calendar_button.grid(row=4, column=2)

 

        # Bottone per assegnare il task

        self.assign_button = tk.Button(master, text="Assign Task", command=self.assign_task)

        self.assign_button.grid(row=9, columnspan=2)

 

    def assign_task(self):

        # Recupera i dati dai campi di input

       task_data = {key: entry.get() for key, entry in self.fields.items()}

 

    # Verifica che il campo "Commento Admin" non sia vuoto

       if not task_data["Commento Admin"]:

            task_data["Commento Admin"] = "default"

    

        # Assicuriamoci che tutti i campi siano compilati

       if all(task_data.values()):

            task = str(task_data)  # Stringa per salvare il task nel database

            self.db.assign_task(self.user_id, task)  # Salva il task nel database

    

            # Recupera Work Hours dall'input

            try:

                work_hours = float(task_data["Work Hours"])  # Converte il valore Work Hours in float

            except ValueError:

                messagebox.showerror("Input Error", "Work Hours deve essere un numero.")

                return

    

            # Incrementa le ore di lavoro direttamente nella tabella `users`

            self.db.increment_work_hours(self.user_id, work_hours)

    

            # Recupera l'ID del task appena creato

            task_id = self.db.check_task_id(self.user_id)

    

            if task_id:

                start_date = self.fields["Start Date"].get()
               
    

                # Calcolo della data di fine

                end_date = self.calculate_end_date(start_date, work_hours)

    

                # Aggiorna le date di inizio e fine nel database

                self.db.set_work_dates(task_id, start_date, end_date)

    

                messagebox.showinfo("Task Assigned", f"Task assigned with {work_hours} hours to user {self.username}.")

                self.master.destroy()

            else:

                messagebox.showerror("Database Error", "Errore nella creazione del task. ID non trovato.")

       else:

            messagebox.showerror("Input Error", "Compila tutti i campi.")

    

 

    def open_calendar(self):

        task_id = self.user_id

        work_hours = self.db.get_work_hours(self.user_id)

 

        calendar_window = tk.Toplevel(self.master)

        CalendarWindow(calendar_window, self.db, task_id, work_hours, self.set_date)

 

    def set_date(self, start_date, ):

        print(f"Selected start date: {start_date}  for user: {self.user_id}")

        self.fields["Start Date"].delete(0, tk.END)

        self.fields["Start Date"].insert(0, start_date)

 

    def calculate_end_date(self, start_date, work_hours):

        if work_hours is None:

            return start_date

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

        total_hours = 0

        current_date = start_date

 

        while total_hours < work_hours:

            if current_date.weekday() != 5 and current_date.weekday() != 6:  # Non è sabato o domenica

                hours_to_add = min(7.5, work_hours - total_hours)

                total_hours += hours_to_add

 

            if total_hours < work_hours:

                current_date += datetime.timedelta(days=1)

 

        return current_date.strftime('%Y-%m-%d')

