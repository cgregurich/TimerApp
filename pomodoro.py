import tkinter as tk
from tkinter import ttk
from stopwatch import Stopwatch
from locals import *
import storedsettings
import pygame
from tkinter import messagebox


class Pomodoro(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.controller = controller
		pygame.mixer.init()
		pygame.mixer.music.load("resources/sounds/dingsoundeffect.mp3")


		self.frame_back_button = tk.Frame(self)
		self.frame_timer_display = tk.Frame(self)
		self.frame_buttons = tk.Frame(self)

		self.frame_back_button.grid(row=0, column=0)
		self.frame_timer_display.grid(row=1, column=1)
		self.frame_buttons.grid(row=2, column=1)

		self.pomo_mode = WORK
		self.mode = STOPPED

		self.end_type = None

		self.draw_clock()


	def draw_clock(self):
		"""Draws buttons and display label on to main frame"""
		tk.Button(self.frame_back_button, text="Back", command=lambda: self.controller.show_frame('MainMenu')).grid(row=0, column=0)

		self.lbl_time = tk.Label(self.frame_timer_display, text='00:00', fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG, font=storedsettings.CLOCK_FONT)
		self.btn_cancel = tk.Button(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.cancel_button_clicked)
		self.btn_control = tk.Button(self.frame_buttons, text='Start', command=self.control_button_clicked)

		self.lbl_time.grid(row=0, column=0)
		self.btn_cancel.grid(row=0, column=0)
		self.btn_control.grid(row=0, column=1)





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
			if self.pomo_mode == BREAK:
				self.change_pomo_mode()
			self.end_type = MANUAL
			self.reset_timer()
		else:
			self.mode = RUNNING
		self.change_control()


	def change_control(self):
		if self.mode == RUNNING:
			if self.pomo_mode == BREAK:
				self.btn_cancel.config(text="Skip")
			else:
				self.btn_cancel.config(text="Cancel")
			self.btn_cancel.config(state=tk.NORMAL)
			new_control = 'Pause'
		elif self.mode == PAUSED:
			self.btn_cancel.config(state=tk.NORMAL)
			new_control = 'Resume'
		elif self.mode == STOPPED:
			self.btn_cancel.config(state=tk.DISABLED)
			new_control = 'Start'
		self.btn_control.config(text=new_control)


	def start_timer(self):
		seconds = storedsettings.POMO_WORK_TIME if self.pomo_mode == WORK else storedsettings.POMO_BREAK_TIME
		self.end_type = AUTOMATIC
		self.timer_loop(seconds)


	def timer_loop(self, seconds):
		minutes_left, seconds_left = divmod(seconds, 60)

		x = 0
		if seconds != 0:
			if self.mode == RUNNING:
				self._redraw_clock_label(minutes_left, seconds_left)
				x = 1
			elif self.mode == STOPPED:
				seconds = 0
				self._redraw_clock_label(0, 0)
				return
			self.after(1000, self.timer_loop, seconds - x)
		elif self.end_type == AUTOMATIC:
			self._play_timer_end_sound()
			self.reset_timer()
			self.change_control()
			self.change_pomo_mode()


	def reset_timer(self):
		self.mode = STOPPED
		self._redraw_clock_label(0,0)


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
		self.lbl_time.config(fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG)

	def reset(self):
		self.change_settings()

def main():
	pomo = Pomodoro()
	pomo.mainloop()

if __name__ == '__main__':
	main()