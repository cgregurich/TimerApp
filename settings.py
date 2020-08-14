import tkinter as tk
import storedsettings
from tkinter import colorchooser
from configmanager import ConfigManager

class Settings(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.mgr = ConfigManager()

		self.controller = controller
		self.draw_window()


	def draw_window(self):
		tk.Button(self, text="Back", command=self.back_clicked).grid(row=0, column=0)
		tk.Button(self, text="Change FG", command=lambda: self.change_color("fg")).grid(row=1, column=1)
		tk.Button(self, text="Change BG", command=lambda: self.change_color("bg")).grid(row=2, column=1)

		# clock to show what selected colors will look like
		self.lbl_clock = tk.Label(self, text="12:34:56", fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG, font=storedsettings.CLOCK_FONT)
		self.lbl_clock.grid(row=1, column=2)

		# Entry widgets for work and break time in pomo timer
		self.entry_pomo_work = tk.Entry(self)
		self.entry_pomo_break = tk.Entry(self)
		self.entry_pomo_work.delete(0, tk.END)
		self.entry_pomo_break.delete(0, tk.END)
		self.entry_pomo_work.insert(0, storedsettings.POMO_WORK_TIME // 60)
		self.entry_pomo_break.insert(0, storedsettings.POMO_BREAK_TIME // 60)
		self.entry_pomo_work.grid(row=4, column=1)
		self.entry_pomo_break.grid(row=5, column=1)

		
		# button for testing
		tk.Button(self, text="TEST", command=self.test).grid(row=3, column=1)

	def back_clicked(self):
		"""Saves settings and goes back to main menu"""
		
		# user will enter minutes, but timer logic is in seconds
		pomo_work = int(self.entry_pomo_work.get()) * 60
		pomo_break = int(self.entry_pomo_break.get()) * 60
		self.mgr.change_setting('POMO_WORK_TIME', str(pomo_work))
		self.mgr.change_setting('POMO_BREAK_TIME', str(pomo_break))
		storedsettings.POMO_WORK_TIME = pomo_work
		storedsettings.POMO_BREAK_TIME = pomo_break

		self.controller.show_frame('MainMenu')


	def test(self):
		thing = self.mgr.get('SETTINGS', 'CLOCK_FG')
		print(f"thing: {thing}")

	def change_color(self, option):
		color = colorchooser.askcolor()
		if option == "fg":
			# saves color to usersettings.ini
			self.mgr.change_setting('CLOCK_FG', color[1])
			# immediately changes value in storedsettings so clock's change color
			storedsettings.CLOCK_FG = color[1]
		elif option == "bg":
			self.mgr.change_setting('CLOCK_BG', color[1])
			storedsettings.CLOCK_BG = color[1]
		self.redraw_timer()

	def redraw_timer(self):
		self.lbl_clock.config(fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG)

		




	def reset(self):
		pass
