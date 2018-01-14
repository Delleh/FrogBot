import asyncio
import discord
import logging

from . import config
from . import entropy
from discord.ext import commands

logger = logging.getLogger(__name__)
logger.info("loading...")

bot = commands.Bot(command_prefix=config.cfg['bot']['prefix'], description=config.cfg['bot']['description'])

@bot.event
async def on_ready():
    entropy.resetPool()
    logger.info("Success! Logged in to Discord as '{0.user.name}' ({0.user.id})".format(bot))
    logger.info("To add this bot to a discord server, use https://discordapp.com/oauth2/authorize?client_id={0.user.id}&scope=bot&permissions=0".format(bot))
    bot.remove_command('help') #disable default help command its useless right now

    await asyncio.sleep(5)
    logger.info('Setting game status as in as "{0}"'.format(config.cfg['bot']['playing']))
    await bot.change_presence(game=discord.Game(name=config.cfg['bot']['playing']))

def objectFactory(snowflake):
    return discord.Object(snowflake)