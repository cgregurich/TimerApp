from configmanager import ConfigManager


mgr = ConfigManager()


CLOCK_FG = mgr.get("SETTINGS", "CLOCK_FG")


CLOCK_FONT = ('Consolas', 24, 'bold')

# FONTS
MONOSPACED = ("Consolas", 10)

FONT = "Orator STD"
# CLOCK_FONT = "Bahnschrift Light"
CLOCK_FONT = "Consolas"

CLOCK_FONT_SIZE = 24
CLOCK_FONT_TUPLE = ("Consolas", CLOCK_FONT_SIZE, "bold")

DROPDOWN_FONT = ('Orator STD', 14)



LOG_FONT = "Bahnschrift Light"
LOG_LABEL_FONT_SIZE = 12



# font = "Bahnschrift Light"
# font = "Nirmala UI Semilight"



POMO_WORK_TIME = int(mgr.get("SETTINGS", "POMO_WORK_TIME")) # in seconds
POMO_BREAK_TIME = int(mgr.get("SETTINGS", "POMO_BREAK_TIME")) # in seconds

AUTOSAVE = mgr.get("SETTINGS", "AUTOSAVE")


debug = mgr.get("SETTINGS", "DEBUG") == "1"

WAIT = 10 if debug else 1000
# APP_BG_COLOR = "#FF0000"
# APP_FG_COLOR = "#641E16"

APP_MAIN_COLOR = mgr.get("SETTINGS", "APP_MAIN_COLOR")
APP_WIDGET_COLOR = mgr.get("SETTINGS", "APP_WIDGET_COLOR")
APP_FONT_COLOR = mgr.get("SETTINGS", "APP_FONT_COLOR")

HOVER_COLOR = mgr.get("SETTINGS", "HOVER_COLOR")
DISABLED_FONT_COLOR = "#C1C1C1"



