import tkinter as tk



class MainMenu(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.draw_menu()

	def draw_menu(self):
		btn_timer = tk.Button(self, text="Timer", command=lambda: self.controller.show_frame('Timer'))
		btn_stopwatch = tk.Button(self, text="Stopwatch", command=lambda: self.controller.show_frame('Stopwatch'))
		btn_pomo = tk.Button(self, text="Pomodoro", command=lambda: self.controller.show_frame('Pomodoro'))
		btn_settings = tk.Button(self, text="Settings", command=lambda: self.controller.show_frame('Settings'))

		

		PADY = 5
		self.grid_columnconfigure(0, weight=1) # centers buttons in the frame
		btn_timer.grid(row=0, column=0, pady=PADY)
		btn_stopwatch.grid(row=1, column=0, pady=PADY)
		btn_pomo.grid(row=2, column=0, pady=PADY)
		btn_settings.grid(row=0, column=1, pady=PADY)

	def reset(self):
		pass


