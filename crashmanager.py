import tkinter as tk
import os
import json
from sessiondao import SessionDAO
from session import Session
from tkinter import messagebox

sessiondao = SessionDAO()
class CrashManager:
    def __init__(self):
        self.create_crash_file_if_not_exists()

    
    def check_for_crash(self):
        if self.has_crash_data():
            session = self.crash_to_session()
            if self.ask_user_to_log_session(session):
                sessiondao.insert_session(session)
            self.clear_crash_file()



    def has_crash_data(self):
        with open("crash.json", "r") as crash:
            if crash.read():
                return True
            return False

    def create_crash_file_if_not_exists(self):
        if not os.path.exists("crash.json"):
            open("crash.json", "x").close()


    def crash_to_session(self):
        with open("crash.json", "r") as crash:
            data = crash.readlines()[0]
            data = json.loads(data)
            task = data["task"]
            task_time = data["task_time"]
            time_started = data["time_started"]
            date_started = data["date_started"]
            session = Session(task=task, task_time=task_time, time_started=time_started, date_started=date_started)
            return session
    

    def ask_user_to_log_session(self, session):
        message = f"An unsaved session was found. Would you like to log it?\nTask: {session.task} \nTask time: {self.format_task_time(session.task_time)} \nTime started: {session.time_started} \nDate: {session.date_started}"
        return messagebox.askyesno("Unsaved data found", message)

    def update_crash_file(self, session):
        json_data = self.session_to_json(session)
        with open('crash.json', 'w') as crash:
            crash.write(json_data)


    def session_to_json(self, session):
        data = {'task': session.task, 'task_time': session.task_time, 'time_started': session.time_started, 'date_started': session.date_started}
        return json.dumps(data)

    
    def clear_crash_file(self):
        open("crash.json", "w").close()

    def format_task_time(self, seconds):
        h, s = divmod(seconds, 3600)
        m, s = divmod(s, 60)
        string = f"{h:02}:{m:02}:{s:02}"
        return string