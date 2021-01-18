import tkinter as tk
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




class BooterButton(tk.Button):
	def __init__(self, *args, **kwargs):
		tk.Button.__init__(self, *args, **kwargs)

		# Default settings for the widget
		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)
		self.config(relief=tk.SOLID)

		self.config(disabledforeground=storedsettings.DISABLED_FONT_COLOR)


		
		# Set default font unless font is given
		if "font" not in kwargs.keys():
			self.FONT_SIZE = 17
			self.config(font=(storedsettings.FONT, self.FONT_SIZE))

		if "height" not in kwargs.keys():
			self.config(height=0)


		self.bind("<Enter>", self.hover)
		self.bind("<Leave>", self.leave)

	def hover(self, event):
		# Only indicate hover if button is not disabled
		if self['state'] == tk.NORMAL:
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



	def apply_back_image(self):
		"""Applies an image of an arrow to the button; used for back buttons"""
		IMG_SIZE = 20
		img = Image.open("resources/images/backarrow.webp")
		img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(img)
		self.config(image=self.img)
		self.config(width=40)

	def apply_settings_image(self):
		IMG_SIZE = 50
		img = Image.open("resources/images/settings_icon.png")
		img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(img)
		self.config(image=self.img)
		self.config(width=50)
		self.config(bd=0)
		self.disable_hover()
		self.bind("<Enter>", self.settings_hover)
		self.bind("<Leave>", self.settings_leave)

	def settings_hover(self, event):
		IMG_SIZE = 50
		img = Image.open("resources/images/settings_icon_hover.png")
		img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(img)
		self.config(image=self.img)
		self.config(width=50)
		self.config(bd=0)

	def settings_leave(self, event):
		self.apply_settings_image()

	

class BooterSelect(tk.Button):
	def __init__(self, *args, **kwargs):
		tk.Button.__init__(self, *args, **kwargs)
		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)
		self.config(relief=tk.SOLID, highlightthickness=2)

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
		self.hover_color = "#E9FFE8"

	def hover(self, event):
		self.config(bg=self.hover_color)

	def leave(self, event):
		self.config(bg=self.bg)




class BooterLabel(tk.Label):
	def __init__(self, *args, **kwargs):
		tk.Label.__init__(self, *args, **kwargs)
		self.font_size = 18

		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)

		self.config(font=(storedsettings.FONT, self.font_size))


	def change_fg(self, color):
		self.config(fg=color)

	def change_bg(self, color):
		self.config(bg=color)

	def bold(self):
		self.config(font=(storedsettings.FONT, self.font_size, "bold"))


class BooterCheckbutton(tk.Checkbutton):
	def __init__(self, *args, **kwargs):
		tk.Checkbutton.__init__(self, *args, **kwargs)

		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)

	def change_fg(self, color):
		self.config(fg=color)

	def change_bg(self, color):
			self.config(bg=color)


class BooterOptionMenu(tk.OptionMenu):
	def __init__(self, *args, **kwargs):
		tk.OptionMenu.__init__(self, *args, **kwargs)

		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)

		self.config(activebackground=storedsettings.HOVER_COLOR)

		self['menu'].config(bg=storedsettings.APP_MAIN_COLOR)
		self['menu'].config(activebackground=storedsettings.HOVER_COLOR)
		self['menu'].config(activeforeground=storedsettings.APP_FONT_COLOR)
		self['menu'].config(font=storedsettings.DROPDOWN_FONT)
		self.config(relief=tk.SOLID)

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





class BooterEntry(tk.Entry):
	def __init__(self, *args, **kwargs):
		tk.Entry.__init__(self, *args, **kwargs)

		self.config(bg=storedsettings.APP_WIDGET_COLOR)
		self.config(fg=storedsettings.APP_FONT_COLOR)
		self.config(relief=tk.SOLID)
		self.config(font=storedsettings.ENTRY_FONT_TUPLE)
		self.config(highlightthickness=1, highlightbackground=storedsettings.APP_MAIN_COLOR)
		self.config(highlightcolor="#000000")




class BooterRadiobutton(tk.Radiobutton):
	def __init__(self, *args, **kwargs):
		ttk.tk.Radiobutton.__init__(self, *args, **kwargs)

		self.config(bg="white")

	



