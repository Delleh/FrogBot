import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s -> %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.info("Attempting to start. I can't promise you I will work but I can sure try.")

import pepobot.config
import pepobot.discord
import pepobot.functions
import pepobot.analytics
import pepobot.entropy
import pepobot.database

import pepobot.scraper
import pepobot.poster
import pepobot.administration
import pepobot.customizer

#start the discord connection
pepobot.discord.bot.run(pepobot.config.cfg['bot']['token'])

#TODO: 
# systemd service template
# all pepo/frogs should be generic