from tkinter import *
from booterwidgets import *
from taskdao import TaskDAO
from sessiondao import SessionDAO
import datetime as dt
from datetime import date
from tkcalendar import *
from session import Session

taskdao = TaskDAO()
sessiondao = SessionDAO()


# TODO:
# - Where i left off: finish creating a Session object when check is clicked
# - working on input validation; preliminary checks are gucci
# - Don't focus main window when messagebox error pops up???
# - make add window not resizable
# - actually save the session that is entered
# - functionality to delete sessions (to fix errors and stuff)


class AddSession(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.controller = controller

		self.init_back_btn()

		self.frame_main = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_input = Frame(self.frame_main, bg=storedsettings.APP_MAIN_COLOR)		
		self.frame_task_time = Frame(self.frame_input, bg=storedsettings.APP_MAIN_COLOR)		
		self.frame_time_completed = Frame(self.frame_input, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_main.grid(row=0, column=1)
		self.frame_input.grid(row=0, column=1)
		self.frame_task_time.grid(row=1, column=1)
		self.frame_time_completed.grid(row=2, column=1)

		self.widgets = {"optionmenu": None,
					    "task_time": None,
					    "time_completed": None,
					    "date_completed": None}
		self.labels = {"task": None,
					   "task_time": None,
					   "time_completed": None,
					   "date_completed": None}
		self.e_hour = None
		self.e_min = None
		self.e_sec = None

		self.after_job = None

		self.draw_window()


	def draw_window(self):
		self.init_task_optionmenu()

		self.init_task_time_row()
		self.init_time_completed_row()
		self.init_date_completed()

		self.lbl_status = BooterLabel(self, text="")
		self.lbl_status.config(font=(storedsettings.FONT, 15, "bold"), fg="green")
		btn_log = BooterButton(self, text="Log", command=self.check_clicked)

		
		self.lbl_status.grid(row=2, column=1)
		btn_log.grid(row=3, column=1)

		self.refresh_option_menu()	


	def init_back_btn(self):
		btn_back = BooterButton(self, command=lambda: print("TODO: back clicked"))
		btn_back.apply_back_image()
		btn_back.grid(row=0, column=0, sticky="n")


	def init_task_optionmenu(self):
		lbl = BooterLabel(self.frame_input, text="Task")
		om_var = StringVar()
		om_var.set("Select...")
		om = BooterOptionMenu(self.frame_input, om_var, None)
		widgets = {"om_var": om_var,
				   "om": om}
		self.labels["task"] = lbl
		self.widgets["optionmenu"] = widgets
		lbl.grid(row=0, column=0)
		om.grid(row=0, column=1)


	def init_task_time_row(self):
		WIDTH = 4
		lbl = BooterLabel(self.frame_input, text="Task Time")
		e_hour = BooterEntry(self.frame_task_time, width=WIDTH)
		e_min = BooterEntry(self.frame_task_time, width=WIDTH)
		e_sec = BooterEntry(self.frame_task_time, width=WIDTH)

		widgets = {"e_hour": e_hour,
				   "e_min": e_min,
				   "e_sec": e_sec}
		self.labels["task_time"] = lbl
		self.widgets["task_time"] = widgets

		lbl.grid(row=1, column=0)
		e_hour.grid(row=0, column=0)
		BooterLabel(self.frame_task_time, text=":").grid(row=0, column=1)
		e_min.grid(row=0, column=2)
		BooterLabel(self.frame_task_time, text=":").grid(row=0, column=3)
		e_sec.grid(row=0, column=4)

	def init_time_completed_row(self):
		WIDTH = 4
		lbl = BooterLabel(self.frame_input, text="Time Completed")
		e_hour = BooterEntry(self.frame_time_completed, width=WIDTH)
		e_min = BooterEntry(self.frame_time_completed, width=WIDTH)
		widgets = {"e_hour": e_hour,
		           "e_min": e_min}
		self.labels["time_completed"] = lbl
		self.widgets["time_completed"] = widgets

		lbl.grid(row=2, column=0)
		e_hour.grid(row=0, column=0)
		BooterLabel(self.frame_time_completed, text=":").grid(row=0, column=1)
		e_min.grid(row=0, column=2)


	def init_date_completed(self):
		lbl = BooterLabel(self.frame_input, text="Date Completed")
		today = dt.datetime.now()
		cal = DateEntry(self.frame_input, selectmode="day", year=today.year, month=today.month, day=today.day)
		widgets = {"cal": cal}
		self.labels["date_completed"] = lbl
		self.widgets["date_completed"] = widgets
		lbl.grid(row=3, column=0)
		cal.grid(row=3, column=1)


	def check_clicked(self):
		if self.check_input():
			self.change_status(True)
			self.create_session()
		else:
			self.change_status(False)


	def change_status(self, is_valid):
		
		if is_valid:
			self.lbl_status.config(fg="green", text="Session logged!")
		else:
			self.lbl_status.config(fg="red", text="Please fix errors")
		if self.after_job:
			self.lbl_status.after_cancel(self.after_job)
		self.after_job = self.lbl_status.after(2000, lambda: self.lbl_status.config(text=""))


			
	def check_input(self):
		is_valid = True
		if not self.validate_task():
			is_valid = False
		if not self.validate_task_time():
			is_valid = False
		if not self.validate_time_completed():
			is_valid = False
		if not self.validate_date_completed():
			is_valid = False

		return is_valid



	def create_session(self):
		"""Create and return a Session based off the info
		currently in the input window"""
		# things we need:
		# task name
		# task time -> convert to seconds
		# time completed -> convert to whatever it's supposed to be
		# date completed
		# create session object
		# add it to the db
		task = self.widgets["optionmenu"]["om_var"].get()
		task_time = self.get_task_time()
		time_completed = self.get_time_completed()
		date_completed = self.get_date_completed()
		info = {"task": task, "task_time": task_time, "time_completed": time_completed, 
			"date_completed": date_completed}


		s = Session(task, task_time, time_completed, date_completed)
		sessiondao.insert_session(s)


	def get_task_time(self):
		"""Gets the h, m, and s from input window and returns the time
		in seconds as an integer"""
		h = int(self.widgets["task_time"]["e_hour"].get() or 0)
		m = int(self.widgets["task_time"]["e_min"].get() or 0)
		s = int(self.widgets["task_time"]["e_sec"].get() or 0)

		return h*3600 + m*60 + s


	def get_time_completed(self):
		"""Returns a string of format HH:MM based off current
		values in input (this is only called after validation)"""
		h = self.widgets["time_completed"]["e_hour"].get()
		m = self.widgets["time_completed"]["e_min"].get()
		return "{}:{:0>2}".format(h, m)


	def get_date_completed(self):
		"""Returns a string of format MM-DD-YY based off
		selected date in date entry widget"""
		date_str = self.widgets["date_completed"]["cal"].get()
		date_info = [int(i) for i in date_str.split("/")]
		month, day, year = tuple(date_info)
		year += 2000
		date_obj = dt.datetime(year, month, day).date()
		return date_obj.strftime("%m-%d-%y")


	def validate_task(self):
		if self.widgets["optionmenu"]["om_var"].get() == "Select...":
			self.widgets
			self.labels["task"].config(fg="red")
			return False
		self.labels["task"].config(fg="black")
		return True


	def validate_task_time(self):
		h = self.widgets["task_time"]["e_hour"].get() or 0
		m = self.widgets["task_time"]["e_min"].get() or 0
		s = self.widgets["task_time"]["e_sec"].get() or 0

		if not h and not m and not s:
			self.labels["task_time"].config(fg="red")
			return False
		try:
			int(h)
			int(m)
			int(s)
		except ValueError:
			self.labels["task_time"].config(fg="red")
			return False

		if int(h) != float(h) or int(m) != float(m) or int(s) != float(s):
			self.labels["task_time"].config(fg="red")
			return False
		self.labels["task_time"].config(fg="black")
		return True


	def validate_time_completed(self):
		h = self.widgets["time_completed"]["e_hour"].get()
		m = self.widgets["time_completed"]["e_min"].get()
		if not h or not m:
			self.labels["time_completed"].config(fg="red")
			return False
		try:
			int(h)
			int(m)
		except ValueError:
			self.labels["time_completed"].config(fg="red")
			return False

		if int(h) != float(h) or int(m) != float(m):
			self.labels["time_completed"].config(fg="red")
			return False

		h = int(h)
		m = int(m)
		if h < 0 or h > 23 or m < 0 or m > 59:
			self.labels["time_completed"].config(fg="red")
			return False
		self.labels["time_completed"].config(fg="black")
		return True


	def validate_date_completed(self):
		# Is this function needed? does date widget self validate?
		# Do we need to validate for time travel?
		try:
			self.get_date_completed()
			return True
		except ValueError:
			return False

	def refresh_option_menu(self):
		menu = self.widgets["optionmenu"]["om"]['menu']
		tasks = taskdao.get_all_tasks()
		menu.delete(0, END)
		om_var = self.widgets["optionmenu"]["om_var"]
		if not tasks:
			menu.add_command(label="No Tasks")
		else:
			for task in tasks:
				menu.add_command(label=task, command=lambda value=task: om_var.set(value))






def main():
	root = Tk()
	a = AddSession(root)
	a.pack()
	root.mainloop()


if __name__ == "__main__":
	main()