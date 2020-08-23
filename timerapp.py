import tkinter as tk
from mainmenu import MainMenu
from timer import Timer
from stopwatch import Stopwatch
from pomodoro import Pomodoro
from settings import Settings
from tasks import Tasks





# Controller class -> Controls which frame is on top
class TimerApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.title("Productivity Time")

		self.current_task = tk.StringVar()
		self.current_task.set("--")

		

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}


		self.clocks = ("Timer", "Stopwatch", "Pomodoro")


		for gui_class in (MainMenu, Timer, Stopwatch, Pomodoro, Settings, Tasks):
			frame = gui_class(container, self)

			self.frames[gui_class.__name__] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame('MainMenu')



	def show_frame(self, gui_class):
		frame = self.frames[gui_class]
		self.change_bindings(gui_class, frame)
		frame.reset()
		frame.tkraise()



	def change_bindings(self, gui_class, frame):
		if gui_class == 'MainMenu':
			self.unbind('<Return>')
		elif gui_class in self.clocks:
			self.bind('<Return>', frame.control_button_clicked)


# NEED TO IMPLEMENT GRABBING CURRENTLY SELECT TASK!!!!!!!

	def get_current_task(self):
		return self.current_task.get()



def main():
	app = TimerApp()
	app.mainloop()

if __name__ == '__main__':
	main()



