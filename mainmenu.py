from tkinter import *
from tkinter import ttk
from taskdao import TaskDAO

import storedsettings

from configmanager import ConfigManager

taskdao = TaskDAO()


class MainMenu(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.ran = False
		self.mgr = ConfigManager()

		self.frame_buttons = Frame(self)
		self.frame_buttons.grid(row=0, column=0)

		self.draw_menu()

	def draw_menu(self):
		
		btn_settings = ttk.Button(self.frame_buttons, text="Settings", command=lambda: self.controller.show_frame('Settings'))
		btn_tasks = ttk.Button(self.frame_buttons, text="Tasks", command=lambda: self.controller.show_frame("Tasks"))
		btn_stopwatch = ttk.Button(self.frame_buttons, text="Stopwatch", command=lambda: self.controller.show_frame('Stopwatch'))
		btn_pomo = ttk.Button(self.frame_buttons, text="Pomodoro", command=lambda: self.controller.show_frame('Pomodoro'))
		btn_timer = ttk.Button(self.frame_buttons, text="Timer", command=lambda: self.controller.show_frame('Timer'))
		btn_displaydata = ttk.Button(self.frame_buttons, text="Display Data", command=lambda: self.controller.show_frame("DisplayData"))
		check_debug = Checkbutton(self.frame_buttons, text="DEBUG", variable=self.controller.debug, command=self.check_clicked)
		lbl_task = Label(self.frame_buttons, text="What are you working on?")
		self.om_current_task = ttk.OptionMenu(self.frame_buttons, self.controller.current_task, "--",  *taskdao.get_all_tasks())


		PADY = 0
		btn_settings.grid(row=0, column=0, pady=PADY)
		btn_tasks.grid(row=1, column=0, pady=PADY)
		btn_stopwatch.grid(row=2, column=0, pady=PADY)
		btn_pomo.grid(row=3, column=0, pady=PADY)
		btn_timer.grid(row=4, column=0, pady=PADY)
		btn_displaydata.grid(row=5, column=0, pady=PADY)
		check_debug.grid(row=6, column=0)
		lbl_task.grid(row=7, column=0)
		self.om_current_task.grid(row=8, column=1)



		self.grid_columnconfigure(0, weight=1) # centers buttons in the frame
		
		
	def refresh_option_menu(self):
		self.om_current_task.destroy()
		self.om_current_task = ttk.OptionMenu(self, self.controller.current_task, self.controller.current_task.get(),  *taskdao.get_all_tasks())
		self.om_current_task.grid(row=1, column=0)

	def check_clicked(self):
		debug = self.controller.debug.get()
		storedsettings.WAIT = 10 if debug else 1000
		cur_value = self.mgr.get_setting('SETTINGS', 'DEBUG')
		new_value = '1' if cur_value == '0' else '0'
		self.mgr.change_setting('DEBUG', new_value)
		storedsettings.WAIT = 1000 if new_value == '0' else '10'

		

	def reset(self):
		self.refresh_option_menu()
		


