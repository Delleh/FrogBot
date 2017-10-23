print("Importing... %s" % __name__)

from . import config
from . import functions
from . import discord

import time

lastMessageChannels = {}
bernardGenesis = 0

def getEventTime():
	return time.time()

def setGenesis():
	return getEventTime()

#create a dict of all channels and the last time the bot spoke in the channel
def rateLimitNewMessage(channel, eventTime):
	lastMessageChannels[channel] = int(eventTime) #cast the float to an int, add it to a dictionary for all channels

#find the last time the bot spoke in channel, if the bot has never spoken since boot return the ratelimit in config.json
def rateLimitSinceLastMessage(channel):
	try:
		return int(getEventTime()) - lastMessageChannels[channel]
	except KeyError:
		return config.cfg['bot']['rate']

#controls if we should process commands or not
def rateLimitAllowProcessing(msg):
	last = rateLimitSinceLastMessage(msg.channel.id)
	if msg.author.id == config.cfg['administator']['owner']:
		return True
	elif last >= config.cfg['bernard']['ratelimit']:
		return True
	else:
		return False

setGenesis()