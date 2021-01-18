import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from locals import *
import storedsettings

from booterwidgets import *


from session import Session
from sessiondao import SessionDAO
import datetime

sessiondao = SessionDAO()


class Stopwatch(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		
		self.parent = parent

		self.config(bg=storedsettings.APP_MAIN_COLOR)

		self.mode = STOPPED

		# Create sub-frames
		self.frame_back_button = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_timer_display = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		# Put sub-frames on main frame
		self.frame_back_button.grid(row=0, column=0)
		self.frame_timer_display.grid(row=1, column=1)
		self.frame_buttons.grid(row=2, column=1)

		self.timer_id = None
		self.draw_clock()

		self.is_visible = True

		# For keeping track of current time of day at start of session
		self.start_time = None

		# For keeping track of current date at start of session (in case session 
		# begins at around 00:00 so the date won't be counted as the "next" day)
		self.start_date = None


	def back_clicked(self):
		self.is_visible = True
		self.parent.show_frame("MainMenu")


	def draw_clock(self):
		"""Draws buttons and display label on to main frame"""
		btn_back = BooterButton(self.frame_back_button, command=self.back_clicked)
		btn_back.grid(row=0, column=0, padx=10)
	
		btn_back.apply_back_image()

		self.lbl_task = BooterLabel(self)
		self.lbl_task.grid(row=0, column=1)
		self.display_task()

		self.lbl_time = BooterLabel(self.frame_timer_display, text='00:00:00', fg=storedsettings.CLOCK_FG)
		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=storedsettings.CLOCK_FONT_TUPLE)

		# Bind left click to toggle clock visibility
		self.lbl_time.bind("<Button-1>", self.clock_clicked)

		self.btn_cancel = BooterButton(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.left_button_clicked)
		self.btn_control = BooterButton(self.frame_buttons, text='Start', command=self.right_button_clicked, width=6)

		self.lbl_time.grid(row=1, column=0)
		self.btn_cancel.grid(row=0, column=0, padx=(0,10))
		self.btn_control.grid(row=0, column=1)
		

	def display_task(self):
		task = self.parent.get_current_task()
		if task != "Select...":
			self.lbl_task.config(text=task)


	def clock_clicked(self, event):
		if self.is_visible:
			self.is_visible = False
			self.lbl_time.config(fg=storedsettings.APP_MAIN_COLOR)
		else:
			self.is_visible = True
			self.lbl_time.config(fg=storedsettings.CLOCK_FG)


	def left_button_clicked(self):
		"""Prompts user to confirm stopping timer. Displays message and waits
		for user's answer"""
		self.mode = PAUSED
		ans = messagebox.askyesno(message="Are you sure you want to cancel?")
		if ans:
			self.reset_clock()
		else:
			self.mode = RUNNING
		self.change_control()

	def reset_clock(self):
		self.mode = STOPPED
		ans = messagebox.askyesno("Save session?", f"{self.get_task_time_formatted() }")
		if ans:
			self.save_session()
		self.after_cancel(self.timer_id)
		self._redraw_clock_label(0, 0, 0)


	def right_button_clicked(self, event=None):
		"""Changes mode and control button text when the control button is clicked"""
		if self.mode == STOPPED:
			self.mode = RUNNING
			self.start_stopwatch()

		elif self.mode == RUNNING:
			self.mode = PAUSED

		elif self.mode == PAUSED:
			self.mode = RUNNING

		self.change_control()


	def change_control(self):
		"""Changes text of control button based on what current mode is"""
		if self.mode == RUNNING:
			self.btn_cancel.config(state=tk.NORMAL)
			new_control = 'Pause'
		elif self.mode == PAUSED:
			self.btn_cancel.config(state=tk.NORMAL)
			new_control = 'Resume'
		elif self.mode == STOPPED:
			self.btn_cancel.config(state=tk.DISABLED)
			new_control = 'Start'
		self.btn_control.config(text=new_control)


	def start_stopwatch(self):
		self.stopwatch_loop(0)
		self.start_time = self.get_current_time()
		self.start_date = self.get_current_date()


	def get_current_time(self):
		"""Returns string of current time in format HH:MM"""
		now = datetime.datetime.now()
		return now.strftime("%H:%M")


	def get_current_date(self):
		"""Returns string of current date in format MM-DD-YY"""
		today = datetime.datetime.now()
		return today.strftime("%m-%d-%y")




	def stopwatch_loop(self, s):
		"""Runs the stopwatch. Only stops when user stops or pauses it"""
		hours, seconds = divmod(s, 3600)
		minutes, seconds = divmod(seconds, 60)
		x = 0
		self.task_time = s
		if self.mode == RUNNING:
			self._redraw_clock_label(hours, minutes, seconds)
			x = 1
			
		elif self.mode == STOPPED:
			return
		self.timer_id = self.after(storedsettings.WAIT, self.stopwatch_loop, s+x)


	def _redraw_clock_label(self, hours, minutes, seconds):
		"""Redraws timer label in format HH:MM:SS"""
		new_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
		self.lbl_time.config(text=new_time)


	def change_settings(self):
		self.lbl_time.config(fg=storedsettings.CLOCK_FG)


	def get_task_time_formatted(self):
		"""Returns time spent formatted as HH:MM:SS"""
		time_obj = self.get_task_time()
		return time_obj.strftime("%H:%M:%S")

	def get_task_time(self):
		"""Returns a datetime.time object"""
		total_seconds = self.get_task_time_as_seconds()
		hours, seconds = divmod(total_seconds, 3600)
		minutes, seconds = divmod(seconds, 60)
		time_obj = datetime.time(hours, minutes, seconds)
		return time_obj

	def get_task_time_as_seconds(self):
		# - 1 because of how the timer loop logic works, the recorded time is off by 1
		return self.task_time - 1
		
	def save_session(self):
		task = self.parent.get_current_task()
		if task == self.parent.DEFAULT_TASK:
			return
		task_time = self.get_task_time_as_seconds()
		session = Session(task, task_time, self.start_time, self.start_date)
		sessiondao.insert_session(session)

		
	def reset(self):
		self.change_settings()
		# self.parent.geometry(storedsettings.STOPWATCH_WIN_SIZE)
		self.display_task()



def main():
	stopwatch = Stopwatch()
	stopwatch.mainloop()


if __name__ == '__main__':
	main()
