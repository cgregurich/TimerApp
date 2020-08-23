from tkinter import *
from tkinter import ttk
from taskdao import TaskDAO


taskdao = TaskDAO()


class MainMenu(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.ran = False
		self.draw_menu()

	def draw_menu(self):
		btn_timer = ttk.Button(self, text="Timer", command=lambda: self.controller.show_frame('Timer'))
		btn_stopwatch = ttk.Button(self, text="Stopwatch", command=lambda: self.controller.show_frame('Stopwatch'))
		btn_pomo = ttk.Button(self, text="Pomodoro", command=lambda: self.controller.show_frame('Pomodoro'))
		btn_settings = ttk.Button(self, text="Settings", command=lambda: self.controller.show_frame('Settings'))
		btn_activities = ttk.Button(self, text="Tasks", command=lambda: self.controller.show_frame("Tasks"))
		self.om_current_task = ttk.OptionMenu(self, self.controller.current_task, "--",  *taskdao.get_all_tasks())
		lbl_task = Label(self, text="What are you working on?")
		

		PADY = 5
		self.grid_columnconfigure(0, weight=1) # centers buttons in the frame
		lbl_task.grid(row=0, column=0)
		self.om_current_task.grid(row=1, column=0)
		btn_timer.grid(row=2, column=0, pady=PADY)
		btn_stopwatch.grid(row=3, column=0, pady=PADY)
		btn_pomo.grid(row=4, column=0, pady=PADY)
		btn_settings.grid(row=0, column=1, pady=PADY)
		btn_activities.grid(row=3, column=1, pady=PADY)
		
	def refresh_option_menu(self):
		self.om_current_task.destroy()
		self.om_current_task = ttk.OptionMenu(self, self.controller.current_task, "--",  *taskdao.get_all_tasks())
		self.om_current_task.grid(row=1, column=0)

	def reset(self):
		self.refresh_option_menu()
		


