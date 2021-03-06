import pepobot.config as config
import pepobot.functions as functions

import pepobot.importers.folder as folder
import pepobot.importers.imgur as imgur

import argparse
import os
import sys

#cli arg handler
parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="Import images in bulk from defined folder.")
parser.add_argument("--imgur", help="Import images in bulk from imgur.com albums")
arg = parser.parse_args()

if arg.imgur is not None:
    imgur.imgur(arg.imgur, True)
elif arg.folder is not None:
    folder.folder(arg.folder, True)
else:
    print("ERROR: Unable to understand what you're trying to do. I suggest trying -h")
    sys.exit(0)