import tkinter as tk
from tkinter import messagebox
from gui_admin import AdminWindow
from gui_user import UserWindow
from db import Database
from calendario import CalendarWindow

class LoginWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        
        self.master.title("Login")
        
        tk.Label(master, text="Username:").grid(row=0, column=0)
        tk.Label(master, text="Password:").grid(row=1, column=0)

        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show='*')

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        role = self.db.check_login(username, password)
        if role == "admin":
            self.master.withdraw()
            root = tk.Toplevel(self.master)
            AdminWindow(root, self.db)
            root.protocol("WM_DELETE_WINDOW",lambda:self.on_close(root))
        elif role == "user":
            self.master.withdraw()
            root = tk.Toplevel(self.master)
            UserWindow(root, self.db)
            root.protocol("WM_DELETE_WINDOW",lambda:self.on_close(root))
        else:
            messagebox.showerror("Login failed", "Invalid Username or Password.")
    def on_close(self,root):
        root.destroy()
        self.master.deiconify()


"""if __name__ == "__main__":
    db = Database('test_database.db')

        # Aggiungiamo utenti di prova al database
    db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('user1', 'password1', 'user'))
    db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin1', 'password2', 'admin'))
    db.connection.commit()

    root = tk.Tk()
    login_window = LoginWindow(root, db)
    root.mainloop()

    db.close_connection()"""

   
        