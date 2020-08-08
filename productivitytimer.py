import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Timer(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		

		self.RUNNING = "running"
		self.STOPPED = "stopped"
		self.PAUSED = "paused"
		self.timer_mode = self.STOPPED
		self.frame_entries = tk.Frame(self, bd=3)
		self.frame_entries.grid(row=0, column=0)
		self.frame_buttons = tk.Frame(self, bd=3)
		self.frame_buttons.grid(row=1, column=0)
		self.frame_timer_display = tk.Frame(self, bd=3)
		self.frame_timer_display.grid(row=2, column=0)

		self.draw_timer()



	def draw_timer(self):

		# Create widgets
		self.entry_hours = tk.Entry(self.frame_entries)
		self.entry_minutes = tk.Entry(self.frame_entries)
		self.entry_seconds = tk.Entry(self.frame_entries)

		self.btn_control = tk.Button(self.frame_buttons, text='Start', command=self.control_button_clicked)
		self.btn_cancel = tk.Button(self.frame_buttons, text='Cancel', state=tk.DISABLED, command=self.cancel_button_clicked)
		self.lbl_time = tk.Label(self.frame_timer_display, text='00:00:00', fg='light blue', bg='black', font=("Consolas", 24, "bold"))


		# Put widgets on frame
		self.entry_hours.grid(row=0, column=0)
		self.entry_minutes.grid(row=0, column=1)
		self.entry_seconds.grid(row=0, column=2)

		self.btn_cancel.grid(row=0, column=0, padx=(0, 10))
		self.btn_control.grid(row=0, column=1)

		self.lbl_time.grid(row=0, column=0)

	def control_button_clicked(self):

		if self.timer_mode == self.STOPPED:
			self.timer_mode = self.RUNNING
			self.start_timer()
		elif self.timer_mode == self.RUNNING:
			self.timer_mode = self.PAUSED
			# pause the timer
		elif self.timer_mode == self.PAUSED:
			self.timer_mode = self.RUNNING
			#resume the timer
		self.change_control()

	def change_control(self):
		if self.timer_mode == self.RUNNING:
			self.btn_cancel.config(state=tk.NORMAL)
			new_control = 'Pause'
		elif self.timer_mode == self.PAUSED:
			self.btn_cancel.config(state=tk.NORMAL)
			new_control = 'Resume'
		elif self.timer_mode == self.STOPPED:
			self.btn_cancel.config(state=tk.DISABLED)
			new_control = 'Start'
		self.btn_control.config(text=new_control)

	def start_timer(self):
		seconds = self._get_time_entered_in_seconds()
		if seconds > 0:
			self.timer_loop(seconds)
		else:
			self.timer_mode = self.STOPPED

	def cancel_button_clicked(self):
		prompt = messagebox.askyesno(message='Are you sure you want to cancel?')
		if prompt == True:
			self.timer_mode = self.STOPPED
			self.lbl_time.config(text="00:00:00")
			self.entry_hours.delete(0, tk.END)
			self.entry_minutes.delete(0, tk.END)
			self.entry_seconds.delete(0, tk.END)
		self.change_control()



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
		return (h.get() * 3600 + m.get() * 60 + s.get())

	def _is_entered_time_valid(self):
		try
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
			if self.timer_mode == self.RUNNING:
				self._redraw_timer_label(hours_left, minutes_left, seconds_left)
				x = 1
			elif self.timer_mode == self.STOPPED:
				seconds = 0


			self.after(1000, self.timer_loop, seconds - x)

		


	def _redraw_timer_label(self, h, m, s):
		new_time = "{:02}:{:02}:{:02}".format(h, m, s)
		self.lbl_time.config(text=new_time)


def main():
	timer = Timer()
	timer.mainloop()

if __name__ == "__main__":
	main()