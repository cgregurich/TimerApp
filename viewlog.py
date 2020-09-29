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

import autocomplete
import calendar

import storedsettings






sessiondao = SessionDAO()
taskdao = TaskDAO()


class ViewLog(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.frame_controls = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_totals = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_data = Frame(self)

		self.frame_controls.grid(row=0, column=0)
		self.frame_totals.grid(row=1, column=0)
		self.frame_data.grid(row=2, column=0)

		self.frame_totals.grid_columnconfigure(0, weight=1)
		self.frame_totals.grid_rowconfigure(0, weight=1)


		self.session_rows = [] # list of lists of labels

		self.input_widgets = {}

		self.total_labels = []

		self.draw_window()

	def draw_window(self):
		btn_back = BooterButton(self.frame_controls, command=lambda: self.controller.show_frame("MainMenu"))
		btn_back.grid(row=0, column=0)
		btn_back.apply_back_image()


		# FRAME CONTROLS
		self.mode_var = StringVar()
		self.mode_var.set(DAY)

		self.btn_day = BooterSelect(self.frame_controls, text="Day", command=lambda: self.mode_btn_clicked(self.btn_day, DAY))
		self.btn_week = BooterSelect(self.frame_controls, text="Week", command=lambda: self.mode_btn_clicked(self.btn_week, WEEK))
		self.btn_month = BooterSelect(self.frame_controls, text="Month", command=lambda: self.mode_btn_clicked(self.btn_month, MONTH))
		self.btn_task = BooterSelect(self.frame_controls, text="Task", command=lambda: self.mode_btn_clicked(self.btn_task, TASK))
		self.select_btns = [self.btn_day, self.btn_week, self.btn_month, self.btn_task]
		self.btn_day.selected()



		self.btn_day.grid(row=0, column=1)
		self.btn_week.grid(row=0, column=2)
		self.btn_month.grid(row=0, column=3)
		self.btn_task.grid(row=0, column=4)


		self.btn_view = BooterButton(self.frame_controls, text="View", command=self.draw_sessions)
		self.btn_view.grid(row=1, column=1)
		

		# CREATE SCROLLABLE WINDOW
		#                     this is how we get no grey line between totals and sessions      DON'T REMOVE HIGHLIGHT BACKGROUND
		self.display_canvas = Canvas(self.frame_data, bg=storedsettings.APP_MAIN_COLOR, width=440, highlightbackground=storedsettings.APP_MAIN_COLOR) 
		self.yscrollbar = Scrollbar(self.frame_data, orient="vertical", command=self.display_canvas.yview)
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

		self.controller.bind_all("<MouseWheel>", self._on_mousewheel)



		self.change_input_widgets()
		self.draw_sessions()


	def mode_btn_clicked(self, button, mode):
		self.mode_var.set(mode)
		for btn in self.select_btns:
			btn.deselected()
		button.selected()
		self._clear_input_widgets()
		self.change_input_widgets()




	def change_input_widgets(self):
		mode = self.mode_var.get()
		if mode == DAY:
			self.draw_calendar()

		elif mode == WEEK:
			self.draw_week_widgets()
			

		elif mode == MONTH:
			self.draw_month_widgets()

		elif mode == TASK:
			self.draw_autocomplete()



	def draw_month_widgets(self):
		"""Draws two calendar pickers; one set to today, one set to a week ago"""

		today = dt.datetime.now()
		# Quick and dirty fix for if it's January; 1 - 1 != 12
		if today.month == 1:
			days_in_month = calendar.monthrange(today.year, 12)[1]
		else:
			days_in_month = calendar.monthrange(today.year, today.month-1)[1]
		month_ago = today - dt.timedelta(days=days_in_month)

		start = DateEntry(self.frame_controls, selectmode="day", year=month_ago.year, month=month_ago.month, day=month_ago.day)
		start.grid(row=1, column=0)

		
		end = DateEntry(self.frame_controls, selectmode="day", year=today.year, month=today.month, day=today.day)
		end.grid(row=1, column=1)

		self.btn_view.grid(row=1, column=2)

		self.input_widgets['calendar_end'] = end
		self.input_widgets['calendar_start'] = start

	def draw_week_widgets(self):
		"""Draws two calendar pickers; one set to today, one set to a week ago"""

		today = dt.datetime.now()
		week_ago = today - dt.timedelta(days=7)

		start = DateEntry(self.frame_controls, selectmode="day", year=week_ago.year, month=week_ago.month, day=week_ago.day)
		start.grid(row=1, column=0)

		
		end = DateEntry(self.frame_controls, selectmode="day", year=today.year, month=today.month, day=today.day)
		end.grid(row=1, column=1)

		self.btn_view.grid(row=1, column=2)

		

		self.input_widgets['calendar_end'] = end
		self.input_widgets['calendar_start'] = start



	def draw_calendar(self):
		today = dt.datetime.now()
		cal = DateEntry(self.frame_controls, selectmode="day", year=today.year, month=today.month, day=today.day)
		cal.grid(row=1, column=0)
		self.input_widgets['calendar_end'] = cal

	def draw_autocomplete(self):
		entry = autocomplete.AutoComplete(self.frame_controls, options=taskdao.get_all_tasks())
		entry.config(relief=SOLID, bd=1)
		entry.grid(row=1, column=0)
		self.input_widgets['entry'] = entry


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
		if self.mode_var.get() == DAY:
			sessions_list = self.get_selected_day_sessions()
		elif self.mode_var.get() == WEEK:
			sessions_list = self.get_selected_timeframe_sessions()

		elif self.mode_var.get() == MONTH:
			sessions_list = self.get_selected_timeframe_sessions()

		elif self.mode_var.get() == TASK:
			task = self.input_widgets['entry'].get()
			sessions_list = sessiondao.get_all_sessions_by_task(task)


		self.draw_sessions_to_screen(sessions_list)
		self.draw_totals(sessions_list)

		# Why -23? Because that's what number works; if it's higher or lower, 
		# the frame will shrink/grow each time the page is redrawn
		self.display_canvas.config(width=self.frame_data.winfo_width()-21)


	def get_selected_timeframe_sessions(self):
		"""Method used for when in week or month mode (two calendar widgets exist)
		Grabs date from both and retrieves all Sessions from between those dates, inclusive"""
		start = self.grab_date_from_cal('calendar_start')
		end = self.grab_date_from_cal('calendar_end')
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
		# return f"{hours}:{minutes}:{seconds}"

		return "{:0>2}h {:0>2}m {:0>2}s".format(hours, minutes, seconds)




	def _create_tasks_time_dict(self, sessions_list):
		tasks_set = self._get_all_tasks_from_sessions(sessions_list)
		# Create a dictionary to map tasks to total time spent on task
		tasks_time_dict = {task:0 for task in tasks_set} # dict of format {task: time(in sec)}

		for session in sessions_list:
			tasks_time_dict[session.task] += session.time_logged

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



	def get_selected_day_sessions(self):	
		day = self.grab_date_from_cal('calendar_end')
		selected_day_sessions = sessiondao.get_all_sessions_from_date(day)

		return selected_day_sessions
	
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

	def _clear_input_widgets(self):
		# Clear input section (calendar/entry)
		for widget in self.input_widgets.values():
			widget.destroy()
		self.input_widgets = {}



	def reset(self):
		self.draw_sessions()
		self.controller.geometry(storedsettings.VIEWLOG_WIN_SIZE)
