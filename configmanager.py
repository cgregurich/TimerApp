import configparser

class ConfigManager(configparser.ConfigParser):
	def __init__(self):
		super().__init__(self)

		self.FILE_NAME = 'usersettings.ini'
		self.check_for_config_file()

	def check_for_config_file(self):
		if not self.read(self.FILE_NAME):
			self.create_config_file()


	def create_config_file(self):
		self['SETTINGS'] = {
			'CLOCK_FG': '#000000',
			'CLOCK_BG': '#FFFFFF'
		}
		with open(self.FILE_NAME, 'w') as configfile:
			self.write(configfile)


	def change_setting(self, key, value):
		self['SETTINGS'] = {
			key: value
		}
		with open(self.FILE_NAME, 'w') as configfile:
			self.write(configfile)





