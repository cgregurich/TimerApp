import sqlite3

# I believe the task name should function as a unique key
# This should work as long as I only have functionality for
# daily goals, not week, month, custom, etc.

class GoalDAO():
	def __init__(self, db_name="goal.db"):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS goals (
			task text, goal_time integer
			)""")
		self.conn.commit()


	def insert_goal(self, goal_dict):
		"""Expects arg goal_dict of format
		{"task": str, "goal_time": int}"""
		with self.conn:
			self.c.execute("""INSERT INTO goals VALUES(
				:task, :goal_time
				)""", goal_dict)

	def get_all_goals(self):
		"""Pulls all data from database and uses helper func 
		to convert to a list of dictionaries that look like 
		{"task": str, "goal_time": int}"""
		with self.conn:
			self.c.execute("""SELECT * FROM goals""")
			tup_list = self.c.fetchall()
		return self._convert_tup_list_to_dict_list(tup_list)


	def _convert_tup_list_to_dict_list(self, tup_list):
		goal_dict_list = []
		for tup in tup_list:
			info_dict = {"task": tup[0], "goal_time": tup[1]}
			goal_dict_list.append(info_dict)
		return goal_dict_list


	def get_all_tasks(self):
		"""Returns a list of all task names in the database"""
		with self.conn:
			self.c.execute("""SELECT task FROM goals""")
			tup_list = self.c.fetchall()
		return [tup[0] for tup in tup_list]


	def update_goal(self, goal_dict):
		with self.conn:
			self.c.execute("""UPDATE goals
				SET goal_time = :goal_time
				WHERE task = :task""", goal_dict)
		return self.c.rowcount