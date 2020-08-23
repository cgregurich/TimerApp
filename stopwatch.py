import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from locals import *
import storedsettings


from session import Session
from sessiondao import SessionDAO

sessiondao = SessionDAO()


class Stopwatch(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		
		self.controller = controller

		self.mode = STOPPED

		# Create sub-frames
		self.frame_back_button = tk.Frame(self)
		self.frame_timer_display = tk.Frame(self)
		self.frame_buttons = tk.Frame(self)

		# Put sub-frames on main frame
		self.frame_back_button.grid(row=0, column=0)
		self.frame_timer_display.grid(row=1, column=1)
		self.frame_buttons.grid(row=2, column=1)

		# Button for testing
		# tk.Button(self, text="TEST", command=self.test).grid(row=2, column=2)

		self.timer_id = None
		self.draw_clock()



	def test(self):
		"""Method for testing whatever needs to be tested"""
		print("unbinding i hope")
		self.controller.unbind('<Return>')




	def draw_clock(self):
		"""Draws buttons and display label on to main frame"""
		btn_back = tk.Button(self.frame_back_button, text="Back", command=lambda: self.controller.show_frame('MainMenu'))
		btn_back.grid(row=0, column=0)

		self.lbl_time = tk.Label(self.frame_timer_display, text='00:00:00', fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG, font=storedsettings.CLOCK_FONT)
		self.btn_cancel = tk.Button(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.cancel_button_clicked)
		self.btn_control = tk.Button(self.frame_buttons, text='Start', command=self.control_button_clicked)

		self.lbl_time.grid(row=0, column=0)
		self.btn_cancel.grid(row=0, column=0)
		self.btn_control.grid(row=0, column=1)

	def cancel_button_clicked(self):
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
		ans = messagebox.askyesno("Save session?", f"{self.get_time_spent_formatted() }")
		if ans:
			self.save_session()

		self._redraw_clock_label(0, 0, 0)
		self.after_cancel(self.timer_id)



	def control_button_clicked(self, event=None):
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


	def stopwatch_loop(self, s):
		"""Runs the stopwatch. Only stops when user stops or pauses it"""
		hours, seconds = divmod(s, 3600)
<<<<<<< HEAD
		minutes, seconds = divmod(s, 60)
=======
		minutes, seconds = divmod(seconds, 60)
>>>>>>> af89d156e64563aeca603a949d619acb0bb7332b

		x = 0
		self.time_spent = s
		if self.mode == RUNNING:
			self._redraw_clock_label(hours, minutes, seconds)
			x = 1
			
		elif self.mode == STOPPED:
			return
		self.timer_id = self.after(100, self.stopwatch_loop, s+x)

			

	def _redraw_clock_label(self, hours, minutes, seconds):
		"""Redraws timer label in format HH:MM:SS"""
		new_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
		self.lbl_time.config(text=new_time)

	def change_settings(self):
		self.lbl_time.config(fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG)



	def reset(self):
		self.change_settings()


	def get_time_spent_formatted(self):
		total_seconds = self.get_time_spent()
		hours, seconds = divmod(total_seconds, 3600)
		minutes, seconds = divmod(seconds, 60)
		return f"{hours}:{minutes}:{seconds}"

	def get_time_spent(self):
		return self.time_spent
		
	def save_session(self):
		task = self.controller.get_current_task()
		time_logged = self.get_time_spent()
		session = Session(task, time_logged)
		sessiondao.insert_session(session)

		
		



def main():
	stopwatch = Stopwatch()
	stopwatch.mainloop()


if __name__ == '__main__':
	main()
