import tkinter as tk
from db import Database
from login import LoginWindow
def main():
    db = Database('miodatabase.db')

    # Aggiungi pochi utenti di prova (commenta se già esistono)
    db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', '123456', 'admin'))
    db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('user1', 'password1', 'user'))
    db.connection.commit()

    root = tk.Tk()
    login_window = LoginWindow(root, db)
  
    root.mainloop()
    
    db.close_connection()


if __name__ == "__main__":
    main()

