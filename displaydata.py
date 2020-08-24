from tkinter import *
from tkinter import ttk
from session import Session
from sessiondao import SessionDAO

class DisplayData(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.frame_back = Frame(self)
		self.frame_controls = Frame(self)
		self.frame_scroll = Frame(self)

		self.frame_back.grid(row=0, column=0)
		self.frame_controls.grid(row=0, column=1)
		self.frame_scroll.grid(row=1, column=1)

		self.draw_window()

	def draw_window(self):
		btn_back = ttk.Button(self.frame_back, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
		btn_back.grid(row=0, column=0)

		btn_mnth = ttk.Button(self.frame_controls, text="Month")
		btn_day = ttk.Button(self.frame_controls, text="Day")
		btn_year = ttk.Button(self.frame_controls, text="Year")

		self.display_canvas = Canvas(self.frame_scroll)
		self.scrollbar = ttk.Scrollbar(self.frame_scroll, orient="vertical", command=self.display_canvas.yview)
		self.scrollable_frame = ttk.Frame(self.display_canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.display_canvas.configure(
				scrollregion=self.display_canvas.bbox("all")
			)
		)

		self.display_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

		self.display_canvas.configure(yscrollcommand=self.scrollbar.set)

		self.display_canvas.pack(side="left", fill="both", expand=True)
		self.scrollbar.pack(side="right", fill="y")

		self.controller.bind_all("<MouseWheel>", self._on_mousewheel)

		self.draw_sessions()

	def _on_mousewheel(self, event):
		self.display_canvas.yview_scroll(-1*(event.delta//120), "units")



	def draw_sessions(self):
		for i in range(50):
			ttk.Label(self.scrollable_frame, text="Sample scrolling label").grid(row=i, column=0)


	def reset(self):
		pass