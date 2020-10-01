from tkinter import *
from tkinter import ttk
from locals import *
import storedsettings
from tkinter import colorchooser
from configmanager import ConfigManager

from booterwidgets import *



from tkinter import *
from tkinter import ttk
from locals import *
import storedsettings
from tkinter import colorchooser
from configmanager import ConfigManager

class Settings(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.mgr = ConfigManager()
		

		self.frame_settings = Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_labels = Frame(self.frame_settings, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_options = Frame(self.frame_settings, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_example = Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_settings.grid(row=1, column=1)

		self.frame_labels.grid(row=1, column=1)
		self.frame_options.grid(row=1, column=2)
		self.frame_example.grid(row=0, column=1)


		self.controller = controller

		if storedsettings.AUTOSAVE == '1':
			self.save_mode = ON
		else:
			self.save_mode = OFF

		self.draw_window()

		

	def draw_window(self):
		PADY = 5

		btn_back = BooterButton(self, command=self.back_clicked)
		btn_back.grid(row=0, column=0, padx=10)
		btn_back.apply_back_image()

		# BooterLabels for what each setting is for
		BooterLabel(self.frame_labels, text="Clock Color").grid(row=1, column=0, pady=PADY)
		BooterLabel(self.frame_labels, text="Pomo Work Time").grid(row=3, column=0, pady=PADY)
		BooterLabel(self.frame_labels, text="Pomo Break Time").grid(row=4, column=0, pady=PADY)
		BooterLabel(self.frame_labels, text="Time Autosave").grid(row=5, column=0, pady=PADY)

		# Colored buttons for changing clock colors
		self.btn_fg = BooterButton(self.frame_options, command=lambda: self.change_color("fg"))
		self.btn_fg.config(bg=storedsettings.CLOCK_FG, width=3, height=1)
		self.btn_fg.disable_hover()
		

		self.btn_save_op = BooterButton(self.frame_options, width=10, text=self.save_mode.upper(), command=self.autosave_clicked)
		self.btn_save_op.config(height=1)
		self.btn_fg.grid(row=1, column=0, pady=PADY)
		self.btn_save_op.grid(row=4, column=0, pady=PADY)


		# Example clock to show how chosen colors will look
		
		self.lbl_clock = BooterLabel(self.frame_example, text="12:34:56")
		# Have to config to override default BooterLabel options
		self.lbl_clock.config(font=storedsettings.CLOCK_FONT_TUPLE)
		self.lbl_clock.grid(row=3, column=0, sticky="N")
		# Need to config after init since BooterLabels have default colors set at initialization
		self.lbl_clock.config(fg=storedsettings.CLOCK_FG)

		# Create Entries for pomo work and break times
		self.entry_pomo_work = BooterEntry(self.frame_options)
		self.entry_pomo_break = BooterEntry(self.frame_options)
		# Clears current info and inserts saved settings, displayed as minutes
		self.entry_pomo_work.delete(0, END)
		self.entry_pomo_break.delete(0, END)
		self.entry_pomo_work.insert(0, storedsettings.POMO_WORK_TIME // 60)
		self.entry_pomo_break.insert(0, storedsettings.POMO_BREAK_TIME // 60)
		self.entry_pomo_work.grid(row=2, column=0, pady=PADY)
		self.entry_pomo_break.grid(row=3, column=0, pady=PADY)


	def autosave_clicked(self):
		self.change_auto_save_mode()
		self.change_auto_save_button()
	

	def change_auto_save_mode(self):
		if self.save_mode == OFF:
			self.save_mode = ON
		else:
			self.save_mode = OFF

	def change_auto_save_button(self):
		if self.save_mode == ON:
			self.btn_save_op.config(text='ON')
		else:
			self.btn_save_op.config(text='OFF')

	def back_clicked(self):
		"""Saves settings and goes back to main menu"""
		
		# user will enter minutes, but timer logic is in seconds, so multiply by 60
		pomo_work = int(self.entry_pomo_work.get()) * 60
		pomo_break = int(self.entry_pomo_break.get()) * 60
		self.mgr.change_setting('POMO_WORK_TIME', str(pomo_work))
		self.mgr.change_setting('POMO_BREAK_TIME', str(pomo_break))
		storedsettings.POMO_WORK_TIME = pomo_work
		storedsettings.POMO_BREAK_TIME = pomo_break

		if self.save_mode == ON:
			self.mgr.change_setting('AUTOSAVE', str(1))
			storedsettings.AUTOSAVE = '1'
		else:
			self.mgr.change_setting('AUTOSAVE', str(0))
			storedsettings.AUTOSAVE = '0'

		self.controller.show_frame('MainMenu')


		
	def change_color(self, option):
		# askcolor returns a tuple of format ((r, g, b) hexcode); color[1] is the hex code
		color = colorchooser.askcolor()
		if None in color:
			return
		

		# saves color to usersettings.ini
		self.mgr.change_setting('CLOCK_FG', color[1])
		# immediately changes value in storedsettings so clock's change color
		storedsettings.CLOCK_FG = color[1]
		self.btn_fg.config(bg=color[1])
		self.redraw_timer()

	def redraw_timer(self):
		self.lbl_clock.config(fg=storedsettings.CLOCK_FG)

		

	def reset(self):
		self.controller.geometry(storedsettings.SETTINGS_WIN_SIZE)