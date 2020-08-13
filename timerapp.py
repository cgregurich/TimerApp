import tkinter as tk
from mainmenu import MainMenu
from timer import Timer
from stopwatch import Stopwatch
from pomodoro import Pomodoro
from settings import Settings




class TimerApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.title("Productivity Time")

		

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (MainMenu, Timer, Stopwatch, Pomodoro, Settings):
			frame = F(container, self)

			self.frames[F.__name__] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame('MainMenu')

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.reset()
		frame.tkraise()

def main():
	app = TimerApp()
	app.mainloop()

if __name__ == '__main__':
	main()



