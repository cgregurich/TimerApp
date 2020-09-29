from tkinter import *
import storedsettings

import PIL
from PIL import ImageTk, Image

"""Module for making custom widgets that I can easily set/modify the default properties for
in order to make the application more styled.
All of these widgets inherit from the base Tkinter widgets of 
the same name (minus 'Booter')"""




# Honorable mentions for fonts
# font = "Bahnschrift Light"
# font = "Nirmala UI Semilight"




class BooterButton(Button):
	def __init__(self, *args, **kwargs):
		Button.__init__(self, *args, **kwargs)

		# Default settings for the widget
		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)
		self.config(relief=SOLID)

		self.config(disabledforeground=storedsettings.DISABLED_FONT_COLOR)


		self.config(height=0)


		self.FONT_SIZE = 17

		self.config(font=(storedsettings.FONT, self.FONT_SIZE))


		self.bind("<Enter>", self.hover)
		self.bind("<Leave>", self.leave)

	def hover(self, event):
		# Only indicate hover if button is not disabled
		if self['state'] == NORMAL:
			self.change_bg(storedsettings.HOVER_COLOR)


	def leave(self, event):
		self.change_bg(storedsettings.APP_WIDGET_COLOR)

	def change_fg(self, color):
		self.config(fg=color)

	def change_bg(self, color):
		self.config(bg=color)

	def disable_hover(self):
		self.unbind("<Enter>")
		self.unbind("<Leave>")


	def bold(self):
		self.config(font=(storedsettings.FONT, self.FONT_SIZE, "bold"))

	

class BooterSelect(Button):
	def __init__(self, *args, **kwargs):
		Button.__init__(self, *args, **kwargs)
		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)
		self.config(relief=SOLID, highlightthickness=2)

		self.FONT_SIZE = 14
		width = 6
		self.config(font=(storedsettings.FONT, self.FONT_SIZE), width=width)

		self.bind("<Enter>", self.hover)
		self.bind("<Leave>", self.leave)
		self.bg = storedsettings.APP_WIDGET_COLOR
		self.hover_color = "#E9FFE8"

	def selected(self):
		self.config(font=(storedsettings.FONT, self.FONT_SIZE))
		self.bg = "#91FF8C"
		self.config(bg=self.bg)
		self.hover_color = self.bg

	def deselected(self):
		self.config(font=(storedsettings.FONT, self.FONT_SIZE))
		self.bg = storedsettings.APP_WIDGET_COLOR
		self.config(bg=self.bg)
		# self.hover_bg = storedsettings.HOVER_COLOR
		self.hover_color = "#E9FFE8"

	def hover(self, event):
		self.config(bg=self.hover_color)

	def leave(self, event):
		self.config(bg=self.bg)




class BooterLabel(Label):
	def __init__(self, *args, **kwargs):
		Label.__init__(self, *args, **kwargs)
		self.font_size = 12

		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)

		self.config(font=(storedsettings.FONT, self.font_size))


	def change_fg(self, color):
		self.config(fg=color)

	def change_bg(self, color):
		self.config(bg=color)

	def bold(self):
		self.config(font=(storedsettings.FONT, self.font_size, "bold"))


class BooterCheckbutton(Checkbutton):
	def __init__(self, *args, **kwargs):
		Checkbutton.__init__(self, *args, **kwargs)

		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)

	def change_fg(self, color):
		self.config(fg=color)

	def change_bg(self, color):
			self.config(bg=color)


class BooterOptionMenu(OptionMenu):
	def __init__(self, *args, **kwargs):
		OptionMenu.__init__(self, *args, **kwargs)

		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)

		self.config(activebackground=storedsettings.HOVER_COLOR)

		self['menu'].config(bg=storedsettings.APP_MAIN_COLOR)
		self['menu'].config(activebackground=storedsettings.HOVER_COLOR)
		self['menu'].config(activeforeground=storedsettings.APP_FONT_COLOR)
		self['menu'].config(font=storedsettings.DROPDOWN_FONT)
		self.config(relief=SOLID)

		# # Removes grey border around Option Menu
		self.config(highlightthickness=0)

		self.config(font=(storedsettings.FONT, 13))
		self.apply_image()


	def change_fg(self, color):
		self.config(fg=color)

	def change_bg(self, color):
		self.config(bg=color)



	def apply_image(self):
		IMG_SIZE = 10
		img = Image.open("resources/images/dropdownarrow.png")
		
		img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(img)

		self.config(indicatoron=0, image=self.img, compound="right")





class BooterEntry(Entry):
	def __init__(self, *args, **kwargs):
		Entry.__init__(self, *args, **kwargs)

		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)
		self.config(relief=GROOVE)


class BooterRadiobutton(Radiobutton):
	def __init__(self, *args, **kwargs):
		ttk.Radiobutton.__init__(self, *args, **kwargs)

		self.config(bg="white")

	



