
from tkinter import *
from tkinter import ttk
from locals import *
from session import Session
from sessiondao import SessionDAO
from taskdao import TaskDAO
import datetime as dt
from datetime import date
from tkcalendar import *
from booterwidgets import *
from addsession import AddSession

import autocomplete
import calendar

# things i need as far as buttons and controls go:
# - back button
# - task search
# - date entry(s)
# - mode optionmenu
# - view button
# - add button
# - arrow buttons


sessiondao = SessionDAO()
taskdao = TaskDAO()


class ViewLog(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		
		self.config(bg=storedsettings.APP_MAIN_COLOR)

		# OVERHAUL FRAMES
		self.frame_upper = Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_lower = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_totals = Frame(self.frame_lower, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_upper.grid(row=0, column=0)
		self.frame_lower.grid(row=1, column=0)
		self.frame_totals.grid(row=0, column=0)


		self.session_rows = [] # list of lists of labels

		self.input_widgets = {}

		self.total_labels = []

		self.draw_window()

	def draw_window(self):
		PADY = 5
		PADX = 5

		btn_back = BooterButton(self.frame_upper, command=self.back_clicked)
		btn_back.grid(row=0, column=0, sticky="n", pady=PADY)
		btn_back.apply_back_image()


		# FRAME CONTROLS
		self.mode_var = StringVar()
		self.mode_var.set(DAY)

		modes = (DAY, WEEK, MONTH, TASK)
		self.mode_om = BooterOptionMenu(self.frame_upper, self.mode_var, command=self.mode_changed, *modes)
		self.mode_om.config(width=90)
		self.mode_om.change_fontsize(17)


		self.mode_om.grid(row=0, column=1, padx=PADX, pady=PADY)
	
		self.btn_view = BooterButton(self.frame_upper, text="View", command=self.view_clicked)
		
		self.btn_add = BooterButton(self.frame_upper, text="Add", command=self.add_clicked)

		self.btn_view.grid(row=0, column=2, padx=PADX)
		self.btn_add.grid(row=0, column=3, padx=PADX)
		

		# CREATE SCROLLABLE WINDOW
		#                     this is how we get no grey line between totals and sessions      DON'T REMOVE HIGHLIGHT BACKGROUND
		self.display_canvas = Canvas(self.frame_lower, bg=storedsettings.APP_MAIN_COLOR, width=440, highlightbackground=storedsettings.APP_MAIN_COLOR) 
		self.yscrollbar = Scrollbar(self.frame_lower, orient="vertical", command=self.display_canvas.yview)
		# self.xscrollbar = Scrollbar(self.frame_data, orient="horizontal", command=self.display_canvas.xview)
		self.scrollable_frame = Frame(self.display_canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.display_canvas.configure(
				scrollregion=self.display_canvas.bbox("all")
			)
		)

		self.display_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


		self.display_canvas.configure(yscrollcommand=self.yscrollbar.set)
		# self.display_canvas.configure(xscrollcommand=self.xscrollbar.set)

		self.display_canvas.grid(row=1, column=0)
		self.yscrollbar.grid(row=1, column=2, sticky='nsew')
		# self.xscrollbar.grid(row=3, column=0, sticky='nsew')

		self.parent.bind_all("<MouseWheel>", self._on_mousewheel)

		self.init_input_widgets()
		self.draw_sessions()



	def add_clicked(self):
		win = Toplevel()
		win.config(bg=storedsettings.APP_MAIN_COLOR)
		win.geometry("500x250")
		a = AddSession(win)
		a.pack()


	def back_clicked(self):
		self.parent.show_frame("MainMenu")
		self.parent.resizable(False, False)

	def init_input_widgets(self):
		"""Since the autocomplete only needs to be drawn once, it's in its own init function, and the other widgets that 
		will change depending on the selected mode are also created here for the first time"""
		self.draw_autocomplete()
		self.mode_changed()

	def mode_changed(self, event=None):
		"""Takes arg event because this func is a command of an option menu"""
		self.reset_calendars()


	def _calc_week_ago(self):
		"""Return the date 7 days ago from today"""
		return dt.datetime.now() - dt.timedelta(days=7)


	def _calc_month_ago(self):
		"""Returns the dat 30 days ago from today"""
		return dt.datetime.now() - dt.timedelta(days=30)


	def reset_calendars(self):
		"""When TASK mode is selected, the calendars and arrows and destroyed and deleted. Otherwise, the calendars are either
		created or their dates are changed, depending on the previous selected mode."""

		mode = self.mode_var.get()
		if mode == DAY:
			self.draw_calendars(dt.datetime.today(), dt.datetime.today())
		elif mode == WEEK:
			self.draw_calendars(self._calc_week_ago(), dt.datetime.today())
		elif mode == MONTH:
			self.draw_calendars(self._calc_month_ago(), dt.datetime.today())
		elif mode == TASK:
			self.destroy_calendars()

	def destroy_calendars(self):
		"""Only need to destroy calendars (and arrows) when task mode is selected"""
		self.input_widgets["cal1"].destroy()
		self.input_widgets["cal2"].destroy()
		self.input_widgets["leftbtn1"].destroy()
		self.input_widgets["rightbtn1"].destroy()
		self.input_widgets["leftbtn2"].destroy()
		self.input_widgets["rightbtn2"].destroy()

		del self.input_widgets["cal1"]
		del self.input_widgets["cal2"]
		del self.input_widgets["leftbtn1"]
		del self.input_widgets["rightbtn1"]
		del self.input_widgets["leftbtn2"]
		del self.input_widgets["rightbtn2"]
		

	def create_calendar(self, date):
		"""Helper function for creating and returning a DateEntry object.
		Date is a dt.datetime object"""
		cal = DateEntry(self.frame_upper, selectmode="day", year=date.year, month=date.month, day=date.day, firstweekday="sunday", font=storedsettings.CALENDAR_FONT)
		return cal

	def draw_calendars(self, date1, date2):
		"""Creates two DateEntry objects: one with date1, one with date2. Grids them and saves them, and draws the arrows for both."""
		# if the calendars already exist, then just change the dates on them don't create new ones
		if "cal1" in self.input_widgets.keys() and "cal2" in self.input_widgets.keys():
			self.set_calendar_dates(date1, date2)
			return

		PADY = 5
		cal1 = self.create_calendar(date1)
		cal1.grid(row=1, column=2, pady=PADY)
		self.input_widgets["cal1"] = cal1

		
		cal2 = self.create_calendar(date2)
		cal2.grid(row=2, column=2)
		self.input_widgets["cal2"] = cal2

		self._draw_cal_arrows()


	def set_calendar_dates(self, date1, date2):
		"""Func to optimize when the view mode is changed. Instead of destroying then remaking the calendar widgets, it's
		more efficient to simply change the date, if possible (not possible when the last mode was TASK)"""
		self.input_widgets["cal1"].set_date(date1)
		self.input_widgets["cal2"].set_date(date2)


	def view_clicked(self):
		self.draw_sessions()


	def _draw_cal_arrows(self):
		"""Creates, grids, and saves all arrows for the calendar widgets."""
		btn_left = BooterButton(self.frame_upper, text="<", command=lambda: self.left_arrow("cal1"))
		btn_right = BooterButton(self.frame_upper, text=">", command=lambda: self.right_arrow("cal1"))
		btn_left.grid(row=1, column=1)
		btn_right.grid(row=1, column=3)
		self.input_widgets["leftbtn1"] = btn_left
		self.input_widgets["rightbtn1"] = btn_right


		btn_left = BooterButton(self.frame_upper, text="<", command=lambda: self.left_arrow("cal2"))
		btn_right = BooterButton(self.frame_upper, text=">", command=lambda: self.right_arrow("cal2"))
		btn_left.grid(row=2, column=1)
		btn_right.grid(row=2, column=3)
		self.input_widgets["leftbtn2"] = btn_left
		self.input_widgets["rightbtn2"] = btn_right
		

	def left_arrow(self, cal_name):
		"""Func bound to the left arrow widgets. Arg cal_name indicates which calendar is to be decremented"""
		if self.mode_var.get() == DAY:
			self.change_cal_date(days=-1, cal_name=cal_name)

		elif self.mode_var.get() == WEEK:
			self.change_cal_date(days=-7, cal_name=cal_name)

		elif self.mode_var.get() == MONTH:
			self.change_cal_date(days=-30, cal_name=cal_name)


	def right_arrow(self, cal_name):
		"""Func bound to the right arrow widgets. Arg cal_name indicates which calendar is to be incremented."""
		if self.mode_var.get() == DAY:
			self.change_cal_date(days=1, cal_name=cal_name)

		elif self.mode_var.get() == WEEK:
			self.change_cal_date(days=7, cal_name=cal_name)

		elif self.mode_var.get() == MONTH:
			self.change_cal_date(days=30, cal_name=cal_name)



	def change_cal_date(self, days, cal_name):
		"""For incrementing/decrementing caledar by number of days. Days is negative if it's to be decremented"""
		cal = self.input_widgets[cal_name]
		delta = dt.timedelta(days=days)
		tmp = cal.get_date()
		cal.set_date(cal.get_date() + delta)
		if (self.input_widgets["cal1"].get_date() > self.input_widgets["cal2"].get_date()):
			cal.set_date(tmp)


	def draw_task_widgets(self):
		self.draw_autocomplete()

	def draw_autocomplete(self):
		entry = autocomplete.AutoComplete(self.frame_upper, options=taskdao.get_all_tasks(), width=16)
		entry.config(relief=SOLID, bd=1)
		entry.grid(row=1, column=0)
		self.input_widgets["entry"] = entry
		entry.bind("<Return>", self._bind_func)

	def _bind_func(self, e):
		self.focus_set()
		self.draw_sessions()
		self.input_widgets["entry"]._close_popup()


	def _on_mousewheel(self, event):
		self.display_canvas.yview_scroll(-1*(event.delta//120), "units")


	def grab_date_from_cal(self, cal_name):
		"""Returns the current selected date as a datetime.datetime.date obj (???)"""
		date_str = self.input_widgets[cal_name].get()
		date_info = [int(i) for i in date_str.split('/')]
		month, day, year = tuple(date_info)
		year += 2000
		date_obj = dt.datetime(year, month, day).date()
		return date_obj
	

	def draw_sessions(self):
		self._clear_screen()

		# If user is searching for all sessions of a specific task
		if self.mode_var.get() == TASK:
			task = self.input_widgets["entry"].get()
			sessions_list = sessiondao.get_all_sessions_by_task(task)

		else:
			if self._is_task_entered():
				sessions_list = self.get_selected_timeframe_sessions_by_task()
			else:
				sessions_list = self.get_selected_timeframe_sessions()

		self.draw_sessions_to_screen(sessions_list)
		self.draw_totals(sessions_list)

		# Why -21? Because that's what number works; if it's higher or lower, 
		# the frame will shrink/grow each time the page is redrawn
		self.display_canvas.config(width=self.frame_lower.winfo_width()-21)


	def _is_task_entered(self):
		return self.input_widgets["entry"].get() != ""


	def get_selected_timeframe_sessions_by_task(self):

		sessions = self.get_selected_timeframe_sessions()
		task = self._get_entered_task()
		task_sessions = []
		for s in sessions:
			if s.task == task:
				task_sessions.append(s)
		return task_sessions


	def _get_entered_task(self):
		"""
		Assumes validation has already been done. does it matter tho?
		"""
		return self.input_widgets["entry"].get()


	def get_selected_timeframe_sessions(self):
		"""Method used for when in week or month mode (two calendar widgets exist)
		Grabs date from both and retrieves all Sessions from between those dates, inclusive"""
		start = self.grab_date_from_cal("cal1")
		end = self.grab_date_from_cal("cal2")

		sessions = sessiondao.get_all_sessions_between_dates(start, end)
		return sessions


	def draw_totals(self, sessions_list):
		tasks_time_dict = self._create_tasks_time_dict(sessions_list)
		for task, time in tasks_time_dict.items():
			self._create_total_label(task, time)


	def _create_total_label(self, task, seconds):
		"""
		task: string
		time: int (seconds)
		"""
		formatted_time = self._format_seconds(seconds)
		lbl_task = BooterLabel(self.frame_totals, text=f"{task}:", anchor="w")
		lbl_time = BooterLabel(self.frame_totals, text=formatted_time)
		# Config to override default BooterLabel options
		lbl_task.config(font=(storedsettings.LOG_FONT, storedsettings.LOG_LABEL_FONT_SIZE))
		lbl_task.config(font=(storedsettings.LOG_FONT, storedsettings.LOG_LABEL_FONT_SIZE))
		lbl_task.grid(row=len(self.total_labels), column=0)
		lbl_time.grid(row=len(self.total_labels), column=1)
		self.total_labels.append(lbl_task)
		self.total_labels.append(lbl_time)


	def _format_seconds(self, total_seconds):
		hours, seconds = divmod(total_seconds, 3600)
		minutes, seconds = divmod(seconds, 60)

		return "{:0>2}h {:0>2}m {:0>2}s".format(hours, minutes, seconds)


	def _create_tasks_time_dict(self, sessions_list):
		tasks_set = self._get_all_tasks_from_sessions(sessions_list)
		# Create a dictionary to map tasks to total time spent on task
		tasks_time_dict = {task:0 for task in tasks_set} # dict of format {task: time(in sec)}


		for session in sessions_list:
			
			tasks_time_dict[session.task] += session.task_time

		
		return tasks_time_dict


	def _get_all_tasks_from_sessions(self, sessions_list):
		"""Returns a set of tasks from the Session objects in sessions_list"""
		tasks_set = set()
		for session in sessions_list:
			tasks_set.add(session.task)
		return tasks_set

		
	def _calc_col_widths(self, sessions_list):
		"""Calculates how wide each column should be depending
		on the Session objects' data given in the arg sessions_list"""
		self.col_widths = [0, 0, 0, 0]
		for s in sessions_list:
			s_info = s.get_info_for_display()
			for i in range(len(self.col_widths)):
				if len(s_info[i]) > self.col_widths[i]:
					self.col_widths[i] = len(s_info[i])

		# Manually add padding to taste; since using non monospaced font
		PADS = (5, 0, 0, 4)
		for i in range(0, 4):
			self.col_widths[i] += PADS[i]

		# Because 20 works with fat characters at max char length (15)
		self.col_widths[0] = 20


	def draw_sessions_to_screen(self, all_sessions):
		"""sessions is a list of Session objects"""
		self._calc_col_widths(all_sessions)

		for s in all_sessions:
			row = self.create_session_row(s)
			self.session_rows.append(row)
			self._draw_row(row)

	
	def create_session_row(self, session):
		"""Receives Session obj as arg.
		Returns a list of lists of labels"""
		info = session.get_info_for_display()
		row = [Label(self.scrollable_frame, text=info[i], width=self.col_widths[i], 
			font=(storedsettings.LOG_FONT, storedsettings.LOG_LABEL_FONT_SIZE)) for i in range(len(self.col_widths))]
		return row

	def _draw_row(self, row):
		r = len(self.session_rows)
		c = 0
		if r % 2 != 0:
			color = "#FFFFFF"
		else:
			color = "#AFAFAF"

		for lbl in row:
			lbl.grid(row=r, column=c)
			lbl.config(bg=color)
			c += 1



	def _clear_screen(self):
		# Clear labels
		for row in self.session_rows:
			for lbl in row:
				lbl.destroy()
		self.session_rows = []

		# Clear totals labels
		for label in self.total_labels:
			label.destroy()
		self.total_labels = []




	def reset(self):
		self.draw_sessions()
		self.parent.resizable(True, True)
		self.parent.geometry("500x500")
