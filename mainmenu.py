from tkinter import *
from tkinter import ttk
from taskdao import TaskDAO
from booterwidgets import *

import storedsettings

from configmanager import ConfigManager

taskdao = TaskDAO()


class MainMenu(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.ran = False
		self.mgr = ConfigManager()

		self.frame_buttons = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons.grid(row=0, column=0)

		self.draw_menu()

	def draw_menu(self):
		BUTTON_WIDTH = 12
		lbl_task = BooterLabel(self.frame_buttons, text="What are you working on?")
		lbl_task.bold()

		# None is used as a dummy value; this version of the OM is never seen, just used as initialization
		self.om_current_task = BooterOptionMenu(self.frame_buttons, self.controller.current_task, None)
		# Clears the blank space created by dummy data None
		self.om_current_task['menu'].delete(0, END)

		btn_settings = BooterButton(self.frame_buttons, text="SETTINGS".title(), command=lambda: self.controller.show_frame('Settings'), width=BUTTON_WIDTH)
		btn_settings.apply_settings_image()
		btn_tasks = BooterButton(self.frame_buttons, text="TASKS".title(), command=lambda: self.controller.show_frame("Tasks"), width=BUTTON_WIDTH)
		btn_stopwatch = BooterButton(self.frame_buttons, text="STOPWATCH".title(), command=lambda: self.controller.show_frame('Stopwatch'), width=BUTTON_WIDTH)
		btn_pomo = BooterButton(self.frame_buttons, text="POMODORO".title(), command=lambda: self.controller.show_frame('Pomodoro'), width=BUTTON_WIDTH)
		btn_timer = BooterButton(self.frame_buttons, text="TIMER".title(), command=lambda: self.controller.show_frame('Timer'), width=BUTTON_WIDTH)
		btn_displaydata = BooterButton(self.frame_buttons, text="VIEW LOG".title(), command=lambda: self.controller.show_frame('ViewLog'), width=BUTTON_WIDTH)
		check_debug = BooterCheckbutton(self.frame_buttons, text="DEBUG", variable=self.controller.debug, command=self.check_clicked)
		


		PADY = 6
		lbl_task.grid            (row=0, column=0)
		self.om_current_task.grid(row=1, column=0, pady=(0, PADY*3))
		
		btn_tasks.grid           (row=2, column=0, pady=PADY)
		btn_stopwatch.grid       (row=3, column=0, pady=PADY)
		btn_pomo.grid            (row=4, column=0, pady=PADY)
		btn_timer.grid           (row=5, column=0, pady=PADY)
		btn_displaydata.grid     (row=6, column=0, pady=PADY)
		btn_settings.grid        (row=7, column=0, pady=PADY)
		check_debug.grid         (row=8, column=0)
	
		self.grid_columnconfigure(0, weight=1) # centers buttons in the frame

		
	def refresh_option_menu(self):
		menu = self.om_current_task['menu']
		tasks = taskdao.get_all_tasks()
		menu.delete(0, END)
		if not tasks:
			menu.add_command(label="No Tasks")

		else:
			
			
			for task in tasks:
				menu.add_command(label=task, command=lambda value=task: self.controller.current_task.set(value))



	def check_clicked(self):
		debug = self.controller.debug.get()
		storedsettings.WAIT = 10 if debug else 1000
		cur_value = self.mgr.get_setting('SETTINGS', 'DEBUG')
		new_value = '1' if cur_value == '0' else '0'
		self.mgr.change_setting('DEBUG', new_value)
		storedsettings.WAIT = 1000 if new_value == '0' else '10'
		if debug:
			self.controller.resizable(True, True)
		else:
			self.controller.resizable(False, False)
		

		

	def reset(self):
		self.refresh_option_menu()
		self.controller.geometry(storedsettings.MAINMENU_WIN_SIZE)