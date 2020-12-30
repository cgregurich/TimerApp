from tkinter import *
from booterwidgets import *
from goaldao import GoalDAO
from sessiondao import SessionDAO
import datetime as dt

from addgoal import AddGoal

# TODO:
# WHERE I LEFT OFF: just got the goals to display properly
# Disable entries
# change entry widths
# obviously tweak lbl_header so it looks decent
# resize window
# display goals -> task | goal_time | time_completed | time_remaining
# refresh this data in self.reset()

goaldao = GoalDAO()
sessiondao = SessionDAO()

class Goals(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		self.config(bg=storedsettings.APP_MAIN_COLOR)

		self.frame_buttons = None
		self.init_top()
		
		self.frame_goals = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_goals.grid(row=2, column=1)


		self.col_widths = {"task": 0,
						   "goal_time": 0,
						   "time_completed": 0,
						   "time_remaining": 0}
		
		self.COL_HEADERS = {"task": "task",
							"goal_time": "goal time",
							"time_completed": "time completed",
							"time_remaining": "time remaining"}
		self.row_frames = [] # to keep track of rows for gridding correctly
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
		self.frame_buttons = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons.grid(row=1, column=1)
		btn_add = BooterButton(self.frame_buttons, text="Add", command=self.add_clicked)
		btn_del = BooterButton(self.frame_buttons, text="Delete", command=self.del_clicked)
		btn_add.grid(row=0, column=0, padx=(0, 20), pady=(0, 10))
		btn_del.grid(row=0, column=1, pady=(0, 10))


	def add_clicked(self):
		win = Toplevel()
		win.config(bg=storedsettings.APP_MAIN_COLOR)
		a = AddGoal(win, self)
		a.pack()
		win.protocol("WM_DELETE_WINDOW", a.go_back)
		win.geometry("500x250")
		


	def del_clicked(self):
		# used currently for printing debug info
		print()
		print(self.parent.winfo_height())
		print(self.parent.winfo_width())
		print(self.frame_goals.winfo_height())
		print(self.frame_goals.winfo_width())



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
		# for key in self.col_widths.keys():
		# 	self.col_widths[key] += 1


	def draw_col_headers(self):
		header_frame = self.create_goal_frame(self.COL_HEADERS, header=True)
		self.draw_goal_row_frame(header_frame)
		self.row_frames.append(header_frame)


	def draw_goals(self):
		display_data = self.get_display_data()
		for data_dict in display_data:
			row_frame = self.create_goal_frame(data_dict)
			self.draw_goal_row_frame(row_frame)
			self.row_frames.append(row_frame)


	def create_goal_frame(self, data, header=False):
		"""Expects a dict:
		{"task": str, "goal_time": str, "time_completed": str,
		"time_remaining": str} the strings are formatted for display already.
		Returns the frame that holds the widgets that contain the data"""
		# A row should be a frame that contains disabled entries 
		# that display: task | goal_time | time_completed | time_remaining
		frame = Frame(self.frame_goals)
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
		e_task.config(state=DISABLED)
		e_goal_time.config(state=DISABLED)
		e_time_completed.config(state=DISABLED)
		e_time_remaining.config(state=DISABLED)

		e_task.grid(row=0, column=0)
		e_goal_time.grid(row=0, column=1)
		e_time_completed.grid(row=0, column=2)
		e_time_remaining.grid(row=0, column=3)

		return frame


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
			# row = {}
			# row["task"] = formatted_data["task"]
			# row["goal_time"] = formatted_data["goal_time"]
			# row["time_completed"] = formatted_data["time_completed"]
			# row["time_remaining"] = formatted_data["time_remaining"]
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


	def draw_goal_row_frame(self, row_frame):
		row_frame.grid(row=len(self.row_frames), column=0)


	def clear_screen(self):
		for frame in self.row_frames:
			frame.destroy()




	def reset(self):
		"""Reload the data; check for updated goals; recalculate
		time completed and time remaining"""
		self.clear_screen()
		self.init_main_frame()
		# self.parent.geometry(storedsettings.GOALS_WIN_SIZE)
