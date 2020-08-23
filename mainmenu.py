import tkinter as tk
from taskdao import TaskDAO

taskdao = TaskDAO()


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
		btn_activities = tk.Button(self, text="Tasks", command=lambda: self.controller.show_frame("Tasks"))
		om_current_task = tk.OptionMenu(self, self.controller.current_task ,*taskdao.get_all_tasks())
		lbl_task = tk.Label(self, text="What are you working on?")
		

		PADY = 5
		self.grid_columnconfigure(0, weight=1) # centers buttons in the frame
		lbl_task.grid(row=0, column=0)
		om_current_task.grid(row=1, column=0, pady=PADY)
		btn_timer.grid(row=2, column=0, pady=PADY)
		btn_stopwatch.grid(row=3, column=0, pady=PADY)
		btn_pomo.grid(row=4, column=0, pady=PADY)
		btn_settings.grid(row=0, column=1, pady=PADY)
		btn_activities.grid(row=3, column=1, pady=PADY)
		

	def reset(self):
		pass


