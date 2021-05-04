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
import storedsettings
import pygame




# Controller class -> Controls which frame is on top
class TimerApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.mgr = ConfigManager()

		self.title("Productivity Time")
		self.iconbitmap("resources/images/icon.ico")
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.resizable(False, False)

		# Volume / sound setup
		self.volume = tk.IntVar()
		self.volume.set(int(self.mgr.get_setting("SETTINGS", "SOUND_VOLUME")))
		pygame.mixer.init()
		pygame.mixer.music.load("resources/sounds/dingsoundeffect.wav")
		pygame.mixer.music.set_volume(self.volume.get()/100)
		print(f"volume set to: {self.volume.get()}") # FOR TESTING, REMOVE

		self.current_task = tk.StringVar()
		self.DEFAULT_TASK = "untracked"
		self.current_task.set(self.DEFAULT_TASK)
		self.debug = tk.BooleanVar()
		self.debug.set(int(ConfigManager().get_setting('SETTINGS', 'DEBUG')))
		# self.resizable = (False, False)

		self.frames = {}


		self.clocks = ("Timer", "Stopwatch", "Pomodoro")

		self.current_frame = None


		for gui_class in (MainMenu, Timer, Stopwatch, Pomodoro, 
			Settings, Tasks, ViewLog, Goals):
			frame = gui_class(self)
			self.frames[gui_class.__name__] = frame

		self.show_frame('MainMenu')


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
		volume = int(value) / 100
		pygame.mixer.music.set_volume(volume)
		self.mgr.change_setting("SOUND_VOLUME", value)
		self.play_sound()


def main():
	app = TimerApp()
	app.mainloop()

if __name__ == '__main__':
	main()