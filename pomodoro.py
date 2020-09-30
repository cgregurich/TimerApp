from tkinter import *
from tkinter import ttk
from stopwatch import Stopwatch
from locals import *
import storedsettings
import pygame
from tkinter import messagebox

from booterwidgets import *

from session import Session
from sessiondao import SessionDAO

import datetime

sessiondao = SessionDAO()


class Pomodoro(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		
		self.controller = controller
		pygame.mixer.init()
		pygame.mixer.music.load("resources/sounds/dingsoundeffect.wav")


		self.frame_back_button = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_timer_display = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons = Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_back_button.grid(row=0, column=0)
		self.frame_timer_display.grid(row=1, column=1)
		self.frame_buttons.grid(row=2, column=1)

		self.pomo_mode = WORK
		self.mode = STOPPED

		self.end_type = None

		self.timer_id = None

		self.draw_clock()


	def draw_clock(self):
		"""Draws buttons and display label on to main frame"""
		btn_back = BooterButton(self.frame_back_button, command=lambda: self.controller.show_frame('MainMenu'))
		btn_back.grid(row=0, column=0)
		btn_back.apply_back_image()

		self.lbl_time = BooterLabel(self.frame_timer_display, text='00:00', fg=storedsettings.CLOCK_FG)
		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=storedsettings.CLOCK_FONT_TUPLE)
		self.btn_cancel = BooterButton(self.frame_buttons, text='Cancel', state=DISABLED, command=self.cancel_button_clicked)
		self.btn_control = BooterButton(self.frame_buttons, text='Start', command=self.control_button_clicked, width=6)

		self.lbl_time.grid(row=0, column=0)
		self.btn_cancel.grid(row=0, column=0, padx=(0,10))
		self.btn_control.grid(row=0, column=1)

		# button for testing
		# BooterButton(self, text="Change pomo mode", command=self.change_pomo_mode).grid(row=3, column=0)




	def control_button_clicked(self, event=None):
		if self.mode == STOPPED:
			
			self.mode = RUNNING
			self.start_timer()

		elif self.mode == RUNNING:
			self.mode = PAUSED

		elif self.mode == PAUSED:
			self.mode = RUNNING

		self.change_control()


	def cancel_button_clicked(self):
		self.mode = PAUSED
		if self.pomo_mode == WORK:
			msg = 'Are you sure you want to cancel this pomo?'
		else:
			msg = 'Are you sure you want to skip this break?'
		ans = messagebox.askyesno('', msg)
		if ans == True:
			self.end_type = MANUAL
			self.reset_timer()
			if self.pomo_mode == BREAK:
				self.change_pomo_mode()
		else:
			self.mode = RUNNING
		self.change_control()


	def change_control(self):
		# Switch from break to work or vice versa, 
		# change text of cancel button
		if self.pomo_mode == BREAK:
			self.btn_cancel.config(text="Skip")
		else:
			self.btn_cancel.config(text="Cancel")

		# Change state of cancel button and
		# change text of control button
		if self.mode == RUNNING:
			self.btn_cancel.config(state=NORMAL)
			new_control = 'Pause'
		elif self.mode == PAUSED:
			self.btn_cancel.config(state=NORMAL)
			new_control = 'Resume'
		elif self.mode == STOPPED:
			if self.pomo_mode == BREAK:
				self.btn_cancel.config(state=NORMAL)
			else:
				self.btn_cancel.config(state=DISABLED)
			new_control = 'Start'
		self.btn_control.config(text=new_control)


	def start_timer(self):
		self.change_sound_file()

		seconds = storedsettings.POMO_WORK_TIME if self.pomo_mode == WORK else storedsettings.POMO_BREAK_TIME
		self.original_time = seconds
		self.end_type = AUTOMATIC
		self.timer_loop(seconds)


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
				self.get_time_spent()
			self._play_timer_end_sound()
			self.reset_timer()
			self.change_pomo_mode()
			self.change_control()
	

	def change_pomo_mode(self):
		if self.pomo_mode == WORK:
			self.pomo_mode = BREAK
		else:
			self.pomo_mode = WORK


	def _play_timer_end_sound(self):
		pygame.mixer.music.play()


	def _redraw_clock_label(self, m, s):
		new_time = "{:02}:{:02}".format(m, s)
		self.lbl_time.config(text=new_time)

	def change_settings(self):
		self.lbl_time.config(fg=storedsettings.CLOCK_FG)

	def reset(self):
		self.change_settings()
		self.controller.geometry(storedsettings.POMO_WIN_SIZE)


	def reset_timer(self):
		self.mode = STOPPED
		self.after_cancel(self.timer_id)
		if self.pomo_mode == WORK:
			if self.end_type == MANUAL or storedsettings.AUTOSAVE == '0':
				ans = messagebox.askyesno("Save session?", f"{self.get_time_spent_formatted()}")
				if ans:
					self.save_session()
			else:
				self.save_session()
		self._redraw_clock_label(0,0)

		# self.change_sound_file()


	def change_sound_file(self):
		if self.pomo_mode == BREAK:
			pygame.mixer.music.load("resources/sounds/break_done.wav")
		elif self.pomo_mode == WORK:
			pygame.mixer.music.load("resources/sounds/dingsoundeffect.wav")




	def save_session(self):
		"""Creates a Session object with the clock's time 
		and saves it to the database."""
		task = self.controller.get_current_task()
		time_logged = self.get_time_spent_as_seconds()
		session = Session(task, time_logged)
		sessiondao.insert_session(session)

		

	def get_time_spent_formatted(self):
		"""Returns time spent formatted as MM:SS"""
		time_obj = self.get_time_spent()
		return time_obj.strftime("%M:%S")


	def get_time_spent(self):
		"""Returns a datetime.time object"""
		total_seconds = self.get_time_spent_as_seconds()
		minutes, seconds = divmod(total_seconds, 60)
		time_obj = datetime.time(0, minutes, seconds)
		return time_obj

	def get_time_spent_as_seconds(self):
		if self.end_type == MANUAL:
			# - 1 because of how the timer loop logic works, the recorded time is off by 1
			self.time_spent = self.original_time - self.time_left - 1
		elif self.end_type == AUTOMATIC:
			self.time_spent = self.original_time
		return self.time_spent


def main():
	pomo = Pomodoro()
	pomo.mainloop()

if __name__ == '__main__':
	main()