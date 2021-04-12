import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from locals import *
import storedsettings
import pygame

from booterwidgets import *

from session import Session
from sessiondao import SessionDAO

import datetime as dt

sessiondao = SessionDAO()


class Timer(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		pygame.mixer.init()

		self.parent = parent
		
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		
		self.frame_back_button = tk.Frame(self, bg=storedsettings.APP_WIDGET_COLOR)
		self.frame_entries = tk.Frame(self, bd=3, bg=storedsettings.APP_WIDGET_COLOR)
		self.frame_buttons = tk.Frame(self, bd=3, bg=storedsettings.APP_WIDGET_COLOR)
		self.frame_timer_display = tk.Frame(self, bd=3, bg=storedsettings.APP_WIDGET_COLOR)

		self.mode = STOPPED
		self.entry_mode = TIMER

		self.frame_back_button.grid(row=0, column=0)

		self.frame_timer_display.grid(row=1, column=1)
		
		
		
		self.frame_entries.grid(row=2, column=1)
		
		self.frame_buttons.grid(row=3, column=1)
		
		


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

		# Create widgets
		btn_back = BooterButton(self.frame_back_button, text="Back", command=self.back_clicked)
		btn_back.grid(row=0, column=0, padx=10)
		btn_back.apply_back_image()

		self.lbl_task = BooterLabel(self)
		self.lbl_task.grid(row=0, column=1)
		self.display_task()


		self.entry_hours = BooterEntry(self.frame_entries, width=4)

		# Create two labels for the colons between the entries
		colon_lbls = [BooterLabel(self.frame_entries, text=":") for i in range(2)]
		
		self.entry_minutes = BooterEntry(self.frame_entries, width=4)
		self.entry_seconds = BooterEntry(self.frame_entries, width=4)

		self.entries = (self.entry_hours, self.entry_minutes, self.entry_seconds)

		self.mode_btn = BooterButton(self.frame_entries, text=self.entry_mode, font=(storedsettings.FONT, 10), command=self.mode_btn_clicked)


		self.btn_control = BooterButton(self.frame_buttons, text='Start', command=self.right_button_clicked, width=6)
		self.btn_control.bind('enter')
		self.btn_cancel = BooterButton(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.left_button_clicked)
		self.lbl_time = BooterLabel(self.frame_timer_display, text='00:00:00', fg=storedsettings.CLOCK_FG)
		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=storedsettings.CLOCK_FONT_TUPLE)

		# Bind left click to toggle clock visibility
		self.lbl_time.bind("<Button-1>", self.clock_clicked)

		# Put widgets on frame
		self.lbl_time.grid(row=0, column=0)
		self.entry_hours.grid(row=1, column=0)
		colon_lbls[0].grid(row=1, column=1)
		self.entry_minutes.grid(row=1, column=2)
		colon_lbls[1].grid(row=1, column=3)
		self.entry_seconds.grid(row=1, column=4)
		self.mode_btn.grid(row=1, column=5, padx=(15, 0))

		self.btn_cancel.grid(row=2, column=0, padx=(0, 10))
		self.btn_control.grid(row=2, column=1)


	def mode_btn_clicked(self):
		if self.entry_mode == TIMER:
			self.entry_mode = CLOCK
		elif self.entry_mode == CLOCK:
			self.entry_mode = TIMER

		self.mode_btn.config(text=self.entry_mode)

		# Enables third entry when switched to timer mode, disables it when switched to clock mode
		self.change_entries_state()



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


	def right_button_clicked(self, event=None):
		if self.mode == STOPPED:
			
			self.mode = RUNNING
			self.start_timer()

		elif self.mode == RUNNING:
			self.mode = PAUSED

		elif self.mode == PAUSED:
			self.mode = RUNNING

		self.change_control()
		self.change_entries_state()


	def change_control(self):
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


	def change_entries_state(self):
		"""Disables relevant widgets when clock runs, enables them when clock stops"""
		if self.mode == STOPPED:
			for e in self.entries:
				e.config(state=tk.NORMAL)

			# Also enable the mode button
			self.mode_btn.config(state=tk.NORMAL)

			# Third entry is disabled when in clock mode
			if self.entry_mode == CLOCK:
				self.entry_seconds.config(state=tk.DISABLED)

		else: # RUNNING or PAUSED
			for e in self.entries:
					e.config(state=tk.DISABLED)
			# Also disable the mode button
			self.mode_btn.config(state=tk.DISABLED)


	def start_timer(self):
		# Used to remember time to log when the timer ends
		if self.entry_mode == TIMER:
			self.original_time = self._get_time_entered_in_seconds()
		elif self.entry_mode == CLOCK:
			self.original_time = self._calculate_time()
		seconds = self.original_time
		if seconds > 0:
			self.end_type = AUTOMATIC
			self.timer_loop(seconds)
		else:
			self.mode = STOPPED
		self.start_time = self.get_current_time()
		self.start_date = self.get_current_date()


	def _calculate_time(self):
		"""When entry_mode is clock, user enters a clock time to run the timer till based off system clock.
		Need to calculate how many total seconds until that time and return it.
		Validates for valid clock time, assuming 24 hour clock"""
		if not self._is_entered_clock_time_valid():
			return -1 # indicates that timer shouldn't be started

		now = dt.datetime.now()
		then = self._get_entered_clock_time()
		delta = then - now

		# Deals with the scenario where the time entered is technically before the current time
		# Eg. if the time is 23:30 and you entered 00:00 because you want a timer that goes
		# till midnight, it would think you meant midnight of TODAY which would be 23h 30m in the past
		# rather than 30 minutes in the future, since "then" is created using today's date
		if delta.total_seconds() < 0:
			new_delta = dt.timedelta(days=1)
			then += new_delta
			delta = then - now

		return int(delta.total_seconds())


	def _get_entered_clock_time(self):
		"""Gets time entered in entries when entry_mode is on CLOCK. Assumes validation already completed.
		Returns a dt.time object"""
		h = int(self.entry_hours.get() or 0)
		m = int(self.entry_minutes.get() or 0)
		s = int(self.entry_seconds.get() or 0)

		return dt.datetime.now().replace(hour=h, minute=m, second=s)
		



	def _is_entered_clock_time_valid(self):
		try:
			# Check that entries either contain valid integers and aren't empty
			h = int(self.entry_hours.get())
			m = int(self.entry_minutes.get())
			# Check for valid clock times (check for negatives and out of range values)
			if h < 0 or m < 0 or h > 23 or m > 59:
				raise ValueError
			
		except ValueError:
			messagebox.showerror("Invalid Time", "Time entered must be a valid clock time (24 hour clock format)")
			return False	
	
		return True


	def left_button_clicked(self):
		self.mode = PAUSED
		ans = messagebox.askyesno('', 'Are you sure you want to cancel?')
		if ans == True:
			self.end_type = MANUAL
			self.reset_timer()
		else:
			self.mode = RUNNING
		self.change_control()
		self.change_entries_state()

	
	def _get_time_entered_in_seconds(self):
		"""Helper method that returns total number of time in seconds"""
		if not self._is_entered_time_valid():
			return -1 # indicates that timer shouldn't be started
		h = tk.IntVar()
		m = tk.IntVar()
		s = tk.IntVar()
		h.set(self.entry_hours.get() or 0)
		m.set(self.entry_minutes.get() or 0)
		s.set(self.entry_seconds.get() or 0)
		return (h.get() * 3600 + m.get() * 60 + s.get())


	def _is_entered_time_valid(self):
		try:
			int(self.entry_hours.get() or 0)
			int(self.entry_minutes.get() or 0)
			int(self.entry_seconds.get() or 0)
			
		except ValueError:
			messagebox.showerror("Invalid Time", "Time entered must be a valid time")
			return False

		times = (self.entry_hours.get(), self.entry_minutes.get(), self.entry_seconds.get())
		
		for time in times:
			if int(time or 0) < 0:
				messagebox.showerror("Invalid Time", "Time entered can't be negative")
				return False
		return True


	def timer_loop(self, seconds):
		"""seconds is the grand total number of seconds left in the timer"""
		hours_left, seconds_left = divmod(seconds, 3600) # divmod(a, b) -> (a//b, a%b) 
		minutes_left, seconds_left = divmod(seconds_left, 60)
		# Continue looping if timer is not done
		x = 0	
		if seconds != 0:
			self.time_left = seconds
			if self.mode == RUNNING:
				self._redraw_clock_label(hours_left, minutes_left, seconds_left)
				x = 1
			elif self.mode == STOPPED:
				return
			self.timer_id = self.after(storedsettings.WAIT, self.timer_loop, seconds - x)
		elif self.end_type == AUTOMATIC:
			self._play_timer_end_sound()
			self.reset_timer()
			self.change_control()
		

	def reset_timer(self):
		"""Helper to reset the timer when it runs down or is cancelled."""
		self.mode = STOPPED
		self.change_entries_state()
		self.after_cancel(self.timer_id)

		self.session_done()

		self.entry_hours.delete(0, tk.END)
		self.entry_minutes.delete(0, tk.END)
		self.entry_seconds.delete(0, tk.END)
		self._redraw_clock_label(0, 0, 0)


	def session_done(self):
		"""
		Deals with taking care of things when the timer is done.
		Depending on user settings, different things will need to happen.
		"""
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
		if storedsettings.UNTRACKED_POPUP == ON and self.end_type == AUTOMATIC:
			messagebox.showinfo("", "Timer is done")

	def tracked_session_done(self):
		"""
		Takes care of when the timer is done and a task is selected.
		Why? Depends on if the user manually ended or if time ran out 
		& if autosave is on
		"""
		# When timer is manually ended or autosave is disabled, 
		# user needs to decide whether or not to log the session
		if self.end_type == MANUAL or storedsettings.AUTOSAVE == OFF:
			# Prompt the user to save session
			ans = messagebox.askyesno("Save session?", f"{self.get_task_time_formatted()}")
			if ans:
				self.save_session()
		else: # automatic and autosave is on, so save it automatically
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
		task = self.parent.get_current_task()
		if task == self.parent.DEFAULT_TASK:
			return
		task_time = self.get_task_time_as_seconds()
		session = Session(task, task_time, self.start_time, self.start_date)
		sessiondao.insert_session(session)


	def _play_timer_end_sound(self):
		pygame.mixer.music.play()


	def _redraw_clock_label(self, h, m, s):
		new_time = "{:02}:{:02}:{:02}".format(h, m, s)
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

		time_obj = dt.time(hours, minutes, seconds)
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
		self.display_task()



def main():
	timer = Timer()
	timer.mainloop()

if __name__ == "__main__":
	main()