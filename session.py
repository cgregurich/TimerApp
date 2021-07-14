from datetime import datetime
DEFAULT_TASK = "Select..."
class Session():
	"""
	task -> str
	task_time -> int representing seconds
	time_started -> time in format HH:MM (military time)
	date_started -> date in format MM-DD-YY
	"""
	def __init__(self, task=None, task_time=None, time_started=None, date_started=None):

		self.info = {"task": task, "task_time": task_time, "time_started": time_started, 
								"date_started": date_started}

		# Get current date/time if missing
		if not self.time_started:
			self.info["time_started"] = self.get_current_time()
		if not self.date_started:
			self.info["date_started"] = self.get_current_date()
		if self.task == DEFAULT_TASK:
			self.info["task"] = "N/A"


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
		[task, task_time -> HH:MM:SS, time_started, date_started]"""
		info = list(self.info.values())
		info[1] = self._format_seconds_to_time(self.task_time)
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


	def get_info(self):
		return self.info


	def set_task_time(self, task_time):
		"""Arg task_time is in seconds"""
		self.info["task_time"] = task_time


	def set_task(self, task):
		self.info["task"] = task


	def get_current_time(self):
		"""Returns string of current time in format HH:MM"""
		now = datetime.now()
		return now.strftime("%H:%M")


	def get_current_date(self):
		"""Returns string of current date in format MM-DD-YY"""
		today = datetime.now()
		return today.strftime("%m-%d-%y")


	def get_date_obj(self):
		date_list = self.date_started.split('-')
		month = int(date_list[0])
		day = int(date_list[1])
		year = int(date_list[2]) + 2000
		obj = datetime(year, month, day).date()
		return obj


	@property
	def task_time(self):
		return self.info["task_time"]


	@property
	def time_started(self):
		return self.info["time_started"]


	@property
	def date_started(self):
		return self.info["date_started"]


	@property
	def task(self):
		return self.info["task"]