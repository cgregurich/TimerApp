from tkinter import *
from taskdao import TaskDAO
from tkinter import messagebox
from booterwidgets import *

"""
BooterEntry for entering new task
save button to save changes (only saves non-empty entries)
check box next to each entry for deleting
save when back button is pressed???? idk
"""
taskdao = TaskDAO()

class Tasks(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.config(bg=storedsettings.APP_MAIN_COLOR)

		
		self.frame_buttons = Frame(self, bg=storedsettings.APP_MAIN_COLOR)
		self.frame_input = Frame(self, bg=storedsettings.APP_MAIN_COLOR)

		
		self.frame_buttons.grid(row=1, column=2, padx=(20, 0))
		self.frame_input.grid(row=1, column=1)

		self.parent = parent
		self.selected_task = StringVar()
		self.selected_task.set("Select...")
		self.draw_window()

	def draw_window(self):

		lbl_header = BooterLabel(self, text="Edit Tasks")
		lbl_header.config(font=(storedsettings.FONT, 20, "bold"))

		btn_back = BooterButton(self, command=lambda: self.parent.show_frame('MainMenu'))
		
		btn_back.apply_back_image()

		self.entry_task = BooterEntry(self.frame_input, width=16)
		

		btn_add = BooterButton(self.frame_buttons, text="Add", width=7, command=self.add_clicked)
		

		tasks = taskdao.get_all_tasks()
	
		# Init's OptionMenu; this is never seen because refresh_task_menu is called
		# when Tasks is clicked on for the first time	
		self.om_tasks = BooterOptionMenu(self.frame_input, self.selected_task, None)
		self.om_tasks['menu'].delete(0)

		
		self.btn_del = BooterButton(self.frame_buttons, text="Delete", width=7, command=self.del_clicked)
		

		btn_back.grid(row=0, column=0, padx=(10, 10))
		lbl_header.grid(row=0, column=1, columnspan=2, pady=(0, 30))
		self.entry_task.grid(row=1, column=1, pady=(0, 30))
		btn_add.grid(row=1, column=2, pady=(0, 10))
		self.om_tasks.grid(row=2, column=1)
		self.btn_del.grid(row=2, column=2)

	def del_clicked(self):
		task = self.selected_task.get()
		if task == "Select...":
			return
		tasks = taskdao.get_all_tasks_lower()
		index = tasks.index(task.lower())
		self.delete_task(index)
		taskdao.delete_task(task)
		self.refresh_task_menu()

	def delete_task(self, index):
		"""Deletes task from OptionMenu using item's index"""
		self.om_tasks['menu'].delete(index)



	def add_clicked(self):
		task = self.entry_task.get()
		if not self.is_task_entered_valid():
			return
		
		taskdao.insert_task(task)

		self.entry_task.delete(0, 
			END)
		self.selected_task.set("")
		# Since an item has been added, enable delete button
		self.btn_del.config(state=NORMAL)
		self.refresh_task_menu()

	def is_task_entered_valid(self):
		task = self.entry_task.get()

		# Check length of task
		if len(task) > 15:
			messagebox.showerror("Error", "Maximum task name length of 15 characters")
			return False


		# Check for duplicates
		if not self.is_task_unique(task):
			messagebox.showerror("Error", f"There is already a task called '{task}'")
			return False

		# Check for blank entry
		if not task:
			messagebox.showerror("Error", "Task name can't be blank")
			return False

		# Check for reserved string "No Tasks"
		if task.lower() == "no tasks":
			messagebox.showerror("Error", "Invalid name")
			return False
		return True

	def refresh_task_menu(self):
		menu = self.om_tasks['menu']
		tasks = taskdao.get_all_tasks()
		menu.delete(0, END)
		# No tasks -> create unselectable item indicating no tasks have been added
		if not tasks:
			menu.add_command(label="No Tasks")
			# Since no items exist, disable delete button
			self.btn_del.config(state=DISABLED)

		# Tasks exist -> clear the list, get all tasks from DB, draw them to the menu
		else:
			for task in tasks:
				menu.add_command(label=task, command=lambda value=task: self.selected_task.set(value))
		# Set prompt text
		self.selected_task.set("Select...")

		


	def is_task_unique(self, task):
		return task.lower() not in taskdao.get_all_tasks_lower()



	def reset(self):
		self.refresh_task_menu()
		# self.parent.geometry(storedsettings.TASKS_WIN_SIZE)