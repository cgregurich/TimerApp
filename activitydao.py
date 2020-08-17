import sqlite3

class ActivityDAO():
	def __init__(self, db_name='activity.db'):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS activities (
			activity text
			)""")

		self.conn.commit()

	def insert_activity(self, new_activity):
		with self.conn:
			self.c.execute("""INSERT INTO activities VALUES(:activity)""", (new_activity,))