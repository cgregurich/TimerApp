from datetime import datetime

class Session():
	def __init__(self, task, time_logged):
		cur_date = self.get_current_date()
		cur_time = self.get_current_time()
		self.info = { 'task': task, 'time_logged': time_logged, 'time_completed': cur_time, 'date_completed': cur_date}



	def __str__(self):
		return_str = ""
		for key, value in self.info.items():
			return_str += f"{key}: {value}  "
		return return_str.strip()

	def info_as_tuple(self):
		"""Returns the values from class dict info as a tuple"""
		return tuple(self.info.values())

	def get_info(self):
		return self.info

	def set_info(self, info):
		self.info = info

	def set_time_logged(self, time_logged):
		"""Arg time_logged is in seconds"""
		self.info['time_logged'] = time_logged

	def set_task(self, task):
		self.info['task'] = task

	def get_current_time(self):
		"""Returns string of current time in format HH:MM"""
		hour = datetime.now().time().hour
		minute = datetime.now().time().minute
		return f"{hour}:{minute}"

	def get_current_date(self):
		"""Returns string of current time in format MM-DD-YY"""
		date = datetime.now().date()
		month = date.month
		day = date.day
		year = date.year
		return f"{month}-{day}-{year}"


	@property
	def time_logged(self):
		return self.info['time_logged']

	@property
	def time_completed(self):
		return self.info['time_completed']

	@property
	def date_completed(self):
		return self.info['date_completed']

	@property
	def task(self):
		return self.info['task']



