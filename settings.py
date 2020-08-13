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
		tk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainMenu")).grid(row=0, column=0)
		tk.Button(self, text="Change FG", command=lambda: self.change_color("fg")).grid(row=1, column=1)
		tk.Button(self, text="Change BG", command=lambda: self.change_color("bg")).grid(row=2, column=1)

		self.lbl_clock = tk.Label(self, text="12:34:56", fg=storedsettings.CLOCK_FG, bg=storedsettings.CLOCK_BG, font=storedsettings.CLOCK_FONT)
		self.lbl_clock.grid(row=1, column=2)

		
		
		# button for testing
		tk.Button(self, text="TEST", command=self.test).grid(row=3, column=1)

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
