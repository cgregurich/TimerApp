import tkinter as tk
from mainmenu import MainMenu
from timer import Timer
from stopwatch import Stopwatch
from pomodoro import Pomodoro
from settings import Settings
from tasks import Tasks
from viewlog import ViewLog
from goals import Goals
from configmanager import ConfigManager
from crashmanager import CrashManager
import storedsettings
import pygame





# Controller class -> Controls which frame is on top
class TimerApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.cfg_mgr = ConfigManager()

		self.title("Productivity Time")
		self.iconbitmap("resources/images/icon.ico")
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		# self.resizable(False, False)

		# Volume / sound setup
		self.volume = tk.IntVar()
		self.volume.set(int(self.cfg_mgr.get_setting("SETTINGS", "SOUND_VOLUME")))
		pygame.mixer.init()
		pygame.mixer.music.load("resources/sounds/dingsoundeffect.wav")
		pygame.mixer.music.set_volume(self.volume.get()/100)

		self.current_task = tk.StringVar()
		self.DEFAULT_TASK = "untracked"
		self.current_task.set(self.DEFAULT_TASK)
		self.debug = tk.BooleanVar()
		self.debug.set(int(ConfigManager().get_setting('SETTINGS', 'DEBUG')))
		self.resizable(False, False)

		self.frames = {}

		self.clocks = ("Timer", "Stopwatch", "Pomodoro")

		self.current_frame = None

		for gui_class in (MainMenu, Timer, Stopwatch, Pomodoro, 
			Settings, Tasks, ViewLog, Goals):
			frame = gui_class(self)
			self.frames[gui_class.__name__] = frame

		self.show_frame('MainMenu')

		self.crash_mgr = CrashManager()
		self.crash_mgr.check_for_crash()


	def show_frame(self, gui_class):
		if self.current_frame: self.current_frame.grid_forget()
		self.current_frame = self.frames[gui_class]
		self.change_bindings(gui_class, self.current_frame)
		self.current_frame.reset()
		self.current_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
		self.geometry("")
		self.current_frame.focus_set()



	def change_bindings(self, gui_class, frame):
		if gui_class == 'MainMenu':
			self.unbind('<Return>')
		elif gui_class in self.clocks:
			self.bind('<Return>', frame.right_button_clicked)


	def get_current_task(self):
		return self.current_task.get()

	def play_sound(self):
		"""Plays the timer end sound"""
		pygame.mixer.music.play()

	def volume_changed(self, value=None):
		"""Saves the new volume in usersettings.ini, sets the mixer's volume, then plays the ding sound so the user can test the new volume."""
		volume = int(value) / 100
		pygame.mixer.music.set_volume(volume)
		self.play_sound()

	def toggle_debug(self):
		debug = self.debug.get()
		storedsettings.WAIT = 10 if debug else 1000 # changes timescales
		cur_value = self.cfg_mgr.get_setting('SETTINGS', 'DEBUG')
		new_value = '1' if cur_value == '0' else '0'
		self.cfg_mgr.change_setting('DEBUG', new_value)
		storedsettings.WAIT = 1000 if new_value == '0' else '10'
		if debug:
			self.resizable(True, True)
		else:
			self.resizable(False, False)


def main():
	app = TimerApp()
	app.mainloop()

if __name__ == '__main__':
	main()