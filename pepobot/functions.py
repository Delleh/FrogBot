from . import config

import aiohttp
import glob
import hashlib
import imghdr
import os
import random
import re
import sys
import logging

logger = logging.getLogger(__name__)
logger.info("loading...")

def getLinksFromPost(msg):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)

def getAllFrogs():
    frogs = glob.glob(config.cfg['scraper']['location'] + "*")
    return frogs

def randomFrog():
    return random.choice(getAllFrogs())

def stopBot():
    sys.exit(0)

def osSlashes():
    #find if we are on windows or unix because windows is a special snowflake liberal that needs its \\ hugbox directories. Wanna hop on Discord and debate me?
    if os.name == "nt":
        return "\\"
    elif os.name == "posix":
        return "/"
    else:
        return None

def sha1Sum(file):
    sha1 = hashlib.sha1() 
    with open(file, 'rb') as r:
        buf = r.read(65536)
        while len(buf) > 0:
            sha1.update(buf)
            buf = r.read(65536)

    return sha1.hexdigest()

def allowedFileType(filename):
    filetype = imghdr.what(filename)
    if filetype in ['jpg','jpeg','png','gif','bmp']:
        return True
    else:
        return False

def deleteFrog(filename):
    return os.remove(filename)

def findDuplicateFrog(sha1):
    return glob.glob(config.cfg['scraper']['location'] + sha1 + "*")

def commitFrogToLibrary(filename):
    sha = sha1Sum(filename)

    #if we find a duplicate frog, ignore
    if len(findDuplicateFrog(sha)) is not 0:
        logger.warn("A duplicate frog was already found saved on disk with the SHA1 of {0}".format(sha))
        deleteFrog(filename)
        return False
    else:
        logger.info("Frog accepted as not seen, adding to the folder. SHA1:{0}".format(sha))
        fname, fext = os.path.splitext(filename)
        os.rename(filename, config.cfg['scraper']['location'] + sha + fext)
        return filename

async def saveFrog(url, filename):
     async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        raw = await r.read()
                        with open(filename, "wb") as wr:
                            wr.write(raw)
                        return filename
                    else:
                        return False

async def getFrogFromUpload(msg):
    for attachment in msg.attachments:
        #come up with a filename
        filename = msg.id + "-" + attachment['filename'].replace("-","_").replace(" ","_")

        #pull into temp folder and return
        temp = await saveFrog(attachment['url'], config.cfg['scraper']['staging'] + filename)
        return temp

async def getFrogFromURL(id, urls):
    for url in urls:
        filebase = url.split("/")[-1]
        filename = id + "-" + filebase.replace("-","_").replace(" ","_")
        temp = await saveFrog(url, config.cfg['scraper']['staging'] + filename)
        return temp

async def fetchFrogFromMessage(message):
    if message.attachments:
        resp = await getFrogFromUpload(message)
        return commitFrogToLibrary(resp)
    else:
        URLs = getLinksFromPost(message.content)
        resp = await getFrogFromURL(message.id, URLs)
        return commitFrogToLibrary(resp)

async def queueFrogFromMessage(message):
    if message.attachments:
        resp = await getFrogFromUpload(message)
        return resp
    else:
        URLs = getLinksFromPost(message.content)
        resp = await getFrogFromURL(message.id, URLs)
        return resp