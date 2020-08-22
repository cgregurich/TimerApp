import sqlite3

from session import Session


class SessionDAO():
	def __init__(self, db_name='session.db'):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS sessions (
			task text, time_logged integer, time_completed text, date_completed text
			)""")
		self.conn.commit()



	def insert_session(self, session):
		with self.conn:
			self.c.execute("""INSERT INTO sessions VALUES(
				:task, :time_logged,  :time_completed, :date_completed
				)""", session.info)

	def delete_session(self, session_to_del):
		with self.conn:
			self.c.execute("""DELETE FROM sessions WHERE 
				task=? AND time_logged=? AND time_completed=? AND date_completed=?""", ('reading', 120, '16:14', '8-22-2020'))
			# session_to_del.info_as_tuple()
		return self.c.rowcount


	def get_all_sessions(self):
		"""Pulls all data from database and uses helper to convert to and return
		list of Session objects"""
		with self.conn:
			self.c.execute("""SELECT * FROM sessions""")
			tup_list = self.c.fetchall()

		return self._convert_tup_list_to_session_list(tup_list)


	def _convert_tup_list_to_session_list(self, tup_list):
		"""Helper method for get_all_sessions. Receives a list of tuples 
		and returns a list of Session objects"""
		session_list = []

		for tup in tup_list:
			info_dict = {'task':tup[0], 'time_logged':tup[1], 'time_completed':tup[2], 'date_completed':tup[3]}
			session_list.append(Session(info_dict))

		return session_list



