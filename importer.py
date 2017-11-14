import pepobot.config as config
import pepobot.functions as functions

import glob
import os
import sys
import shutil

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

#let the user do imports via cli command
if len(sys.argv) > 2:
    print("ERROR: too many arguments. {0}".format(sys.argv[2:]))
    sys.exit(0)
elif len(sys.argv) == 1 or sys.argv[1].lower() == "-h":
    print('HELP: python3 importer.py "C:\\users\\user\\Desktop\\my pics\\memes"') #todo: probably build a better help menu, and how paths cant end in \canidates
    sys.exit(0)
else:
    IMPORT_FOLDER = sys.argv[1] + SLASHES
    print("IMPORT: Looking in \"{0}\" for images(PNG, JPG, GIF) that do not already exist in {1}".format(IMPORT_FOLDER, config.cfg['scraper']['location']))

#get all the frogs
canidates = glob.glob(IMPORT_FOLDER + "*")
elected = []

#find any images that will be eligible to be added to the image store
for image in canidates:
    sha = functions.sha1Sum(image)

    #checks file type by hex data
    if functions.allowedFileType(image) is False:
        print("WARN: Ignoring {0}, does not have a valid image type according to metadata.".format(image))
        continue

    #checks for duplicates, if it doesnt find one adds it to an elected images list
    if len(functions.findDuplicateFrog(sha)) is 0:
        elected.append(image)
    else:
        print("DUPE: {0} was already found saved with the SHA1 of {1}".format(image, sha))

#no images stop processing, otherwise ask for permission to complete
if len(elected) is 0:
    print("ERROR: no images elliglble for import :(")
    sys.exit(0)
else:
    print("IMPORT: Ready to copy {0} images of the {1} files in selected folder.".format(len(elected), len(canidates)))

#make the user accept what they are about to do to the collection
meme = input("IMPORT (USER INPUT): Type 'ok' to start. Any other input will cancel.\n")
if meme != "ok":
    print("IMPORT: import cancelled :(")
    sys.exit(0)

#if we got this far were not looking back, process each image that passed the checks
for image in elected:

    #copy it to the tmp folder
    tempimage = os.getcwd() + SLASHES + config.cfg['scraper']['staging'] + os.path.basename(image)
    shutil.copyfile(image, tempimage)

    #commit it to the store as any fetch command would do
    functions.commitFrogToLibrary(tempimage)

#were finished
print("IMPORT: All done :^)")