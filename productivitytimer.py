import tkinter as tk

class Timer(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.gridit()

	def gridit(self):
		self.hours = tk.Entry(self)
		self.minutes = tk.Entry(self)
		self.seconds = tk.Entry(self)
		self.hours.grid(row=0, column=0)
		self.minutes.grid(row=0, column=1)
		self.seconds.grid(row=0, column=2)
		self.btn_start = tk.Button(self, text='Start!')
		self.btn_start['command'] = self.record
		self.btn_start.grid(row=1, column=1)

	def record(self):
		h = tk.IntVar()
		m = tk.IntVar()
		s = tk.IntVar()
		h.set(self.hours.get())
		m.set(self.minutes.get())
		s.set(self.seconds.get())
		print(f'{h.get()}\n{m.get()}\n{s.get()}\n')

timer = Timer(tk.Tk())
timer.grid()
timer.mainloop()