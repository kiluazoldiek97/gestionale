import tkinter as tk
from tkinter import messagebox
import sqlite3
from task_gui import TaskWindow
from db import Database
from calendario import CalendarWindow
class AdminWindow:
    
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Admin Panel")

        self.users = self.db.get_users()
        
        tk.Label(master, text="Click on a user to assign a task or set dates").grid(row=0, columnspan=2)
        
        for i,(user_id,username) in enumerate(self.users):
            tk.Button(master, text=username, command=lambda u=user_id, un=username: self.open_task_window(u,un)).grid(row=i+1, column=0)
            #tk.Button(master,text="set dates", command=lambda u=user_id: self.open_calendar(u)).grid(row =i+1,column=1)

    def open_task_window(self, user_id, username):
            task_window = tk.Toplevel(self.master)
            TaskWindow(task_window, self.db, username)
   
   
   
   
   
   
    """def open_calendar(self,user_id):
        task_id = self.db.check_task_id(user_id)
        if task_id:
            work_hours =  self.db.get_work_hours(user_id)
            calendar_window = tk.Toplevel(self.master)
            CalendarWindow(calendar_window,self.db,task_id,work_hours,lambda start_date:self.set_date(task_id,start_date))
    def set_date(self,task_id,start_date):
        print(f"Selected start date:{start_date} for task id:{task_id}")
        self.db.set_start_date(task_id,start_date) """
        
"""if __name__ == "__main__":
    db = Database('test_database.db')

        # Aggiungiamo utenti di prova al database
    db.cursor.execute("INSERT INTO users (username, role) VALUES (?, ?)", ('user1', 'user'))
    db.cursor.execute("INSERT INTO users (username, role) VALUES (?, ?)", ('user2', 'user'))
    db.cursor.execute("INSERT INTO users (username, role) VALUES (?, ?)", ('admin1', 'admin'))
    db.connection.commit()

        # Inizializziamo la finestra principale di Tkinter
    root = tk.Tk()
    admin_window = AdminWindow(root, db)

        # Avviamo il ciclo principale di Tkinter
    root.mainloop()

        # Chiudiamo la connessione al database
    db.close_connection()"""