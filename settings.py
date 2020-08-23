import tkinter as tk
from locals import *
import storedsettings
from tkinter import colorchooser
from configmanager import ConfigManager

class Settings(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.mgr = ConfigManager()


		self.frame_labels = tk.Frame(self)
		self.frame_options = tk.Frame(self)
		self.frame_example = tk.Frame(self)


		self.frame_labels.grid(row=1, column=1)
		self.frame_options.grid(row=1, column=2)
		self.frame_example.grid(row=1, column=3)


		self.controller = controller
		self.draw_window()

		if storedsettings.AUTOSAVE == '1':
			self.save_mode = ON
		else:
			self.save_mode = OFF

	def draw_window(self):
		PADY = 5

		tk.Button(self, text="Back", command=self.back_clicked).grid(row=0, column=0)

		# Labels for what each setting is for
		tk.Label(self.frame_labels, text="Background").grid(row=0, column=0, pady=PADY)
		tk.Label(self.frame_labels, text="Foreground").grid(row=1, column=0, pady=PADY)
		tk.Label(self.frame_labels, text="Pomo Work Time").grid(row=3, column=0, pady=PADY)
		tk.Label(self.frame_labels, text="Pomo Break Time").grid(row=4, column=0, pady=PADY)
		tk.Label(self.frame_labels, text="Time Autosave").grid(row=5, column=0, pady=PADY)

		# Colored buttons for changing clock colors
		self.btn_fg = tk.Button(self.frame_options, bg=storedsettings.CLOCK_FG, width=3, command=lambda: self.change_color("fg"))
		self.btn_bg = tk.Button(self.frame_options, bg=storedsettings.CLOCK_BG, width=3, command=lambda: self.change_color("bg"))
		self.btn_save_op = tk.Button(self.frame_options, width=3, text='ON', command=self.autosave_clicked)
		self.btn_bg.grid(row=0, column=0, pady=PADY)
		self.btn_fg.grid(row=1, column=0, pady=PADY)
		self.btn_save_op.grid(row=4, column=0, pady=PADY)


		# Example clock to show how chosen colors will look
		self.lbl_clock = tk.Label(self.frame_example, text="12:34:56", fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG, font=storedsettings.CLOCK_FONT)
		self.lbl_clock.grid(row=3, column=0, sticky="N")

		# Create Entries for pomo work and break times
		self.entry_pomo_work = tk.Entry(self.frame_options)
		self.entry_pomo_break = tk.Entry(self.frame_options)
		# Clears current info and inserts saved settings, displayed as minutes
		self.entry_pomo_work.delete(0, tk.END)
		self.entry_pomo_break.delete(0, tk.END)
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

		print(storedsettings.AUTOSAVE)

		
	def change_color(self, option):
		# askcolor returns a tuple of format ((r, g, b) hexcode); color[1] is the hex code
		color = colorchooser.askcolor()
		if None in color:
			return
		
		if option == "fg":
			# saves color to usersettings.ini
			self.mgr.change_setting('CLOCK_FG', color[1])
			# immediately changes value in storedsettings so clock's change color
			storedsettings.CLOCK_FG = color[1]
			self.btn_fg.config(bg=color[1])
		elif option == "bg":
			self.mgr.change_setting('CLOCK_BG', color[1])
			storedsettings.CLOCK_BG = color[1]
			self.btn_bg.config(bg=color[1])
		self.redraw_timer()

	def redraw_timer(self):
		self.lbl_clock.config(fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG)

		

	def reset(self):
		pass
