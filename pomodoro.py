import tkinter as tk
from tkinter import ttk
from stopwatch import Stopwatch
from locals import *
import storedsettings
from tkinter import messagebox
from booterwidgets import *
from session import Session
from sessiondao import SessionDAO
import datetime as dt


sessiondao = SessionDAO()


class Pomodoro(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent

		self.config(bg=storedsettings.APP_MAIN_COLOR)
		
		self.frame_back_button = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_timer_display = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.grid_rowconfigure(0, weight=1)
		self.frame_back_button.grid_columnconfigure(1, weight=1)
		self.frame_back_button.grid(row=0, column=0, sticky="nsew")
		self.frame_timer_display.grid(row=1, column=0)
		self.frame_buttons.grid(row=2, column=0, pady=(10, 0))

		self.pomo_mode = WORK
		self.mode = STOPPED

		self.end_type = None

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
		btn_back.grid(row=0, column=0)
		btn_back.apply_back_image()

		self.lbl_task = BooterLabel(self.frame_back_button)
		self.lbl_task.grid(row=0, column=1, padx=(10,0))
		self.display_task()

		self.lbl_time = BooterLabel(self.frame_timer_display, text='00:00', fg=storedsettings.CLOCK_FG)

		# Bind left click to toggle clock visibility
		self.lbl_time.bind("<Button-1>", self.clock_clicked)

		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=storedsettings.CLOCK_FONT_TUPLE)
		self.btn_left = BooterButton(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.left_button_clicked)
		self.btn_right = BooterButton(self.frame_buttons, text='Start', command=self.right_button_clicked, width=6)

		self.lbl_time.grid(row=0, column=0)
		self.btn_left.grid(row=0, column=0, padx=(0,10))
		self.btn_right.grid(row=0, column=1)


	def display_task(self):
		task = self.parent.get_current_task()
		self.lbl_task.config(text=task)


	def clock_clicked(self, event):
		if self.is_visible:
			self.is_visible = False
			self.lbl_time.config(fg=storedsettings.APP_MAIN_COLOR)
		else:
			self.is_visible = True
			self.lbl_time.config(fg=storedsettings.CLOCK_FG)


	def right_button_clicked(self, event=None):
		# Right button is for starting/pausing/resuming
		# start timer
		prev_mode = self.change_mode_right()
		if prev_mode == STOPPED:
			self.start_timer()

		self.display_message()


		# make button text match the state of the timer
		self.change_control()

	def display_message(self):
		"""
		Tells user what clock time the timer will be done at. This occurs
		when the user starts the timer, or resumes the timer after it's 
		paused.
		"""
		if self.mode == RUNNING:
			lbl = BooterLabel(self, text=self.create_endtime_message())
			lbl.place(relx=0.5, rely=0.625, anchor=tk.CENTER)
			lbl.config(font=(storedsettings.FONT, 12))
			self.after(2000, lbl.destroy)

	def create_endtime_message(self):
		"""
		get the time left on the timer.
		use that to calculate what time it will be when that much
		time has elapsed. display this time in an HH:MM format.
		"""
		now = dt.datetime.now()
		delta = dt.timedelta(seconds=self.time_left)
		time_str = (now + delta).strftime("Ends at %H:%M")
		return time_str


	def change_mode_right(self):
		"""For when the right button is clicked and 
		the timer's mode needs to be altered accordingly
		Returns the mode when this function was called"""
		prev_mode = self.mode
		# Start timer
		if self.mode == STOPPED:
			self.mode = RUNNING

		# Pause timer
		elif self.mode == RUNNING:
			self.mode = PAUSED
		
		# Resume timer
		elif self.mode == PAUSED:
			self.mode = RUNNING
		return prev_mode


	def left_button_clicked(self):
		"""Left button is for cancelling/skipping
		Asks user """

		prev_mode = self.mode
		self.mode = PAUSED

		# Prompt user with different prompt depending on pomo mode
		if self.pomo_mode == WORK:
			msg = 'Are you sure you want to cancel this pomo?'
		else: # in break mode
			msg = 'Are you sure you want to skip this break?'
		ans = messagebox.askyesno('', msg)

		# If yes, reset timer, go to next pomo mode
		if ans == True:
			self.end_type = MANUAL
			self.reset_timer()
			if self.pomo_mode == BREAK:
				self.change_pomo_mode()
		else:
			self.mode = prev_mode
		self.change_control()



	def change_pomo_mode(self):
		if self.pomo_mode == WORK:
			self.pomo_mode = BREAK
		else:
			self.pomo_mode = WORK



	def change_control(self):
		self.change_left_button_text()

		# Change state of cancel button and
		# change text of control button
		if self.mode == RUNNING:
			self.btn_left.config(state=tk.NORMAL)
			new_control = 'Pause'

		elif self.mode == PAUSED:
			self.btn_left.config(state=tk.NORMAL)
			new_control = 'Resume'

		elif self.mode == STOPPED:
			if self.pomo_mode == BREAK:
				self.btn_left.config(state=tk.NORMAL)
			else:
				self.btn_left.config(state=tk.DISABLED)
			new_control = 'Start'
		self.btn_right.config(text=new_control)
	

	def change_left_button_text(self):
		# Make left button's text match the state of the timer
		if self.pomo_mode == BREAK:
			self.btn_left.config(text="Skip")
		else:
			self.btn_left.config(text="Cancel")


	def start_timer(self):
		seconds = storedsettings.POMO_WORK_TIME if self.pomo_mode == WORK else storedsettings.POMO_BREAK_TIME
		self.original_time = seconds
		self.end_type = AUTOMATIC
		self.timer_loop(seconds)
		self.start_time = self.get_current_time()
		self.start_date = self.get_current_date()


	def timer_loop(self, seconds):
		minutes_left, seconds_left = divmod(seconds, 60)

		x = 0
		self.time_left = seconds
		if seconds != 0:
			if self.mode == RUNNING:
				self._redraw_clock_label(minutes_left, seconds_left)
				x = 1
			elif self.mode == STOPPED:
				return
			self.timer_id = self.after(storedsettings.WAIT, self.timer_loop, seconds - x)
		elif self.end_type == AUTOMATIC:
			if self.pomo_mode != BREAK:
				self.get_task_time()
			self._play_timer_end_sound()
			self.reset_timer()
			self.change_pomo_mode()
			self.change_control()
	

	def _play_timer_end_sound(self):
		self.parent.play_sound()


	def _redraw_clock_label(self, m, s):
		new_time = "{:02}:{:02}".format(m, s)
		self.lbl_time.config(text=new_time)


	def change_settings(self):
		self.lbl_time.config(fg=storedsettings.CLOCK_FG)


	def reset_timer(self):
		"""
		"""
		self.mode = STOPPED
		self.after_cancel(self.timer_id)
		self.session_done()
		self._redraw_clock_label(0,0)


	def session_done(self):
		"""
		Deals with taking care of things when the timer is done.
		Depending on user settings, different things will need to happen.
		"""
		# Nothing to do for a break being done
		if self.pomo_mode == BREAK:
			return
		if self.parent.get_current_task() == self.parent.DEFAULT_TASK:
			self.untracked_session_done()
		else:
			self.tracked_session_done()
		

	def untracked_session_done(self):
		"""
		Takes care of when the timer is done and no task is selected.
		Why? Depends on if the user wants there to be a popup notification when 
		an untracked session is done
		"""

		# Display notification if setting is enabled, however only
		# when the user didn't manually end the timer.
		if storedsettings.UNTRACKED_POPUP == ON and self.end_type == AUTOMATIC:
			messagebox.showinfo("Popup", "Pomodoro is done")


	def tracked_session_done(self):
		"""
		Takes care of when the timer is done and a task is selected.
		Why? Depends on if the user manually ended or if time ran out 
		& if autosave is on
		"""
		if self.end_type == MANUAL or storedsettings.AUTOSAVE == OFF:
			# Prompt user to save session
			ans = messagebox.askyesno("Save session?", f"{self.get_task_time_formatted()}")
			if ans: # user wants to save session
				self.save_session()
		else: # automatic pomo end and autosave is on
			self.save_session()


	def get_current_time(self):
		"""Returns string of current time in format HH:MM"""
		now = dt.datetime.now()
		return now.strftime("%H:%M")


	def get_current_date(self):
		"""Returns string of current date in format MM-DD-YY"""
		today = dt.datetime.now()
		return today.strftime("%m-%d-%y")


	def save_session(self):
		"""Creates a Session object with the clock's time 
		and saves it to the database."""
		task = self.parent.get_current_task()
		if task == self.parent.DEFAULT_TASK:
			return
		task_time = self.get_task_time_as_seconds()
		session = Session(task, task_time, self.start_time, self.start_date)
		sessiondao.insert_session(session)

		
	def get_task_time_formatted(self):
		"""Returns time spent formatted as MM:SS"""
		time_obj = self.get_task_time()
		return time_obj.strftime("%M:%S")


	def get_task_time(self):
		"""Returns a datetime.time object"""
		total_seconds = self.get_task_time_as_seconds()
		minutes, seconds = divmod(total_seconds, 60)
		time_obj = dt.time(0, minutes, seconds)
		return time_obj


	def get_task_time_as_seconds(self):
		if self.end_type == MANUAL:
			# - 1 because of how the timer loop logic works, the recorded time is off by 1
			self.task_time = self.original_time - self.time_left - 1
		elif self.end_type == AUTOMATIC:
			self.task_time = self.original_time
		return self.task_time


	def reset(self):
		self.change_settings()
		# self.parent.geometry(storedsettings.POMO_WIN_SIZE)
		self.display_task()


def main():
	pomo = Pomodoro()
	pomo.mainloop()

if __name__ == '__main__':
	main()