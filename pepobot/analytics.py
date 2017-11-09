print("IMPORT: %s" % __name__)

from . import config
from . import functions
from . import discord
from . import entropy

import time

lastMessageChannels = {}

@discord.bot.event
async def on_message(message):
	#this controls the entropy pool size, to make sure its at least x of the start
	entropy.monitorPool()

	if message.author.id == discord.bot.user.id:
		return

	if rateLimitAllowProcessing(message):
		await discord.bot.process_commands(message)
		
	if message.author.id == discord.bot.user.id:
		rateLimitNewMessage(message.channel.id, getEventTime())

def getEventTime():
	return time.time()

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
	if msg.author.id == config.cfg['administration']['owner']:
		return True
	elif last >= config.cfg['bot']['rate']:
		return True
	else:
		print("RATE: '{0.author.name}' rate limited at '{0.channel.server.name}' in channel '#{0.channel.name}' last sent {1} seconds ago.".format(msg, last))
		return False