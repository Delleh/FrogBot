import requests
import os
import sys


def imgur(url):
    #fetch the list of images to get
    req = requests.get("https://imgur.com/ajaxalbums/getimages/" + url.split("/")[-1] + "/hit.json")
    if req.status_code is not 200:
        print("ERROR: Unable to retrieve API, status code {0} from {1}".format(req.status_code, req.url))
        sys.exit()
    else:
        print("IMGUR: Got album via unofficial API. This could go very badly... got {0} bytes from {1}".format(req.headers['content-length'], req.url))
        album = req.json()
        print("IMGUR: unofficial API returned {0} results in album. Does this look correct?".format(len(album['data']['images'])))

    #verify if the user wants to go through with this knowing it could fuck up
    meme = input("IMPORT (USER INPUT): Type 'ok' to start. Any other input will cancel.\n")
    if meme != "ok":
        print("IMPORT: import cancelled :(")
        sys.exit(0)

    #download all of the images to the temp folder
    for image in album['data']['images']:
        req = requests.get("https://i.imgur.com/" + image['hash'] + image['ext'], stream=True)
        
        #error out if it doesnt exist
        if req.status_code is not 200:
            print("ERROR: Unable to retrieve image {0}, status code {1}".format(req.url, req.status_code))
            continue

        #save to temp folder
        print("IMGUR: Attempting to import {0}".format(req.url))
        tempimage = os.getcwd() + SLASHES + config.cfg['scraper']['staging'] + SLASHES + image['hash'] + image['ext']
        with open(tempimage, 'wb') as wr:
            for block in req.iter_content(1024):
                wr.write(block)

        #commit
        functions.commitFrogToLibrary(tempimage)