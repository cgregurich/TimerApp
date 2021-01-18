from configmanager import ConfigManager

import pyglet, os

pyglet.font.add_file('resources/fonts/OratorSTD.otf')


mgr = ConfigManager()


CLOCK_FG = mgr.get("SETTINGS", "CLOCK_FG")


CLOCK_FONT = ('Consolas', 24, 'bold')

# FONTS
MONOSPACED = ("Consolas", 10)

FONT = "Orator STD"
BACK_FONT_SIZE = 10
# CLOCK_FONT = "Bahnschrift Light"
CLOCK_FONT = "Consolas"

CLOCK_FONT_SIZE = 50
CLOCK_FONT_TUPLE = ("Consolas", CLOCK_FONT_SIZE, "bold")

ENTRY_FONT_TUPLE = (FONT, 14)

DROPDOWN_FONT = ('Orator STD', 14)

GOAL_FONT = ("Orator STD", 17)



LOG_FONT = "Bahnschrift Light"
LOG_LABEL_FONT_SIZE = 12



# font = "Bahnschrift Light"
# font = "Nirmala UI Semilight"



POMO_WORK_TIME = int(mgr.get("SETTINGS", "POMO_WORK_TIME")) # in seconds
POMO_BREAK_TIME = int(mgr.get("SETTINGS", "POMO_BREAK_TIME")) # in seconds

AUTOSAVE = mgr.get("SETTINGS", "AUTOSAVE")
UNTRACKED_POPUP = mgr.get("SETTINGS", "UNTRACKED_POPUP")


debug = mgr.get("SETTINGS", "DEBUG") == "1"

WAIT = 10 if debug else 1000
# APP_BG_COLOR = "#FF0000"
# APP_FG_COLOR = "#641E16"

APP_MAIN_COLOR = mgr.get("SETTINGS", "APP_MAIN_COLOR")
APP_WIDGET_COLOR = mgr.get("SETTINGS", "APP_WIDGET_COLOR")
APP_FONT_COLOR = mgr.get("SETTINGS", "APP_FONT_COLOR")

HOVER_COLOR = mgr.get("SETTINGS", "HOVER_COLOR")
DISABLED_FONT_COLOR = "#C1C1C1"



# Window sizes for all frames
STOPWATCH_WIN_SIZE =     "428x205"
TIMER_WIN_SIZE =         "434x250"
POMO_WIN_SIZE =          "336x205"
SETTINGS_WIN_SIZE =      "452x402"
TASKS_WIN_SIZE =         "419x300"
VIEWLOG_WIN_SIZE =       "470x300"
MAINMENU_WIN_SIZE =      "300x575"
GOALS_WIN_SIZE =         ""


SETTINGS_BUTTON_FONT = (FONT, 14)


