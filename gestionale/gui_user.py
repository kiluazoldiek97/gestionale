import tkinter as tk

from tkinter import messagebox

import sqlite3

import datetime

class UserWindow:

    def __init__(self, master, db):

        self.master = master

        self.db = db

        self.master.title("User Panel")

 

        # Entry per inserire username

        tk.Label(master, text="Enter Username:").grid(row=0, column=0)

        self.username_entry = tk.Entry(master)

        self.username_entry.grid(row=0, column=1)

 

        # Button per effettuare il login

        self.login_button = tk.Button(master, text="Login", command=self.login)

        self.login_button.grid(row=1, columnspan=2)

 

    def login(self):

        username = self.username_entry.get()

        user_id = self.db.check_username()

        if user_id is not None:

            self.user_id = user_id

            self.show_tasks()

        else:

            messagebox.showerror("Login failed", "Invalid Username.")

   

    def show_tasks(self):

        # Rimuove i widget di login

        for widget in self.master.winfo_children():

            widget.grid_forget()

 

        # Recupera i task dal database

        self.tasks = self.db.get_tasks(self.user_id)

       

        tk.Label(self.master, text="Your Tasks:").grid(row=0, columnspan=2)

       

        self.task_listbox = tk.Listbox(self.master, height=10, width=290)

        self.task_listbox.grid(row=1, column=0, columnspan=2)

        self.update_task_listbox()

 

       
       

        tk.Label(self.master, text="Tecnico Start Date (YYYY-MM-DD):").grid(row=3, column=0)

        self.tecnico_start_date_entry = tk.Entry(self.master)

        self.tecnico_start_date_entry.grid(row=3, column=1)

       

        tk.Label(self.master, text="Commento Tecnico:").grid(row=4, column=0)

        self.comment_entry = tk.Entry(self.master)

        self.comment_entry.grid(row=4, column=1)

 

        tk.Label(self.master, text="End Date (YYYY-MM-DD):").grid(row=5, column=0)

        self.end_date_entry = tk.Entry(self.master)

        self.end_date_entry.grid(row=5, column=1)

 

        self.update_button = tk.Button(self.master, text="Update Task", command=self.update_task)

        self.update_button.grid(row=6, columnspan=2)

 

    def update_task_listbox(self):

        self.task_listbox.delete(0, tk.END)

        for task in self.tasks:

            self.task_listbox.insert(tk.END, f"Task ID: {task[0]}, Task: {task[1]}, Commento Tecnico: {task[2]}, Start Date: {task[3]}, Tecnico Start Date: {task[4]}, End Date: {task[5]}")

   

    def update_task(self):

        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:

            task_id = self.tasks[selected_task_index[0]][0]

            tecnico_start_date = self.tecnico_start_date_entry.get()

            comment = self.comment_entry.get()

            end_date = self.end_date_entry.get()

    

            # Controllo che la tecnico_start_date e end_date non siano di sabato o domenica

            dates = [tecnico_start_date, end_date]

            for date_str in dates:

                if date_str:

                    try:

                        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                        if date_obj.weekday() in {5, 6}:  # 5 = Sabato, 6 = Domenica

                            messagebox.showerror("Date Error", f"The date {date_str} falls on a weekend. Please choose another date.")

                            return

                    except ValueError:

                        messagebox.showerror("Date Error", f"The date {date_str} is invalid. Please use the format YYYY-MM-DD.")

                        return

    

            if tecnico_start_date:

                try:

                    self.db.set_tecnico_start_date(task_id, tecnico_start_date)

                except sqlite3.IntegrityError:

                    messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")

                    return

    

            if comment:

                self.db.add_comment(task_id, comment)

            if end_date:

                try:

                    self.db.set_end_date(task_id, end_date)

                except sqlite3.IntegrityError:

                    messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")

                    return

            messagebox.showinfo("Update Successful", "Task updated successfully.")

            self.tasks = self.db.get_tasks(self.user_id)

            self.update_task_listbox()

        else:

            messagebox.showerror("Selection Error", "Please select a task.")

