import tkinter as tk
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

class Settings(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.mgr = ConfigManager()
		
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		
		self.frame_settings = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_labels = tk.Frame(self.frame_settings, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_options = tk.Frame(self.frame_settings, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_example = tk.Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		self.frame_settings.grid(row=2, column=1)

		self.frame_example.grid(row=1, column=1)
		self.frame_labels.grid(row=0, column=1, padx=(0, 20))
		self.frame_options.grid(row=0, column=2)
		


		self.parent = parent

		self.save_mode = None
		self.untracked_popup_mode = None

		self.set_toggle_btns()

		self.draw_window()


	def set_toggle_btns(self):
		"""Uses saved settings to display toggle buttons with appropriate word (on/off)"""
		if storedsettings.AUTOSAVE == ON:
			self.save_mode = ON
		else:
			self.save_mode = OFF

		if storedsettings.UNTRACKED_POPUP == ON:
			self.untracked_popup_mode = ON
		else:
			self.untracked_popup_mode = OFF


		

	def draw_window(self):

		btn_back = BooterButton(self, command=self.back_clicked)
		btn_back.grid(row=0, column=0, padx=10)
		btn_back.apply_back_image()

		# BooterLabels for what each setting is for
		lbl_clock_color = BooterLabel(self.frame_settings, text="Clock Color")
		lbl_pomo_work = BooterLabel(self.frame_settings, text="Pomo Work Time")
		lbl_pomo_break = BooterLabel(self.frame_settings, text="Pomo Break Time")
		lbl_autosave = BooterLabel(self.frame_settings, text="Time Autosave")
		lbl_popup = BooterLabel(self.frame_settings, text="Untracked Popup")
		

		# Colored button for changing clock color
		self.btn_color = BooterButton(self.frame_settings, command=lambda: self.change_color("fg"))
		self.btn_color.config(bg=storedsettings.CLOCK_FG, width=3, height=1)
		# Change font size to make the color button shorter
		self.btn_color.config(font=(storedsettings.FONT, 10))
		self.btn_color.disable_hover()
		

		self.btn_autosave_option = BooterButton(self.frame_settings, 
			width=5, text=self.save_mode, command=self.autosave_clicked)

		self.btn_untracked_popup = BooterButton(self.frame_settings,
			width=5, text=self.untracked_popup_mode, command=self.untracked_popup_clicked)

		
		


		# Example clock to show how chosen color will look
		self.lbl_clock = BooterLabel(self.frame_example, text="12:34:56")
		# Have to config to override default BooterLabel options
		self.lbl_clock.config(font=storedsettings.CLOCK_FONT_TUPLE)
		self.lbl_clock.grid(row=3, column=0, sticky="N")
		# Need to config after init since BooterLabels have default colors set at initialization
		self.lbl_clock.config(fg=storedsettings.CLOCK_FG)

		# Create Entries for pomo work and break times
		ENTRY_WIDTH = 4
		self.entry_pomo_work = BooterEntry(self.frame_settings, width=ENTRY_WIDTH)
		self.entry_pomo_break = BooterEntry(self.frame_settings, width=ENTRY_WIDTH)

		# Clears current info and inserts saved settings, displayed as minutes
		self.entry_pomo_work.delete(0, END)
		self.entry_pomo_break.delete(0, END)
		self.entry_pomo_work.insert(0, storedsettings.POMO_WORK_TIME // 60)
		self.entry_pomo_break.insert(0, storedsettings.POMO_BREAK_TIME // 60)

		self.lbl_status = BooterLabel(self.frame_settings, text="")
		self.lbl_status.config(font=(storedsettings.FONT, 15, "bold"), fg="green")
		self.btn_save = BooterButton(self.frame_settings, text="Save Changes", width=14, command=self.save_clicked)


		# Grid the widgets
		lbl_clock_color.grid(row=0, column=0)
		lbl_pomo_work.grid(row=1, column=0)
		lbl_pomo_break.grid(row=2, column=0)
		lbl_autosave.grid(row=3, column=0)
		lbl_popup.grid(row=4, column=0)

		self.btn_color.grid(row=0, column=1)
		self.entry_pomo_work.grid(row=1, column=1)
		self.entry_pomo_break.grid(row=2, column=1)
		self.btn_autosave_option.grid(row=3, column=1)
		self.btn_untracked_popup.grid(row=4, column=1)
		self.lbl_status.grid(row=5, column=0, columnspan=2, pady=(20,0))

		self.btn_save.grid(row=6, column=0, columnspan=2, pady=(0,0))



	def save_clicked(self):
		if self.save_settings():
			self.indicate_saved()
		


	def save_settings(self):
		"""For when user clicks Save Changes button"""
		if not self.is_pomo_entries_valid():
			return False

		# user will enter minutes, but timer logic is in seconds, so multiply by 60
		pomo_work = int(self.entry_pomo_work.get()) * 60
		pomo_break = int(self.entry_pomo_break.get()) * 60
		self.mgr.change_setting('POMO_WORK_TIME', str(pomo_work))
		self.mgr.change_setting('POMO_BREAK_TIME', str(pomo_break))
		storedsettings.POMO_WORK_TIME = pomo_work
		storedsettings.POMO_BREAK_TIME = pomo_break

		self.mgr.change_setting("AUTOSAVE", self.save_mode)
		self.mgr.change_setting("UNTRACKED_POPUP", self.untracked_popup_mode)

		
		self.update_stored_settings()
		return True
		


	def update_stored_settings(self):
		"""
		Update storedsettings to be current
		If this isn't done, then the changed settings won't
		take effect until the program is restarted.
		"""
		storedsettings.AUTOSAVE = self.save_mode
		storedsettings.UNTRACKED_POPUP = self.untracked_popup_mode



	def indicate_saved(self):
		self.lbl_status.config(text="Changes saved!")
		self.lbl_status.after(2000, lambda: self.lbl_status.config(text=""))

	




	def is_pomo_entries_valid(self):
		"""Validates that time entered is a positive number"""
		entered = (self.entry_pomo_work.get(), self.entry_pomo_break.get())

		for e in entered:
			try:
				e = float(e)
			except ValueError:
				messagebox.showerror("Error", "Time entered must be a number")
				return False
			if float(e) < 0:
				messagebox.showerror("Error", "Time can't be negative")
				return False
			if float(e) > 59:
				messagebox.showerror("Error", "Pomo times must be under 60")
				return False
		return True


	def autosave_clicked(self):
		self.change_auto_save_mode()
		self.change_auto_save_button()


	def untracked_popup_clicked(self):
		self.change_untracked_popup_mode()
		self.change_untracked_popup_button()		

	

	def change_auto_save_mode(self):
		if self.save_mode == OFF:
			self.save_mode = ON
		else:
			self.save_mode = OFF

	def change_auto_save_button(self):
		self.btn_autosave_option.config(text=self.save_mode)
		# if self.save_mode == ON:
		# 	self.btn_autosave_option.config(text="ON")
		# else:
		# 	self.btn_autosave_option.config(text="OFF")


	def change_untracked_popup_mode(self):
		if self.untracked_popup_mode == OFF:
			self.untracked_popup_mode = ON
		else:
			self.untracked_popup_mode = OFF


	def change_untracked_popup_button(self):
		self.btn_untracked_popup.config(text=self.untracked_popup_mode)
		# if self.untracked_popup_mode == ON:
		# 	self.btn_untracked_popup.config(text="ON")
		# else:
		# 	self.btn_untracked_popup.config(text="OFF")



	def back_clicked(self):
		"""Saves settings and goes back to main menu"""
		
		self.save_settings()

		self.parent.show_frame('MainMenu')


		
	def change_color(self, option):
		# askcolor returns a tuple of format ((r, g, b) hexcode); color[1] is the hex code
		color = colorchooser.askcolor()
		if None in color:
			return
		

		# saves color to usersettings.ini
		self.mgr.change_setting('CLOCK_FG', color[1])
		# immediately changes value in storedsettings so clock's change color
		storedsettings.CLOCK_FG = color[1]
		self.btn_color.config(bg=color[1])
		self.redraw_timer()

	def redraw_timer(self):
		self.lbl_clock.config(fg=storedsettings.CLOCK_FG)

		

	def reset(self):
		pass