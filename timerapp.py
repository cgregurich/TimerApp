from tkinter import *
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




# Controller class -> Controls which frame is on top
class TimerApp(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		self.title("Productivity Time")
		self.iconbitmap("resources/images/icon.ico")
		self.config(bg=storedsettings.APP_MAIN_COLOR)

		self.current_task = StringVar()
		self.DEFAULT_TASK = "untracked"
		self.current_task.set(self.DEFAULT_TASK)
		self.debug = BooleanVar()
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


	def change_bindings(self, gui_class, frame):
		if gui_class == 'MainMenu':
			self.unbind('<Return>')
		elif gui_class in self.clocks:
			self.bind('<Return>', frame.right_button_clicked)


	def get_current_task(self):
		return self.current_task.get()


def main():
	app = TimerApp()
	app.mainloop()

if __name__ == '__main__':
	main()