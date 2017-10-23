print("Importing... %s" % __name__)

from . import config
from . import functions
from . import discord
from . import analytics


@discord.bot.event
async def on_message(message):
	msgProcessStart = analytics.getEventTime()

	#print the message to the console only uncomment for debugging
	print("Channel: {0.channel} User: {0.author} (ID:{0.author.id}) Message: {0.content}".format(message))

	#handle message processing per rate limit
	if analytics.rateLimitAllowProcessing(message):
		await discord.bot.process_commands(message)

	#set the rate limit
	if message.author.id == discord.bot.user.id:
		analytics.rateLimitNewMessage(message.channel.id, analytics.getEventTime())

	#message processing timings
	analytics.onMessageProcessTime(msgProcessStart, analytics.getEventTime())