from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from locals import *
import storedsettings
import pygame

from booterwidgets import *

from session import Session
from sessiondao import SessionDAO

import datetime

sessiondao = SessionDAO()



class Timer(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		pygame.mixer.init()

		self.controller = controller


		self.frame_back_button = Frame(self, bg=storedsettings.APP_WIDGET_COLOR)
		self.frame_entries = Frame(self, bd=3, bg=storedsettings.APP_WIDGET_COLOR)
		self.frame_buttons = Frame(self, bd=3, bg=storedsettings.APP_WIDGET_COLOR)
		self.frame_timer_display = Frame(self, bd=3, bg=storedsettings.APP_WIDGET_COLOR)

		self.mode = STOPPED

		self.frame_back_button.grid(row=0, column=0)

		self.frame_timer_display.grid(row=1, column=1)
		
		
		
		self.frame_entries.grid(row=2, column=1)
		
		self.frame_buttons.grid(row=3, column=1)
		
		


		self.end_type = None
		self.timer_id = None

		self.draw_clock()

		self.is_visible = True


	def back_clicked(self):
		self.is_visible = True
		self.controller.show_frame("MainMenu")


	def draw_clock(self):

		# Create widgets
		btn_back = BooterButton(self.frame_back_button, text="Back", command=self.back_clicked)
		btn_back.grid(row=0, column=0, padx=10)
		btn_back.apply_back_image()


		self.entry_hours = BooterEntry(self.frame_entries, width=4)

		# Create two labels for the colons between the entries
		colon_lbls = [BooterLabel(self.frame_entries, text=":") for i in range(2)]
		
		self.entry_minutes = BooterEntry(self.frame_entries, width=4)
		self.entry_seconds = BooterEntry(self.frame_entries, width=4)

		self.entries = (self.entry_hours, self.entry_minutes, self.entry_seconds)


		self.btn_control = BooterButton(self.frame_buttons, text='Start', command=self.control_button_clicked, width=6)
		self.btn_control.bind('enter')
		self.btn_cancel = BooterButton(self.frame_buttons, text='Cancel', state=DISABLED, command=self.cancel_button_clicked)
		self.lbl_time = BooterLabel(self.frame_timer_display, text='00:00:00', fg=storedsettings.CLOCK_FG)
		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=storedsettings.CLOCK_FONT_TUPLE)

		# Bind left click to toggle clock visibility
		self.lbl_time.bind("<Button-1>", self.clock_clicked)

		# Put widgets on frame
		self.lbl_time.grid(row=0, column=0)
		self.entry_hours.grid(row=1, column=1)
		colon_lbls[0].grid(row=1, column=2)
		self.entry_minutes.grid(row=1, column=3)
		colon_lbls[1].grid(row=1, column=4)
		self.entry_seconds.grid(row=1, column=5)

		

		self.btn_cancel.grid(row=2, column=0, padx=(0, 10))
		self.btn_control.grid(row=2, column=1)

	
	def clock_clicked(self, event):
		if self.is_visible:
			self.is_visible = False
			self.lbl_time.config(fg=storedsettings.APP_MAIN_COLOR)
		else:
			self.is_visible = True
			self.lbl_time.config(fg=storedsettings.CLOCK_FG)


	def control_button_clicked(self, event=None):
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
			self.btn_cancel.config(state=NORMAL)
			new_control = 'Pause'
		elif self.mode == PAUSED:
			self.btn_cancel.config(state=NORMAL)
			new_control = 'Resume'
		elif self.mode == STOPPED:
			self.btn_cancel.config(state=DISABLED)
			new_control = 'Start'
		self.btn_control.config(text=new_control)


	def change_entries_state(self):
		if self.mode == STOPPED:
			for e in self.entries:
				e.config(state=NORMAL)
		else: # RUNNING or PAUSED
			for e in self.entries:
					e.config(state=DISABLED)


	def start_timer(self):
		self.original_time = self._get_time_entered_in_seconds()
		seconds = self._get_time_entered_in_seconds()
		if seconds > 0:
			self.end_type = AUTOMATIC
			self.timer_loop(seconds)
		else:
			self.mode = STOPPED


	def cancel_button_clicked(self):
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
			return -1
		h = IntVar()
		m = IntVar()
		s = IntVar()
		h.set(self.entry_hours.get() or 0)
		m.set(self.entry_minutes.get() or 0)
		s.set(self.entry_seconds.get() or 0)

		if self.check_for_weed(h.get(), m.get(), s.get()):
			return 0
		
		elif self.sixty_nine_test(h.get(), m.get(), s.get()):
			return 0

		return (h.get() * 3600 + m.get() * 60 + s.get())

	def check_for_weed(self, h, m, s):
		if h == 420 or m == 420 or s == 420:
			pygame.mixer.music.load("resources/sounds/weed.wav")
			pygame.mixer.music.play()
			self.mode = STOPPED
			return True

		elif h == 4 and m == 20 or m == 4 and s == 20:
			pygame.mixer.music.load("resources/sounds/weed.wav")
			pygame.mixer.music.play()
			return True
			self.mode = STOPPED

		pygame.mixer.music.load("resources/sounds/dingsoundeffect.wav")
		return False


	def sixty_nine_test(self, h, m, s):
		if h == 69 or m == 69 or s == 69:
			pygame.mixer.music.load("resources/sounds/AWWW_F_YEAH.wav")
			pygame.mixer.music.play()
			return True

		elif h == 6 and m == 9 or m == 6 and s == 9:
			pygame.mixer.music.load("resources/sounds/AWWW_F_YEAH.wav")
			pygame.mixer.music.play()
			return True

		pygame.mixer.music.load("resources/sounds/dingsoundeffect.wav")
		return False


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
		if self.end_type == MANUAL or storedsettings.AUTOSAVE == '0':
			ans = messagebox.askyesno("Save session?", f"{self.get_time_spent_formatted()}")
			if ans:
				self.save_session()
		else:
			self.save_session()
		

		
		self.entry_hours.delete(0, END)
		self.entry_minutes.delete(0, END)
		self.entry_seconds.delete(0, END)
		self._redraw_clock_label(0, 0, 0)

	def save_session(self):
		task = self.controller.get_current_task()

		time_logged = self.get_time_spent_as_seconds()
		session = Session(task, time_logged)
		sessiondao.insert_session(session)

			

	def _play_timer_end_sound(self):
		pygame.mixer.music.play()


	def _redraw_clock_label(self, h, m, s):
		new_time = "{:02}:{:02}:{:02}".format(h, m, s)
		self.lbl_time.config(text=new_time)


	def change_settings(self):
		self.lbl_time.config(fg=storedsettings.CLOCK_FG)




	def get_time_spent_formatted(self):
		"""Returns time spent formatted as HH:MM:SS"""
		time_obj = self.get_time_spent()
		return time_obj.strftime("%H:%M:%S")

	def get_time_spent(self):
		"""Returns a datetime.time object"""
		total_seconds = self.get_time_spent_as_seconds()
		hours, seconds = divmod(total_seconds, 3600)
		minutes, seconds = divmod(seconds, 60)

		time_obj = datetime.time(hours, minutes, seconds)
		return time_obj

	def get_time_spent_as_seconds(self):
		if self.end_type == MANUAL:
			# - 1 because of how the timer loop logic works, the recorded time is off by 1
			self.time_spent = self.original_time - self.time_left - 1
		elif self.end_type == AUTOMATIC:
			self.time_spent = self.original_time
		return self.time_spent


	def reset(self):
		self.change_settings()
		self.controller.geometry(storedsettings.TIMER_WIN_SIZE)



def main():
	timer = Timer()
	timer.mainloop()

if __name__ == "__main__":
	main()