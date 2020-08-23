import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from locals import *
import storedsettings
import pygame

from session import Session
from sessiondao import SessionDAO

sessiondao = SessionDAO()



class Timer(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller = controller
		
		self.time_save = 'Yes'

		pygame.mixer.init()

		self.mode = STOPPED
		self.frame_back_button = tk.Frame(self)
		self.frame_back_button.grid(row=0, column=0)
		self.frame_entries = tk.Frame(self, bd=3)
		self.frame_entries.grid(row=0, column=1)
		self.frame_buttons = tk.Frame(self, bd=3)
		self.frame_buttons.grid(row=1, column=1)
		self.frame_timer_display = tk.Frame(self, bd=3)
		self.frame_timer_display.grid(row=2, column=1)
		self.end_type = None


		self.draw_clock()


	def draw_clock(self):

		# Create widgets
		btn_back = tk.Button(self.frame_back_button, text="Back", command=lambda: self.controller.show_frame('MainMenu'))
		btn_back.grid(row=0, column=0)

		self.entry_hours = tk.Entry(self.frame_entries)
		self.entry_minutes = tk.Entry(self.frame_entries)
		self.entry_seconds = tk.Entry(self.frame_entries)

		self.entries = (self.entry_hours, self.entry_minutes, self.entry_seconds)


		self.btn_control = tk.Button(self.frame_buttons, text='Start', command=self.control_button_clicked)
		self.btn_control.bind('enter')
		self.btn_cancel = tk.Button(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.cancel_button_clicked)
		self.lbl_time = tk.Label(self.frame_timer_display, text='00:00:00', fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG, font=storedsettings.CLOCK_FONT)


		# Put widgets on frame
		self.entry_hours.grid(row=0, column=0)
		self.entry_minutes.grid(row=0, column=1)
		self.entry_seconds.grid(row=0, column=2)

		self.btn_cancel.grid(row=0, column=0, padx=(0, 10))
		self.btn_control.grid(row=0, column=1)

		self.lbl_time.grid(row=0, column=0)



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
		if self.mode == STOPPED:
			for e in self.entries:
				e.config(state=tk.NORMAL)
		else: # RUNNING or PAUSED
			for e in self.entries:
					e.config(state=tk.DISABLED)


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
		h = tk.IntVar()
		m = tk.IntVar()
		s = tk.IntVar()
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
			pygame.mixer.music.load("resources/sounds/weed.mp3")
			pygame.mixer.music.play()
			self.mode = STOPPED
			return True

		elif h == 4 and m == 20 or m == 4 and s == 20:
			pygame.mixer.music.load("resources/sounds/weed.mp3")
			pygame.mixer.music.play()
			return True
			self.mode = STOPPED

		pygame.mixer.music.load("resources/sounds/dingsoundeffect.mp3")
		return False


	def sixty_nine_test(self, h, m, s):
		if h == 69 or m == 69 or s == 69:
			pygame.mixer.music.load("resources/sounds/AWWW_F_YEAH.mp3")
			pygame.mixer.music.play()
			return True

		elif h == 6 and m == 9 or m == 6 and s == 9:
			pygame.mixer.music.load("resources/sounds/AWWW_F_YEAH.mp3")
			pygame.mixer.music.play()
			return True

		pygame.mixer.music.load("resources/sounds/dingsoundeffect.mp3")
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
				self._redraw_clock_label(0, 0, 0)
				return
			self.after(10, self.timer_loop, seconds - x)
		elif self.end_type == AUTOMATIC:
			print(self.get_time_spent())
			self._play_timer_end_sound()
			self.reset_timer()
			self.change_control()
		

	def reset_timer(self):
		"""Helper to reset the timer when it runs down or is cancelled."""
		self.mode = STOPPED
		self.change_entries_state()

		if storedsettings.AUTO_SAVE == 0:
			ans = messagebox.showyesno("Would you like to log this time?", f"{self.get_time_spent}")
			if ans:
				self.save_session()
		else:
			self.save_session()
		self.lbl_time.config(text="00:00:00")
		self.entry_hours.delete(0, tk.END)
		self.entry_minutes.delete(0, tk.END)
		self.entry_seconds.delete(0, tk.END)

	def save_session(self):
		task = self.controller.get_current_task()
		time_logged = self.get_time_spent()
		session = Session(task, time_logged)
		sessiondao.insert_session(session)

			

	def _play_timer_end_sound(self):
		pygame.mixer.music.play()


	def _redraw_clock_label(self, h, m, s):
		new_time = "{:02}:{:02}:{:02}".format(h, m, s)
		self.lbl_time.config(text=new_time)

	def destroy_widgets(self):
		self.entry_hours.destroy()
		self.entry_minutes.destroy()
		self.entry_seconds.destroy()
		self.btn_control.destroy()
		self.btn_cancel.destroy()
		self.lbl_time.destroy()

	def change_settings(self):
		self.lbl_time.config(fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG)



	def reset(self):
		self.change_settings()

	def get_time_spent(self):
		if self.end_type == MANUAL:
			self.time_spent = self.original_time - self.time_left
		elif self.end_type == AUTOMATIC:
			self.time_spent = self.original_time
		return self.time_spent




def main():
	timer = Timer()
	timer.mainloop()

if __name__ == "__main__":
	main()