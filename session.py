from datetime import datetime

class Session():
	def __init__(self, task=None, time_logged=None):
		if task and time_logged:
			cur_date = self.get_current_date()
			cur_time = self.get_current_time()
			self.info = { 'task': task, 'time_logged': time_logged, 'time_completed': cur_time, 'date_completed': cur_date}
		else:
			self.info = { 'task': None, 'time_logged': None, 'time_completed': None, 'date_completed': None}




	def __str__(self):
		return_str = ""
		for key, value in self.info.items():
			return_str += f"{key}: {value}  "
		return return_str.strip()

	def set_info_from_dict(self, dict):
		self.info = dict

	def info_as_tuple(self):
		"""Returns the values from class dict info as a tuple"""
		return tuple(self.info.values())

	def get_info_for_display(self):
		"""Returns a list of the Session's info in format
		[task, time_logged -> HH:MM:SS, time_completed, date_completed]"""
		info = list(self.info.values())
		info[1] = self._format_seconds_to_time(self.time_logged)
		return info

	def _format_seconds_to_time(self, s):
		hours, seconds = divmod(s, 3600)
		minutes, seconds = divmod(seconds, 60)
		# Create datetime object
		if hours > 0:
			t = "{:0>2}h {:0>2}m {:0>2}s".format(hours, minutes, seconds)
			time = "{:>11}".format(t)
		elif minutes > 0:
			t = "{:0>2}m {:0>2}s".format(minutes, seconds)
			time = "{:>11}".format(t)
		else:
			t = "{:0>2}s".format(seconds)
			time = "{:>11}".format(t)
		return time


	# 5h 20m 12s
	# 5:20:12

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
		now = datetime.now()
		return now.strftime("%H:%M")

	def get_current_date(self):
		"""Returns string of current time in format MM-DD-YY"""
		today = datetime.now()
		return today.strftime("%m-%d-%y")

	def get_date_obj(self):
		date_list = self.date_completed.split('-')
		month = int(date_list[0])
		day = int(date_list[1])
		year = int(date_list[2]) + 2000
		obj = datetime(year, month, day).date()
		return obj


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



