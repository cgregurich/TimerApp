import sqlite3

"""
add things
delete things
"""


class TaskDAO():
	def __init__(self, db_name='task.db'):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS tasks (
			task text
			)""")
		self.conn.commit()

	def insert_task(self, task):
		"""Inserts the task param into the db"""
		with self.conn:
			self.c.execute("""INSERT INTO tasks VALUES(
				?
				)""", (task,))

	def delete_task(self, task):
		"""Deletes the task that matches the param task"""
		with self.conn:
			self.c.execute("""DELETE FROM tasks WHERE task=?""", (task,))

	def get_all_tasks(self):
		"""Returns a list of all tasks as strings"""
		with self.conn:
			self.c.execute("""SELECT * FROM tasks""")
			tasks = self.c.fetchall()

		tasks = [i[0] for i in tasks]
		return tasks

	def get_all_tasks_lower(self):
		tasks = self.get_all_tasks()
		lower_tasks = [task.lower() for task in tasks]
		return lower_tasks