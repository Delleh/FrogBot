import pepobot.config as config
import pepobot.functions as functions

import pepobot.importers.folder as folder
import pepobot.importers.folder as imgur

import argparse
import os
import sys


#find if we are on windows or unix because windows is a special snowflake liberal that needs its \\ hugbox directories. Wanna hop on Discord and debate me?
if os.name == "nt":
    SLASHES = "\\"
    print("INFO: Attempting to use Windows formatting for filesystems")
elif os.name == "posix":
    SLASHES = "/"
    print("INFO: Attempting to use Linux formatting for filesystems")
else:
    print("ERROR: Unsupported OS. If you're not on Linux or Windows you can probably fix this on your own.")
    sys.exit(0)

#cli arg handler
parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="Import images in bulk from defined folder.")
parser.add_argument("--imgur", help="Import images in bulk from imgur.com albums")
arg = parser.parse_args()





imgur(arg.imgur)
folder(arg.folder)

sys.exit(0)


