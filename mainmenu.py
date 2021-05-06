import tkinter as tk
from tkinter import ttk
from taskdao import TaskDAO
from booterwidgets import *

import storedsettings

from configmanager import ConfigManager

taskdao = TaskDAO()


class MainMenu(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		print(f"parent: {parent}" )
		print(f"type(parent): {type(parent)}")
		self.parent = parent

		self.config(bg=storedsettings.APP_MAIN_COLOR)

		self.ran = False
		self.mgr = ConfigManager()

		self.frame_buttons = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_buttons.grid(row=0, column=0)

		self.draw_menu()

	def draw_menu(self):
		BUTTON_WIDTH = 12
		lbl_task = BooterLabel(self.frame_buttons, text="What are you working on?")
		lbl_task.config(font=(storedsettings.FONT, 12, "bold"))

		# None is used as a dummy value; this version of the OM is never seen, just used as initialization
		self.om_current_task = BooterOptionMenu(self.frame_buttons, self.parent.current_task, None)
		# Clears the blank space created by dummy data None
		self.om_current_task['menu'].delete(0, tk.END)

		btn_goals = BooterButton(self.frame_buttons, text="GOALS".title(), command=lambda: self.parent.show_frame("Goals"), width=BUTTON_WIDTH)
		btn_settings = BooterButton(self.frame_buttons, text="SETTINGS".title(), command=lambda: self.parent.show_frame("Settings"), width=BUTTON_WIDTH)
		btn_settings.apply_settings_image()
		btn_tasks = BooterButton(self.frame_buttons, text="TASKS".title(), command=lambda: self.parent.show_frame("Tasks"), width=BUTTON_WIDTH)
		btn_stopwatch = BooterButton(self.frame_buttons, text="STOPWATCH".title(), command=lambda: self.parent.show_frame("Stopwatch"), width=BUTTON_WIDTH)
		btn_pomo = BooterButton(self.frame_buttons, text="POMODORO".title(), command=lambda: self.parent.show_frame("Pomodoro"), width=BUTTON_WIDTH)
		btn_timer = BooterButton(self.frame_buttons, text="TIMER".title(), command=lambda: self.parent.show_frame("Timer"), width=BUTTON_WIDTH)
		btn_displaydata = BooterButton(self.frame_buttons, text="VIEW LOG".title(), command=lambda: self.parent.show_frame("ViewLog"), width=BUTTON_WIDTH)
		
		# check_debug = BooterCheckbutton(self.frame_buttons, text="DEBUG", variable=self.parent.debug, command=self.check_clicked)
		


		PADY = 6
		lbl_task.grid            (row=0, column=0)
		self.om_current_task.grid(row=1, column=0, pady=(0, PADY*3))
		
		btn_goals.grid           (row=2, column=0, pady=PADY)
		btn_tasks.grid           (row=3, column=0, pady=PADY)
		btn_stopwatch.grid       (row=4, column=0, pady=PADY)
		btn_pomo.grid            (row=5, column=0, pady=PADY)
		btn_timer.grid           (row=6, column=0, pady=PADY)
		btn_displaydata.grid     (row=7, column=0, pady=PADY)
		btn_settings.grid        (row=8, column=0, pady=PADY)
		# check_debug.grid         (row=9, column=0)
	
		self.grid_columnconfigure(0, weight=1) # centers buttons in the frame

		
	def refresh_option_menu(self):
		prev_task = self.parent.get_current_task()
		menu = self.om_current_task['menu']
		tasks = taskdao.get_all_tasks()
		menu.delete(0, tk.END)
		# Add command for the default task (i.e. "untracked") so it can be selected
		menu.add_command(label=self.parent.DEFAULT_TASK, command=lambda arg=self.parent.DEFAULT_TASK: self.parent.current_task.set(arg))

		# Fills option menu with tasks
		if tasks:
			for task in tasks:
				menu.add_command(label=task, command=lambda arg=task: self.parent.current_task.set(arg))		
		# Takes care of when the selected task is deleted; selected task will go back to default task (i.e. "untracked")
		if prev_task not in tasks:
			self.parent.current_task.set(self.parent.DEFAULT_TASK)


	def check_clicked(self):
		self.parent.toggle_debug()
		

		

	def reset(self):
		self.refresh_option_menu()