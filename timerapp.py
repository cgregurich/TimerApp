from tkinter import *
from mainmenu import MainMenu
from timer import Timer
from stopwatch import Stopwatch
from pomodoro import Pomodoro
from settings import Settings
from tasks import Tasks
from viewlog import ViewLog
from configmanager import ConfigManager
import storedsettings




# Controller class -> Controls which frame is on top
class TimerApp(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		self.title("Productivity Time")
		self.iconbitmap("resources/images/icon.ico")
		self.resizable(False, False)


		self.current_task = StringVar()
		self.current_task.set("Select...")
		self.debug = BooleanVar()
		self.debug.set(int(ConfigManager().get_setting('SETTINGS', 'DEBUG')))
		self.configure(bg="red")
		

		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}


		self.clocks = ("Timer", "Stopwatch", "Pomodoro")


		for gui_class in (MainMenu, Timer, Stopwatch, Pomodoro, 
			Settings, Tasks, ViewLog):
			frame = gui_class(container, self)

			self.frames[gui_class.__name__] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame('MainMenu')

		



	def show_frame(self, gui_class):
		# print(f"current winsize: {self.geometry()}")
		frame = self.frames[gui_class]
		frame.configure(bg=storedsettings.APP_MAIN_COLOR)
		print()
		self.change_bindings(gui_class, frame)
		frame.reset()
		frame.tkraise()



	def change_bindings(self, gui_class, frame):
		if gui_class == 'MainMenu':
			self.unbind('<Return>')
		elif gui_class in self.clocks:
			self.bind('<Return>', frame.control_button_clicked)


	def get_current_task(self):
		return self.current_task.get()



def main():
	app = TimerApp()
	app.mainloop()

if __name__ == '__main__':
	main()



