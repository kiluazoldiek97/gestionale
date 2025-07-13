import sqlite3

class MockDatabase:
    def __init__(self):
        # Creiamo un database in memoria per il test
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.setup_table()

    def setup_table(self):
        # Creiamo una tabella `tasks` con colonne `id` e `end_date`
        self.cursor.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, end_date TEXT)")
        self.cursor.execute("INSERT INTO tasks (id, end_date) VALUES (1, '2025-01-01')")
        self.connection.commit()

    def set_end_date(self, task_id, end_date):
        print(f"DEBUG: task_id = {task_id}, type = {type(task_id)}")
        print(f"DEBUG: end_date = {end_date}, type = {type(end_date)}")

        try:
            query = "UPDATE tasks SET end_date = ? WHERE id = ?"
            self.cursor.execute(query, (end_date, task_id))
            self.connection.commit()
            print("Aggiornamento riuscito!")
        except sqlite3.ProgrammingError as e:
            print(f"ERRORE: {e}")

# Test della funzione
db = MockDatabase()

# Caso corretto: ID numerico, data stringa
print("\n🔹 Test 1: Valori corretti")
db.set_end_date(1, "2025-03-21")

# Caso errore: task_id è un metodo invece di un valore
print("\n🔹 Test 2: task_id è un metodo (simulato)")
db.set_end_date(db.set_end_date, "2025-03-21")

# Caso errore: end_date è None
print("\n🔹 Test 3: end_date è None")
db.set_end_date(1, None)

# Caso errore: task_id non è un numero
print("\n🔹 Test 4: task_id non è un numero")
db.set_end_date("abc", "2025-03-21")