from tkinter import *
from booterwidgets import *
from taskdao import TaskDAO

taskdao = TaskDAO()


# WHERE I LEFT OFF:
# getting the window created for adding sessions
# need to implement a calendar widget for date picking
# and some sort of input for the time the task was completed
# as well as validation for the user input and
# then of course figuring out how to actually add the data to the
# database. 

# TODO:
# - add labels for each line
# - add calendar widget for date 
# - make add window not resizable
# - do input validation


class AddSession(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.config(bg=storedsettings.APP_MAIN_COLOR)
		self.controller = controller
		self.frame_input = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_input.grid(row=0, column=1)

		self.frame_task_time = Frame(self.frame_input, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_task_time.grid(row=1, column=0)

		self.frame_time_completed = Frame(self.frame_input, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_time_completed.grid(row=2, column=0)

		self.widgets = {"optionmenu": None,
					    "task_time": None,
					    "time_completed": None,
					    "date_completed": None}




		self.e_hour = None
		self.e_min = None
		self.e_sec = None

		self.draw_window()


	

	def draw_window(self):
		btn_back = BooterButton(self, command=lambda: print("TODO: back clicked"))
		btn_back.apply_back_image()
		
		self.init_task_optionmenu()

		self.init_task_time_row()
		self.init_time_completed_row()
		e4 = BooterEntry(self.frame_input)

		btn_check = BooterButton(self, text="Check", command=self.check_input)

		btn_back.grid(row=0, column=0, sticky="n")
		

		e4.grid(row=3, column=0)
		btn_check.grid(row=2, column=1)


		self.refresh_option_menu()		

	def init_task_optionmenu(self):
		om_var = StringVar()
		om_var.set("Select...")
		om = BooterOptionMenu(self.frame_input, om_var, None)
		widgets = {"om_var": om_var,
				   "om": om}
		self.widgets["optionmenu"] = widgets
		om.grid(row=0, column=0)


	def init_task_time_row(self):
		WIDTH = 4

		e_hour = BooterEntry(self.frame_task_time, width=WIDTH)
		e_min = BooterEntry(self.frame_task_time, width=WIDTH)
		e_sec = BooterEntry(self.frame_task_time, width=WIDTH)

		widgets = {"e_hour": e_hour,
				   "e_min": e_min,
				   "e_sec": e_sec}
		self.widgets["task_time"] = widgets

		e_hour.grid(row=0, column=0)
		BooterLabel(self.frame_task_time, text=":").grid(row=0, column=1)
		e_min.grid(row=0, column=2)
		BooterLabel(self.frame_task_time, text=":").grid(row=0, column=3)
		e_sec.grid(row=0, column=4)

	def init_time_completed_row(self):
		WIDTH = 4
		e_hour = BooterEntry(self.frame_time_completed, width=WIDTH)
		e_min = BooterEntry(self.frame_time_completed, width=WIDTH)
		widgets = {"e_hour": e_hour,
		           "e_min": e_min}
		self.widgets["time_completed"] = widgets
		e_hour.grid(row=0, column=0)
		BooterLabel(self.frame_time_completed, text=":").grid(row=0, column=1)
		e_min.grid(row=0, column=2)


	def check_input(self):
		pass

	def refresh_option_menu(self):
		menu = self.widgets["optionmenu"]["om"]['menu']
		tasks = taskdao.get_all_tasks()
		print(f"tasks: {tasks}")
		menu.delete(0, END)
		if not tasks:
			menu.add_command(label="No Tasks")
		else:
			for task in tasks:
				menu.add_command(label=task, command=lambda value=task: self.om_var.set(value))






def main():
	root = Tk()
	a = AddSession(root)
	a.pack()
	root.mainloop()


if __name__ == "__main__":
	main()