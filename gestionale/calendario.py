import tkinter as tk
from tkcalendar import Calendar
import datetime
from tkinter import messagebox
class CalendarWindow:
    def __init__(self, master, db, task_id, work_hours, callback=None):
        self.master = master
        self.db = db
        self.task_id = task_id
        self.work_hours = work_hours
        self.callback = callback
        self.master.title("Select Start Date")

        tk.Label(master, text="Select a start date from the calendar:").pack(pady=10)
        self.cal = Calendar(master, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=20)

        self.disable_weekends()

        self.select_button = tk.Button(master, text="Select Date", command=self.select_date)
        self.select_button.pack(pady=10)

    def disable_weekends(self):
        mindate = self.cal.cget("mindate")
        maxdate = self.cal.cget("maxdate")
        if maxdate is not None:
            current_date = mindate
            while current_date <= maxdate:
             if current_date.weekday() == 5 or current_date.weekday() == 6:  # 5 = sabato, 6 = domenica
                self.cal.calevent_create(current_date, 'Weekend', 'we')
                self.cal.tag_configure('we', background='gray', state='disabled')
            current_date += datetime.timedelta(days=1)
        else:
            pass

    def select_date(self):
        start_date = self.cal.get_date()
        start_date_parsed = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
        if start_date_parsed.weekday() in (5, 6):
            messagebox.showerror('ERRORE: ','NON PUOI SELEZIONARE I WEEKEND')
        end_date = self.calculate_end_date(start_date, self.work_hours)
        if self.callback:
            #self.db.set_start_date(self.task_id, start_date)
            self.callback(start_date)
        self.master.destroy()

    def calculate_end_date(self, start_date, work_hours):
        if work_hours is None:
            return start_date
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        total_hours = 0
        current_date = start_date
        
        while total_hours < work_hours:
            if current_date.weekday() != 5 and current_date.weekday() != 6:  # Non è sabato o domenica
                
                hours_to_add = min(7.5,work_hours-total_hours)
                total_hours += hours_to_add
            if total_hours < work_hours:
                current_date += datetime.timedelta(days=1)

        return current_date

"""def test_code():

    root = tk.Tk()

    db = None  # Placeholder for your database object

    task_id = 1

    work_hours = 37.5  # Example number of work hours

    calendar_window = CalendarWindow(root, db, task_id, work_hours, callback=lambda date: print(f"Selected date: {date}"))

    root.mainloop()

 

if __name__ == "__main__":

    test_code()"""

 
