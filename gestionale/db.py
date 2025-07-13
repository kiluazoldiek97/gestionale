import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            work_hours REAL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            comment TEXT,
            start_date TEXT,
            end_date TEXT,
            tecnico_start_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id))''')

        self.connection.commit()

    def check_login(self, username, password):
        query = "SELECT role FROM users WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def check_username(self):
        query = "SELECT id FROM users WHERE role != 'admin'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_tasks(self, user_id):

        query = "SELECT id, task, comment, start_date, tecnico_start_date, end_date FROM tasks WHERE user_id = ?"

        self.cursor.execute(query, (user_id,))

        return self.cursor.fetchall()



    def get_users(self):
        query = "SELECT id, username FROM users WHERE role != 'admin'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def assign_task(self, user_id, task):
        query = "INSERT INTO tasks (user_id, task) VALUES (?, ?)"
        self.cursor.execute(query, (user_id, task))
        self.connection.commit()

    def add_comment(self, task_id, comment):
        query = "UPDATE tasks SET comment = ? WHERE id = ?"
       
        self.cursor.execute(query, (comment, task_id))
        self.connection.commit()

    def set_end_date(self, task_id, end_date):
        
        print(f"DEBUG: task_id = {task_id}, type = {type(task_id)}")
        print(f"DEBUG: end_date = {end_date}, type = {type(end_date)}")
         
        query = "UPDATE tasks SET end_date = ? WHERE id = ?"
        self.cursor.execute(query, (end_date, task_id))
        self.connection.commit()
    def check_task_id(self,user_id):
        
        query = 'SELECT max(id) from tasks WHERE user_id = ?'
        self.cursor.execute(query,(user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    def set_work_dates(self,task_id,start_date,end_date):
        query = 'UPDATE tasks SET start_date = ?, end_date=? WHERE id = ?'
        self.cursor.execute(query,(start_date,end_date,task_id))
        self.connection.commit()
    def set_work_hours(self, user_id, work_hours):
        query ='UPDATE users SET work_hours = ? WHERE id = ?'
        self.cursor.execute(query,(user_id,work_hours))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def get_work_hours(self, user_id):
        query ='SELECT work_hours FROM users WHERE id = ?'
        self.cursor.execute(query,(user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def increment_work_hours(self,user_id,hours):
        current_hours = self.get_work_hours(user_id)
        if current_hours is  None:
            current_hours  = 0
        
        new_hours = current_hours + hours 
        self.set_work_hours(user_id, new_hours)
    def set_tecnico_start_date(self, task_id, tecnico_start_date):

        query = 'UPDATE tasks SET tecnico_start_date = ? WHERE id = ?'

        self.cursor.execute(query, (tecnico_start_date, task_id))

        self.connection.commit()
    
    """def set_start_date(self, task_id,start_date):
        query = "UPDATE tasks SET start_date = ? WHERE id = ?"
        self.cursor.execute(query, (start_date, task_id))
        self.connection.commit()"""

"""if __name__ == "__main__":
    # Test database operations
    db = Database('miodatabase.db')

    # Add test users
    db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('user1', 'password1', 'user'))
    db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin1', 'password2', 'admin'))
    db.connection.commit()

    # Test check_login function
    username = 'user1'
    password = 'password1'
    role = db.check_login(username, password)
    print(f"Role of username {username}: {role}")

    # Test get_users function
    users = db.get_users()
    print("Users (non-admin):", users)

    # Test assign_task function
    user_id = 2 
    task = "Complete the project report 4"
    db.assign_task(user_id, task)
    task_id = db.check_task_id(user_id)

    # Retrieve and print tasks for verification
    db.cursor.execute("SELECT * FROM tasks")
    tasks = db.cursor.fetchall()
    print("Tasks:", tasks)
    end_date = '2023-12-31'
    db.set_end_date(task_id,end_date)
    db.close_connection()"""