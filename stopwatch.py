from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from locals import *
import storedsettings

from booterwidgets import *


from session import Session
from sessiondao import SessionDAO
import datetime

sessiondao = SessionDAO()


class Stopwatch(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		
		self.controller = controller

		self.mode = STOPPED

		# Create sub-frames
		self.frame_back_button = Frame(self)
		self.frame_timer_display = Frame(self)
		self.frame_buttons = Frame(self)

		# Put sub-frames on main frame
		self.frame_back_button.grid(row=0, column=0)
		self.frame_timer_display.grid(row=1, column=1)
		self.frame_buttons.grid(row=2, column=1)

		self.timer_id = None
		self.draw_clock()





	def draw_clock(self):
		"""Draws buttons and display label on to main frame"""
		btn_back = BooterButton(self.frame_back_button, text="Back", command=lambda: self.controller.show_frame('MainMenu'))
		btn_back.grid(row=0, column=0)

		self.lbl_time = BooterLabel(self.frame_timer_display, text='00:00:00', fg=storedsettings.CLOCK_FG)
		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=storedsettings.CLOCK_FONT_TUPLE)



		self.btn_cancel = BooterButton(self.frame_buttons, text='Cancel', state=DISABLED, command=self.cancel_button_clicked)
		self.btn_control = BooterButton(self.frame_buttons, text='Start', command=self.control_button_clicked, width=6)

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
		self.after_cancel(self.timer_id)
		self._redraw_clock_label(0, 0, 0)




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
			self.btn_cancel.config(state=NORMAL)
			new_control = 'Pause'
		elif self.mode == PAUSED:
			self.btn_cancel.config(state=NORMAL)
			new_control = 'Resume'
		elif self.mode == STOPPED:
			self.btn_cancel.config(state=DISABLED)
			new_control = 'Start'
		self.btn_control.config(text=new_control)

	def start_stopwatch(self):
		self.stopwatch_loop(0)


	def stopwatch_loop(self, s):
		"""Runs the stopwatch. Only stops when user stops or pauses it"""
		hours, seconds = divmod(s, 3600)

		minutes, seconds = divmod(seconds, 60)

		x = 0
		self.time_spent = s
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



	def reset(self):
		self.change_settings()


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
		# - 1 because of how the timer loop logic works, the recorded time is off by 1
		return self.time_spent - 1
		
	def save_session(self):
		task = self.controller.get_current_task()
		time_logged = self.get_time_spent_as_seconds()
		session = Session(task, time_logged)
		sessiondao.insert_session(session)

		
		



def main():
	stopwatch = Stopwatch()
	stopwatch.mainloop()


if __name__ == '__main__':
	main()
