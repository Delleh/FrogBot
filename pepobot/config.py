print("IMPORT: %s" % __name__)
from . import functions
import json
import os

#load the json file as cfg, allows access as config.json. Stop on error.
def loadConfig():
	global cfg
	try:
		with open("config.json", "r") as cfgFile:
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

#make the folders needed for runtime if they do not exist
if os.path.exists(cfg['scraper']['location']) is False:
	print("WARN: directory {0} does not exist as defined in config. Making now.".format(cfg['scraper']['location']))
	try:
		os.makedirs(cfg['scraper']['location'])
	except OSError as e:
		print("ERROR: Unable to start bot. Unable to make image storage folder. Error: {0}".format(e))
		functions.stopBot()

if os.path.exists(cfg['scraper']['staging']) is False:
	print("WARN: directory {0} does not exist as defined in config. Making now.".format(cfg['scraper']['staging']))
	try:
		os.makedirs(cfg['scraper']['staging'])
	except OSError as e:
		print("ERROR: Unable to start bot. Unable to make image storage folder. Error: {0}".format(e))
		functions.stopBot()