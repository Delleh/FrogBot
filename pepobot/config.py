print("IMPORT: %s" % __name__)
from . import functions
import json

#load the json file as cfg, allows access as config.json. Stop on error.
def loadConfig():
	try:
		with open("config.json", "r") as cfgFile:
			global cfg
			try:
				cfg = json.load(cfgFile)
				print("CONFIG: config.json loaded.")
				return True
			except json.decoder.JSONDecodeError as e:
				print("ERROR: config.json is not formatted properly {0}".format(e))
				return e
	except FileNotFoundError as e:
		print("ERROR: config.json file missing inside root folder... {0}".format(e))
		return e
		functions.stopBot()

#since it is the first time starting the bot we need a working config or crash it
if loadConfig() is not True:
	print("ERROR: Unable to start bot. Unrecoverable error in loading genesis configuration file.")
	functions.stopBot()