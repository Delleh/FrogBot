from . import config

import logging
import sqlite3
import time
import os

logger = logging.getLogger(__name__)
logger.info("loading...")

def check_init_database():
    pass

#first we need to know if the db file exists, if it does start the bot.
if os.path.isfile(config.cfg['db']['location']):
    con = sqlite3.connect(config.cfg['db']['location'], timeout=config.cfg['db']['timeout'])
    cursor = con.cursor()

    check_init_database()

    logger.info("DB loaded successfully!")
else:
    logger.warn("DB Does not exist! Creating new database and starting schema")
    con = sqlite3.connect(config.cfg['db']['location'])

    if con is None:
        logger.critical("Unable to make DB connection. Something seriously broken. (Permissions?)")
        exit()

    con.execute("CREATE TABLE `ratelimit_channel` ( `server` TEXT, `channel` TEXT UNIQUE, `setby` TEXT, `ratelimit` REAL, `time` TEXT )")
    con.execute("CREATE TABLE `ratelimit_server` ( `server` TEXT UNIQUE, `setby` TEXT, `ratelimit` REAL, `time` TEXT )")
    con.execute("CREATE TABLE `ignore_channel` ( `server` TEXT, `channel` TEXT UNIQUE, `setby` TEXT, `time` TEXT )")    
    con.execute("CREATE TABLE `ignore_user` ( `user` TEXT UNIQUE, `reason` INTEGER, `setby` TEXT, `time` TEXT )")
    con.commit()