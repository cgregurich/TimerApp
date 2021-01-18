import tkinter as tk
import storedsettings
from booterwidgets import *
from taskdao import TaskDAO
from goaldao import GoalDAO
from tkinter import messagebox

ERROR = "error"
ADD = "add"
UPDATE = "update"

taskdao = TaskDAO()
goaldao = GoalDAO()

# TODO:
# Check if the current goal to be added's task is already part
# of another goal

class AddGoal(tk.Frame):
	def __init__(self, parent, main_win):
		tk.Frame.__init__(self, parent)
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.parent = parent
		self.main_win = main_win

		self.init_back_btn()
		self.init_frames()
		

		self.widgets = {"optionmenu": None,
						"goal_time": None}

		# Allows changing of label colors to indicate errors
		self.labels = {"task": None, "goal_time": None}

		# Keeps track of timer for changing status label
		self.after_job = None 

		self.is_empty = True
		self.is_saved = False

		self.draw_window()


	def init_back_btn(self):
		btn_back = BooterButton(self, command=self.back_clicked)
		btn_back.apply_back_image()
		btn_back.grid(row=0, column=0, sticky="n")

	def init_frames(self):
		self.frame_input = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_goal_task = tk.Frame(self.frame_input, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_goal_time = tk.Frame(self.frame_input, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_input.grid(row=0, column=1, padx=40)
		self.frame_goal_task.grid(row=0, column=1, pady=(0, 60))
		self.frame_goal_time.grid(row=1, column=1)


	def draw_window(self):
		self.init_task_optionmenu()
		self.init_goal_time()
		self.refresh_option_menu()
		self.init_lbl_status()
		self.init_btn_add()
		

	def init_lbl_status(self):
		self.lbl_status = BooterLabel(self, text="")
		self.lbl_status.config(font=(storedsettings.FONT, 15, "bold"), fg="green")
		self.lbl_status.grid(row=2, column=1)

	def init_btn_add(self):
		self.btn_add = BooterButton(self, text="Add", command=self.add_clicked)
		self.btn_add.grid(row=3, column=1)

	def add_clicked(self):
		if self.is_valid():
			self.correct_entries()
			u = self.check_task_uniqueness()
			if u == -1: # user doesn't want to update existing goal
				return
			elif u == 1: # user wants to update existing goal
				self.update_goal()
				self.change_status(UPDATE)
			elif u == 0: # goal is new; add it
				self.add_goal()
				self.change_status(ADD)
		else:
			self.change_status(ERROR)


	def check_task_uniqueness(self):
		"""Check if there is already a goal with this task
		Returns -1, 0, or 1
		-1: Task is not unique and user doesn't want to update
		0 Task is unique
		1 Task is unqiue and user wants to (and has) updated"""
		task = self._get_selected_task()
		all_goal_tasks = goaldao.get_all_tasks()
		if task in all_goal_tasks:
			if self.ask_user_to_update_goal():
				return 1
			else:
				return -1
		else:
			return 0

	def ask_user_to_update_goal(self):
		task = self._get_selected_task()
		update = messagebox.askyesno("Duplicate goal", 
				f"There is already a goal for '{task}'."
				" Would you like to update it with this time?",
				 parent=self)
		if update:
			return True
		else:
			return False

	def add_goal(self):
		"""Assumes validation has already been done"""
		goal_dict = self.make_goal_dict()
		goaldao.insert_goal(goal_dict)

	def update_goal(self):
		"""Assumes validation has already been done"""
		goal_dict = self.make_goal_dict()
		goaldao.update_goal(goal_dict)


	def make_goal_dict(self):
		"""Returns a dict that looks like:
		{"task": str, "goal_time": int (total seconds)}
		Assumes validation has already been done."""
		task = self._get_selected_task()
		goal_time = self.get_total_seconds()
		goal_dict = {"task": task, "goal_time": goal_time}
		return goal_dict



	def correct_entries(self):
		"""Eg. If user enters 10:64:30, it will change
		the entries to display 11:04:30"""
		h, m, s = self.get_converted_h_m_s()
		e_hour = self.widgets["goal_time"]["e_hour"]
		e_min = self.widgets["goal_time"]["e_min"]
		e_sec = self.widgets["goal_time"]["e_sec"]

		# Clear text in entries
		e_hour.delete(0, tk.END)
		e_min.delete(0, tk.END)
		e_sec.delete(0, tk.END)

		# Zero pad minutes and seconds
		m = "{:0>2}".format(m)
		s = "{:0>2}".format(s)
		e_hour.insert(0, h)
		e_min.insert(0, m)
		e_sec.insert(0, s)
		


	def get_raw_h_m_s(self):
		"""Returns tuple of the current data in the h, m, and s
		entries in the window."""
		h = self.widgets["goal_time"]["e_hour"].get()
		m = self.widgets["goal_time"]["e_min"].get()
		s = self.widgets["goal_time"]["e_sec"].get()
		return (h, m, s)


	def get_zeroed_h_m_s(self):
		"""Returns a tuple of h, m, s as numbers
		If the entry was blank, that value becomes a 0"""
		h, m, s = self.get_raw_h_m_s()
		h = h or 0
		m = m or 0
		s = s or 0

		return (h, m, s)


	def get_converted_h_m_s(self):
		"""Converts h, m, and s to numeric values.
		Clamps m and s to be under 60.
		Eg. 10:64:30 becomes 11:4:30.
		Assumes validation has already been completed.
		Allows decimal input for h and m; converts accordingly."""
		h, m, s = self.get_zeroed_h_m_s()
		h = float(h)
		m = float(m)
		s = float(s)
		total_s = h * 3600 + m * 60 + s
		m, s = divmod(total_s, 60)
		h, m = divmod(m, 60)
		return (int(h), int(m), int(s))


	def get_total_seconds(self):
		h, m, s = self.get_converted_h_m_s()
		return h * 3600 + m * 60 + s


	def change_status(self, arg):
		"""Expects an arg from these: UPDATE, ERROR, ADD"""
		self.is_saved = True
		if arg == UPDATE:
			self.lbl_status.config(fg="green", text="Goal updated!")
		elif arg == ADD:
			self.lbl_status.config(fg="green", text="Goal added!")
		elif arg == ERROR:
			self.lbl_status.config(fg="red", text="Please fix errors")
			self.is_saved = False
		else:
			raise ValueError("change_status expects arg of UPDATE, ERROR, or ADD")
		if self.after_job:
			self.lbl_status.after_cancel(self.after_job)
		self.after_job = self.lbl_status.after(2000, lambda: self.lbl_status.config(text=""))


	def is_valid(self):
		is_valid = True
		if not self.validate_task():
			is_valid = False
		if not self.validate_goal_time():
			is_valid = False
		return is_valid


	def validate_task(self):
		"""Returns True is user has selected a task
		Returns False is task is still set to default 
		i.e. 'Select...'"""
		task = self._get_selected_task()
		if task == "Select...": # Invalid task
			self.labels["task"].config(fg="red")
			return False
		else:
			self.labels["task"].config(fg="black")
			return True


	def validate_goal_time(self):
		h, m, s = self.get_raw_h_m_s()
		# Set to 0 if an empty string to allow numeric checking
		h = h or 0
		m = m or 0
		s = s or 0
		# Check for total emptiness
		if not h and not m and not s:
			self.labels["goal_time"].config(fg="red")
			return False
		# Check for non-numeric input
		try:
			float(h)
			float(m)
			float(s)
		except ValueError:
			self.labels["goal_time"].config(fg="red")
			return False
		# Check for whole number seconds (h and m can be decimals)
		try:
			int(s)
		except ValueError:
			self.labels["goal_time"].config(fg="red")
			messagebox.showerror("Invalid seconds", "Seconds must be a whole number", parent=self)
			return False
			

		self.labels["goal_time"].config(fg="black")
		return True


	def back_clicked(self):
		# Check if data has been entered into the 4 inputs
		# If there is data, ask if user wants to save
		# If not, go back
		if self.check_empty():
			self.go_back()
		else:
			if self.is_saved:
				self.go_back()
				return
			discard = messagebox.askyesno("Changes have been made",
				"Would you like to discard your changes?", parent=self)
			if discard:
				self.go_back()


	def go_back(self):
		self.parent.destroy()
		if self.after_job: self.lbl_status.after_cancel(self.after_job)

		self.main_win.reset()
		



	def check_empty(self):
		"""Returns True if no info has been entered.
		Returns False if any info has been entered"""
		task = self._get_selected_task()
		h, m, s = self.get_raw_h_m_s()
		if task != "Select...":
			return False
		if h or m or s:
			return False
		return True


	def init_task_optionmenu(self):
		lbl = BooterLabel(self.frame_input, text="Goal Task")
		om_var = tk.StringVar()
		om_var.set("Select...")
		om = BooterOptionMenu(self.frame_input, om_var, None)
		widgets = {"om_var": om_var,
				   "om": om}
		self.widgets["optionmenu"] = widgets
		self.labels["task"] = lbl

		lbl.grid(row=0, column=0)
		om.grid(row=0, column=1, padx=(20, 0))


	def init_goal_time(self):
		WIDTH = 4
		lbl = BooterLabel(self.frame_input, text="Goal Time")
		widgets = {}
		e_hour = BooterEntry(self.frame_goal_time, width=WIDTH)
		e_min = BooterEntry(self.frame_goal_time, width=WIDTH)
		e_sec = BooterEntry(self.frame_goal_time, width=WIDTH)
		widgets["e_hour"] = e_hour
		widgets["e_min"] = e_min
		widgets["e_sec"] = e_sec
		self.labels["goal_time"] = lbl
		self.widgets["goal_time"] = widgets

		# Put widgets on screen
		lbl.grid(row=1, column=0)
		e_hour.grid(row=0, column=1, padx=(20,0))
		BooterLabel(self.frame_goal_time, text=":").grid(row=0, column=2)
		e_min.grid(row=0, column=3)
		BooterLabel(self.frame_goal_time, text=":").grid(row=0, column=4)
		e_sec.grid(row=0, column=5)


	def refresh_option_menu(self):
		menu = self.widgets["optionmenu"]["om"]["menu"]
		om_var = self.widgets["optionmenu"]["om_var"]
		tasks = taskdao.get_all_tasks()
		menu.delete(0, tk.END)
		if not tasks:
			menu.add_command(label="No Tasks")
		else:
			for task in tasks:
				menu.add_command(label=task, command=lambda value=task: om_var.set(value))


	def _get_selected_task(self):
		task = self.widgets["optionmenu"]["om_var"].get()
		return task


