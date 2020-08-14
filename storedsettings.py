from configmanager import ConfigManager


mgr = ConfigManager()




CLOCK_FG = mgr.get("SETTINGS", "CLOCK_FG")
CLOCK_BG = mgr.get("SETTINGS", "CLOCK_BG")


CLOCK_FONT = ('Consolas', 24, 'bold')



POMO_WORK_TIME = int(mgr.get("SETTINGS", "POMO_WORK_TIME")) # in seconds
POMO_BREAK_TIME = int(mgr.get("SETTINGS", "POMO_BREAK_TIME")) # in seconds
