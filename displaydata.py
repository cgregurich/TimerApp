from tkinter import *
from tkinter import ttk
from locals import *
from session import Session
from sessiondao import SessionDAO
import datetime as dt
from datetime import date
from tkcalendar import *

sessiondao = SessionDAO()

class DisplayData(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.frame_back = Frame(self)
		self.frame_controls = Frame(self)
		self.frame_scroll = Frame(self)
		self.frame_bottom_scrollbar = Frame(self)

		self.frame_back.grid(row=0, column=0)
		self.frame_controls.grid(row=0, column=1)
		self.frame_scroll.grid(row=1, column=1)
		self.frame_bottom_scrollbar.grid(row=2, column=1)

		self.session_rows = [] # list of lists of labels

		self.draw_window()

	def draw_window(self):
		btn_back = ttk.Button(self.frame_back, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
		btn_back.grid(row=0, column=0)


		# FRAME CONTROLS

		self.rb_var = StringVar()
		self.rb_var.set(DAY)
		rb_day = Radiobutton(self.frame_controls, text="Day", variable=self.rb_var, value=DAY)
		rb_week = Radiobutton(self.frame_controls, text="Week", variable=self.rb_var, value=WEEK)
		rb_month = Radiobutton(self.frame_controls, text="Month", variable=self.rb_var, value=MONTH)
		rb_task = Radiobutton(self.frame_controls, text="Task", variable=self.rb_var, value=TASK)

		rb_day.grid(row=0, column=0)
		rb_week.grid(row=0, column=1)
		rb_month.grid(row=0, column=2)
		rb_task.grid(row=0, column=3)

		today = dt.datetime.now()
		self.cal = DateEntry(self.frame_controls, selectmode="day", year=today.year, month=today.month, day=today.day)
		self.cal.grid(row=1, column=0)
		self.btn_test = ttk.Button(self.frame_controls, text="test", command=self.draw_sessions)
		self.btn_test.grid(row=1, column=1)

		self.display_canvas = Canvas(self.frame_scroll)
		self.scrollbar = ttk.Scrollbar(self.frame_scroll, orient="vertical", command=self.display_canvas.yview)
		self.sideways_scrollbar = ttk.Scrollbar(self.frame_bottom_scrollbar, orient="horizontal", command=self.display_canvas.xview)
		self.scrollable_frame = ttk.Frame(self.display_canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.display_canvas.configure(
				scrollregion=self.display_canvas.bbox("all")
			)
		)

		self.display_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

		self.display_canvas.configure(yscrollcommand=self.scrollbar.set)
		self.display_canvas.configure(xscrollcommand=self.sideways_scrollbar.set)

		self.display_canvas.pack(side="left", fill="both", expand=True)
		self.scrollbar.pack(side="right", fill="y")
		self.sideways_scrollbar.pack(side="bottom", fill="x")

		self.controller.bind_all("<MouseWheel>", self._on_mousewheel)

		self.draw_sessions()

	def _on_mousewheel(self, event):
		self.display_canvas.yview_scroll(-1*(event.delta//120), "units")


	def grab_date_from_cal(self):
		"""Returns the current selected date as a datetime.datetime.date obj"""
		date_str = self.cal.get()
		date_info = [int(i) for i in date_str.split('/')]
		month, day, year = tuple(date_info)
		year += 2000
		date_obj = dt.datetime(year, month, day).date()
		return date_obj
		

	def draw_sessions(self):
		self._clear_screen()
		# check what mode (selected day, last 7, last 30, selected task)
		if self.rb_var.get() == DAY:
			all_sessions = self.get_selected_day_sessions()
		elif self.rb_var.get() == WEEK:
			pass

		elif self.rb_var.get() == MONTH:
			pass

		elif self.rb_var.get() == TASK:
			pass


		self.draw_sessions_to_screen(all_sessions)
		
	def _calc_col_widths(self, all_sessions):
		"""Calculates how wide each column should be depending
		on the Session objects' data given in the arg all_sessions"""
		self.col_widths = [0, 0, 0, 0]
		for s in all_sessions:
			s_info = s.get_info_for_display()
			for i in range(len(self.col_widths)):
				if len(s_info[i]) > self.col_widths[i]:
					self.col_widths[i] = len(s_info[i])

		PADDING = 2
		for i in range(len(self.col_widths)):
			self.col_widths[i] += PADDING







	def draw_sessions_to_screen(self, all_sessions):
		"""sessions is a list of Session objects"""
		self._calc_col_widths(all_sessions)
		for s in all_sessions:
			row = self.create_session_row(s)
			self.session_rows.append(row)
			self._draw_row(row)
		
				


	def get_selected_day_sessions(self):	
		day = self.grab_date_from_cal()
		selected_day_sessions = sessiondao.get_all_sessions_from_date(day)

		return selected_day_sessions
	
	def create_session_row(self, session):
		"""Receives Session obj as arg.
		Returns a list of lists of labels"""
		info = session.get_info_for_display()
		row = [Label(self.scrollable_frame, text=info[i], width=self.col_widths[i], font=MONOSPACED) for i in range(len(self.col_widths))]
		return row

	def _draw_row(self, row):
		r = len(self.session_rows)
		c = 0
		for lbl in row:
			lbl.grid(row=r, column=c)
			c += 1



	def _clear_screen(self):
		for row in self.session_rows:
			for lbl in row:
				lbl.destroy()



	def reset(self):
		self.draw_sessions()
