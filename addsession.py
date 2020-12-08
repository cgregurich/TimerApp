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

class AddSession(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.frame_input = Frame(self)
		self.frame_input.grid(row=0, column=1)

		self.frame_task_time = Frame(self.frame_input)
		self.frame_task_time.grid(row=1, column=0)

		self.om_var = StringVar()
		self.om_var.set("Select...")
		self.om = None
		self.e_hour = None
		self.e_min = None
		self.e_sec = None

		self.draw_window()


	# dropdown for task (or entry?)
	# entry for time spent (h:m:s? regex to validate?)
	# entry for time (regex to validate?)
	# entry for date (regex to validate?)


	# self.om_current_task = BooterOptionMenu(self.frame_buttons, self.controller.current_task, None)
	# # Clears the blank space created by dummy data None
	# self.om_current_task['menu'].delete(0, END)

	def draw_window(self):
		btn_back = BooterButton(self, command=lambda: print("TODO: back clicked"))
		btn_back.apply_back_image()
		self.om_var = StringVar()
		self.om_var.set("Select...")
		self.om = BooterOptionMenu(self.frame_input, self.om_var, None)

		self.init_task_time_row()
		e2 = BooterEntry(self.frame_input)
		e3 = BooterEntry(self.frame_input)
		e4 = BooterEntry(self.frame_input)

		btn_check = BooterButton(self, text="Check", command=self.check_input)

		btn_back.grid(row=0, column=0)
		self.om.grid(row=0, column=0)
		
		e3.grid(row=2, column=0)
		e4.grid(row=3, column=0)
		btn_check.grid(row=2, column=1)

		self.refresh_option_menu()

	def init_task_time_row(self):
		WIDTH = 4
		self.e_hour = BooterEntry(self.frame_task_time, width=WIDTH)
		self.e_min = BooterEntry(self.frame_task_time, width=WIDTH)
		self.e_sec = BooterEntry(self.frame_task_time, width=WIDTH)

		self.e_hour.grid(row=0, column=0)
		BooterLabel(self.frame_task_time, text=":").grid(row=0, column=1)
		self.e_min.grid(row=0, column=2)
		BooterLabel(self.frame_task_time, text=":").grid(row=0, column=3)
		self.e_sec.grid(row=0, column=4)


	def check_input(self):
		pass

	def refresh_option_menu(self):
		menu = self.om['menu']
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