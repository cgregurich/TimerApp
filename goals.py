import tkinter as tk
from booterwidgets import *
from goaldao import GoalDAO
from sessiondao import SessionDAO
import datetime as dt

from addgoal import AddGoal


goaldao = GoalDAO()
sessiondao = SessionDAO()

class Goals(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent

		self.config(bg=storedsettings.APP_MAIN_COLOR)

		self.frame_buttons = None
		self.init_top()
		
		self.frame_goals = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_goals.grid(row=2, column=1)


		self.col_widths = {"task": 0,
						   "goal_time": 0,
						   "time_completed": 0,
						   "time_remaining": 0}
		
		self.COL_HEADERS = {"task": "task",
							"goal_time": "goal time",
							"time_completed": "time completed",
							"time_remaining": "time remaining"}
		self.header_frame_row = None
		self.row_frames = [] # to keep track of rows for gridding correctly
		self.check_btns = []
		self.check_vars = [None]

		self.init_main_frame()


	def init_top(self):
		"""Draws Goals label and back button at the top"""
		self.init_back_btn()
		self.init_lbl_header()
		self.init_buttons()


	def init_back_btn(self):
		btn_back = BooterButton(self, command=self.back_clicked)
		btn_back.apply_back_image()
		btn_back.grid(row=0, column=0, sticky="n", padx=(10, 10))


	def init_lbl_header(self):
		lbl_header = BooterLabel(self, text="Goals")
		lbl_header.config(font=(storedsettings.FONT, 20, "bold"))
		lbl_header.grid(row=0, column=1, columnspan=2, pady=(0, 10))


	def init_buttons(self):
		self.frame_buttons = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons.grid(row=1, column=1)
		btn_add = BooterButton(self.frame_buttons, text="Add", command=self.add_clicked)
		btn_del = BooterButton(self.frame_buttons, text="Delete", command=self.del_clicked)
		btn_add.grid(row=0, column=0, padx=(0, 20), pady=(0, 10))
		btn_del.grid(row=0, column=1, pady=(0, 10))


	def add_clicked(self):
		win = tk.Toplevel()
		win.config(bg=storedsettings.APP_MAIN_COLOR)
		a = AddGoal(win, self)
		a.pack()
		win.protocol("WM_DELETE_WINDOW", a.go_back)
		win.geometry("500x250")
		


	def del_clicked(self):
		del_indices = self.get_checked_indices()
		del_goals = self.get_task_names_at_indices(del_indices)
		self.remove_rows_at_indices(del_indices)
		self.remove_goals_from_database(del_goals)


	def remove_goals_from_database(self, task_names):
		for task_name in task_names:
			goaldao.delete_goal(task_name)


	def get_task_names_at_indices(self, indices):
		goals = goaldao.get_all_goals()
		tasks = [goals[i]["task"] for i in indices]
		return tasks



	def remove_rows_at_indices(self, indices):
		"""Expects a list of integers representing
		the indices of the frames to be deleted.
		Destroys frame at specified indices as well as removes
		checkbutton at specified indices, and removes both from their
		respective lists."""
		for i in indices:
			self.row_frames[i].destroy()
			self.check_btns[i].destroy()

		# Removes the correct frames, checkbuttons, and variables from respective lists
		# Done this way to avoid modifying a concurrent list
		self.row_frames = [self.row_frames[i] for i in range(len(self.row_frames)) if i not in indices]
		self.check_btns = [self.check_btns[i] for i in range(len(self.check_btns)) if i not in indices]
		self.check_vars = [self.check_vars[i] for i in range(len(self.check_vars)) if i not in indices]




	def get_checked_indices(self):
		indices = []
		for i, cv in enumerate(self.check_vars):
			if cv.get() == 1:
				indices.append(i)
		return indices
		

	def init_main_frame(self):
		self.set_col_widths()
		self.draw_col_headers()
		self.draw_goals()



	def back_clicked(self):
		self.parent.show_frame("MainMenu")


	def set_col_widths(self):
		display_data = self.get_display_data()
		display_data.append(self.COL_HEADERS)
		keys = ("task", "goal_time", "time_completed", "time_remaining")
		for key in keys:
			for row in display_data:
				self.col_widths[key] = max(self.col_widths[key], len(row[key]))


	def draw_col_headers(self):
		header_frame = self.create_goal_frame(self.COL_HEADERS, header=True)
		self.draw_goal_row_frame(header_frame)
		self.header_frame_row = header_frame


	def draw_goals(self):
		display_data = self.get_display_data()
		for data_dict in display_data:
			row_frame = self.create_goal_frame(data_dict)
			self.row_frames.append(row_frame)
			self.draw_check_button()
			self.draw_goal_row_frame(row_frame)
			

	def create_goal_frame(self, data, header=False):
		"""Expects a dict:
		{"task": str, "goal_time": str, "time_completed": str,
		"time_remaining": str} the strings are formatted for display already.
		Returns the frame that holds the widgets that contain the data"""
		# A row should be a frame that contains disabled entries 
		# that display: task | goal_time | time_completed | time_remaining
		frame = tk.Frame(self.frame_goals)
		
		e_task = BooterEntry(frame, width=self.col_widths["task"], justify="center")
		e_goal_time = BooterEntry(frame, width=self.col_widths["goal_time"], justify="center")
		e_time_completed = BooterEntry(frame, width=self.col_widths["time_completed"], justify="center")
		e_time_remaining = BooterEntry(frame, width=self.col_widths["time_remaining"], justify="center")

		e_task.config(font=storedsettings.GOAL_FONT)
		e_goal_time.config(font=storedsettings.GOAL_FONT)
		e_time_completed.config(font=storedsettings.GOAL_FONT)
		e_time_remaining.config(font=storedsettings.GOAL_FONT)


		# Get data to use
		task = data["task"]
		goal_time = data["goal_time"]
		time_completed = data["time_completed"]
		time_remaining = data["time_remaining"]

		

		# Put data into widgets

		e_task.insert(0, task)
		e_goal_time.insert(0, goal_time)
		e_time_completed.insert(0, time_completed)
		e_time_remaining.insert(0, time_remaining)

		# Set disabled colors
		e_task.config(disabledforeground="black")
		e_goal_time.config(disabledforeground="black")
		e_time_completed.config(disabledforeground="black")
		e_time_remaining.config(disabledforeground="black")

		# Disable all entries
		e_task.config(state=tk.DISABLED)
		e_goal_time.config(state=tk.DISABLED)
		e_time_completed.config(state=tk.DISABLED)
		e_time_remaining.config(state=tk.DISABLED)

		
		e_task.grid(row=0, column=1)
		e_goal_time.grid(row=0, column=2)
		e_time_completed.grid(row=0, column=3)
		e_time_remaining.grid(row=0, column=4)


		return frame


	def draw_goal_row_frame(self, row_frame):
		row_frame.grid(row=len(self.row_frames), column=1)
		


	def draw_check_button(self):
		check_var = tk.IntVar()
		check_del = BooterCheckbutton(self.frame_goals, variable=check_var)
		check_del.grid(row=len(self.row_frames), column=0)
		self.check_vars.append(check_var)
		self.check_btns.append(check_del)


	def get_display_data(self):
		"""Returns a list of dicts of the data that will be displayed.
		Each "row" of the matrix will be of format:
		(task: str, "goal_time": str, 
		"time_completed": str, "time_remaining": str)"""
		all_data = []
		goals = goaldao.get_all_goals()
		for goal in goals:
			raw_data = self._make_raw_goal_data(goal)
			formatted_data = self.format_goal_data(raw_data)
			all_data.append(formatted_data)
		return all_data


	def _make_raw_goal_data(self, goal_dict):
		"""Expects a dict of format:
		{"task": str, "goal_time": int}
		Adds to the dict the time completed for the goal for the day
		and the time remaining for the goal for the day.
		All number data are total seconds as integers; unformatted"""
		task = goal_dict["task"]
		goal_time = goal_dict["goal_time"]
		time_completed = self.calc_time_completed(task)
		goal_dict["time_completed"] = time_completed
		goal_dict["time_remaining"] = goal_time - time_completed
		return goal_dict


	def format_goal_data(self, goal_dict):
		"""Formats the 3 numeric data of goal_dict to
		be of format H:MM:SS"""
		goal_dict["goal_time"] = self.format_total_seconds(goal_dict["goal_time"])
		goal_dict["time_completed"] = self.format_total_seconds(goal_dict["time_completed"])
		goal_dict["time_remaining"] = self.format_total_seconds(goal_dict["time_remaining"])
		return goal_dict


	def format_total_seconds(self, time):
		"""Expects an arg of type int representing total seconds.
		Returns a str of format HH:MM:SS, zero padded"""
		# Deal with negative numbers without changing the end
		# number, but also without losing the minus sign
		sign = ""
		if time < 0:
			time *= -1
			sign = "-"
		m, s = divmod(time, 60)
		h, m = divmod(m, 60)
		return " {}{}:{:0>2}:{:0>2} ".format(sign, h, m, s)


	def calc_time_completed(self, task_name):
		"""Expects task_name -> str
		Returns total number of seconds"""
		sessions = self.get_today_sessions_of_task(task_name)
		val = self._get_total_seconds_of_sessions(sessions)
		return val


	def get_today_sessions_of_task(self, task_name):
		"""Expects a string task_name.
		Returns a list that only contains Sessions 
		that are of the task specified by task_name from
		today's logged sessions"""
		day_sessions = sessiondao.get_all_sessions_from_date(dt.datetime.now().date())
		sessions = []
		
		for s in day_sessions:
			if s.task == task_name:
				sessions.append(s)
		return sessions


	def _get_total_seconds_of_sessions(self, sessions):
		"""Expects a list of Session objects
		Returns the total sum number of seconds in all the sessions"""
		total_seconds = 0
		for s in sessions:
			total_seconds += s.task_time
		return total_seconds



	def clear_screen(self):
		"""Destroys widgets and removes them from class lists"""
		for frame in self.row_frames:
			frame.destroy()
		for check_btn in self.check_btns:
			check_btn.destroy()
		self.header_frame_row.destroy()
		self.row_frames = []
		self.check_vars = []
		self.check_btns = []




	def reset(self):
		"""Reload the data; check for updated goals; recalculate
		time completed and time remaining"""
		self.clear_screen()
		self.init_main_frame()
	
