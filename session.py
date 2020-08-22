from datetime import datetime

class Session():
	def __init__(self, data=None):
		if data:
			self.data = data
		else:
			cur_date = self.get_current_date()
			cur_time = self.get_current_time()
			self.data = {'time_logged': None, 'time_completed': cur_time, 'date_completed': cur_date, 'task': None}



	def __str__(self):
		return_str = ""
		for key, value in self.data.items():
			return_str += f"{key}: {value} "
		return return_str.strip()


	def get_data(self):
		return self.data

	def set_data(self, data):
		self.data = data

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



