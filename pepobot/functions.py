print("Importing... %s" % __name__)

from . import config

import aiohttp
import glob
import hashlib
import imghdr
import os
import random
import re

def getLinksFromPost(msg):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)

def getAllFrogs():
    frogs = glob.glob(config.cfg['scraper']['location'] + "*")
    return frogs

def randomFrog():
    return random.choice(getAllFrogs())

def md5hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def getFileType(filename):
    filetype = imghdr.what(filename)
    if filetype in ['jpg','jpeg','png','gif','bmp']:
        return filetype
    else:
        return False

def deleteFrog(filename):
    return os.remove(config.cfg['scraper']['location'] + filename)

#ADD DUPE CHECKING, IF EQUAL IGNORE OTHERWISE MD5 NAME OR SOME RANDOM VAL
async def saveFrog(url, filename):
     async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        raw = await r.read()
                        with open(config.cfg['scraper']['location'] + filename, "wb") as wr:
                            wr.write(raw)
                        return filename
                    else:
                        return False

async def getFrogFromUpload(msg):
    for attachment in msg.attachments:
        filename = msg.id + "-" + attachment['filename'].replace("-","_").replace(" ","_")
        ret = await saveFrog(attachment['url'], filename)
        return ret

async def getFrogFromURL(id, urls):
    for url in urls:
        filebase = url.split("/")[-1]
        filename = id + "-" + filebase.replace("-","_").replace(" ","_")
        ret = await saveFrog(url, filename)
        return ret

async def fetchFrogFromMessage(message):
    if message.attachments:
        resp = await getFrogFromUpload(message)
        return resp
    else:
        URLs = getLinksFromPost(message.content)
        resp = await getFrogFromURL(message.id, URLs)
        return resp