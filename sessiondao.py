import sqlite3
from session import Session
import datetime as dt

class SessionDAO():
	def __init__(self, db_name='session.db'):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS sessions (
			task text, task_time integer, time_completed text, date_completed text
			)""")
		self.conn.commit()


	def insert_session(self, session):
		with self.conn:
			self.c.execute("""INSERT INTO sessions VALUES(
				:task, :task_time,  :time_completed, :date_completed
				)""", session.info)


	# TODO: lol didn't know I even wrote this
	def delete_session(self, session_to_del):
		with self.conn:
			self.c.execute("""DELETE FROM sessions WHERE 
				task=? AND task_time=? AND time_completed=? AND date_completed=?""", ('reading', 120, '16:14', '8-22-2020'))
			# session_to_del.info_as_tuple()
		return self.c.rowcount


	def get_all_sessions(self):
		"""Pulls all data from database and uses helper to convert to and return
		list of Session objects"""
		with self.conn:
			self.c.execute("""SELECT * FROM sessions ORDER BY date_completed, time_completed""")
			tup_list = self.c.fetchall()

		return self._convert_tup_list_to_session_list(tup_list)


	def _convert_tup_list_to_session_list(self, tup_list):
		"""Helper method for get_all_sessions. Receives a list of tuples 
		and returns a list of Session objects"""
		session_list = []

		for tup in tup_list:
			info_dict = {'task':tup[0], 'task_time':tup[1], 'time_completed':tup[2], 'date_completed':tup[3]}
			s = Session()
			s.set_info_from_dict(info_dict)
			session_list.append(s)

		return session_list


	def get_all_sessions_from_date(self, date):
		"""Arg date must be datetime.date object"""
		all_sessions = self.get_all_sessions()
		sessions_list = []
		for session in all_sessions:
			session_datetime_obj = session.get_date_obj()
			if session_datetime_obj == date:
				sessions_list.append(session)

		return sessions_list


	def get_all_sessions_between_dates(self, start, end):
		"""Returns list of Session objects that have a date_completed on and between
		start and end"""

		dates = self._generate_dates_between(start, end)
		sessions = []
		for date in dates:
			sessions += self.get_all_sessions_from_date(date)
		return sessions


	def _generate_dates_between(self, start, end):
		"""Returns a list of date objects starting at start and ended on end"""
		dates = []
		temp = start
		while temp <= end:
			dates.append(temp)
			temp += dt.timedelta(days=1)
		return dates


	def get_all_sessions_by_task(self, task):
		"""ARG task : str
		Returns a list of Session objects that are of the task
		provided by the arg task"""
		with self.conn:
			self.c.execute("""SELECT * FROM sessions WHERE task = ?
				ORDER BY date_completed, time_completed""", (task,))
			tup_list = self.c.fetchall()

		return self._convert_tup_list_to_session_list(tup_list)

	# def get_all_sessions_by_task_between_dates(self, task, start_date, end_date):
	# 	"""
	# 	"""
	# 	sessions = self.get_all_sessions_between_dates(start_date, end_date)
	# 	task_sessions = []
	# 	for s in sessions:
	# 		if s.task == task:
	# 			task_sessions.append(s)
	# 	return s

