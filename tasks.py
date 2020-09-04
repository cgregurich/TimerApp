import tkinter as tk
from taskdao import TaskDAO
from tkinter import messagebox

"""
Entry for entering new task
save button to save changes (only saves non-empty entries)
check box next to each entry for deleting
save when back button is pressed???? idk
"""
taskdao = TaskDAO()

class Tasks(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller = controller
		self.selected_task = tk.StringVar()
		self.selected_task.set("--")
		self.draw_window()

	def draw_window(self):
		back_button = tk.Button(self, text='Back', command=lambda: self.controller.show_frame('MainMenu'))
		back_button.grid(row=0, column=0)

		self.entry_task = tk.Entry(self)
		self.entry_task.grid(row=1, column=1)

		btn_add = tk.Button(self, text="Add", command=self.add_clicked)
		btn_add.grid(row=1, column=2)


	
		tasks = taskdao.get_all_tasks()
		if not tasks:
			tasks = ["No tasks"]
		
	
		self.om_tasks = tk.OptionMenu(self, self.selected_task, *tasks)
			

		self.om_tasks.grid(row=2, column=1)
		btn_del = tk.Button(self, text="Delete", command=self.del_clicked)
		btn_del.grid(row=3, column=1)


	def del_clicked(self):
		task = self.selected_task.get()
		if task == "No tasks":
			return
		taskdao.delete_task(task)
		self.refresh_task_menu()
		self.selected_task.set("")



	def add_clicked(self):
		task = self.entry_task.get()
		if not self.is_task_entered_valid():
			return
		
		taskdao.insert_task(task)

		self.entry_task.delete(0, 
			tk.END)
		self.selected_task.set("")

		self.refresh_task_menu()

	def is_task_entered_valid(self):
		task = self.entry_task.get()
		if not self.is_task_unique(task) or not task:
			messagebox.showerror("Error", f"There is already a task called '{task}'")
			return False
		else:
			return True

	def refresh_task_menu(self):
		self.om_tasks.destroy()
		all_tasks = taskdao.get_all_tasks()
		if not all_tasks:
			all_tasks = ["No tasks"]
		self.om_tasks = tk.OptionMenu(self, self.selected_task, *all_tasks)
		self.om_tasks.grid(row=2, column=1)
		

	def is_task_unique(self, task):
		return task.lower() not in taskdao.get_all_tasks()
		






	def reset(self):
		pass


